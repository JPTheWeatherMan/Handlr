import socket
import threading
from state import CLIENT_APPLICATION_STATE
from tkinter import messagebox
import tkinter as tk
import constants
import struct


class HandlrClientUI(tk.Tk):

    def __init__(self, *args):
        tk.Tk.__init__(self, *args)
        container = tk.Frame(self)
        self.geometry("800x600")
        self.resizable(tk.FALSE, tk.FALSE)
        container.pack(side=tk.TOP, fill=tk.BOTH, expand = True, anchor=tk.CENTER)

        self.serverListenerThread = None
        self.serverSocket = None

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (promptForIP, promptForCredentials, roomBrowser, displayChatRoom):
            frame = F(container, self)
            self.frames[F] = frame
            self.frames[F].parentClass = self
            frame.grid(row=0, column=0, sticky="nsew")
            frame.grid_columnconfigure(0, weight=1)
            frame.grid_rowconfigure(0, weight=1)

        self.show_frame(promptForIP)

        self.mainloop()

    def getStringFromSocketUsingLength(self, length):
        string = ""
        for i in range(length):
            newChar = self.serverSocket.recv(1)
            string += struct.unpack(">c", newChar)[0].decode("utf-8")
        return string

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            exit(0)

    def listenForMessages(self):
        while True:
            try:
                serverMessage = self.serverSocket.recv(4).decode("utf-8")
            except socket.error as e:
                print("Had socket error: \t{}".format(e))
                messagebox.showinfo("Connection Error", "Socket experienced error")

            if (str(serverMessage) == constants.SERVER_TO_CLIENT["VALID_LOGIN"]):
                self.show_frame(roomBrowser)

            if (str(serverMessage) == constants.SERVER_TO_CLIENT["INVALID_USERNAME_OR_PASSWORD"]):
                messagebox.showinfo("Invalid Login Warning", "You have entered wrong credentials")
                self.show_frame(promptForCredentials)

            if (str(serverMessage) == constants.SERVER_TO_CLIENT["ALREADY_LOGGED_IN"]):
                messagebox.showinfo("Invalid Login Warning", "Your account is currently in use")
                self.show_frame(promptForCredentials)

            if (str(serverMessage) == constants.SERVER_TO_CLIENT["I_JOINED_ROOM"]):
                welcomeMessageBytes = self.serverSocket.recv(2)
                welcomeMessageLength = int(struct.unpack(">H", welcomeMessageBytes)[0])
                welcomeMessage = self.getStringFromSocketUsingLength(welcomeMessageLength)
                self.show_frame(displayChatRoom)
                self.frames[displayChatRoom].messageBox.delete("1.0", tk.END)
                self.frames[displayChatRoom].messageBox.insert(tk.END,"Server: {}\n".format(welcomeMessage))

            if (str(serverMessage) == constants.SERVER_TO_CLIENT["USER_JOINED_ROOM"]):
                newlyJoinedUserBytes = self.serverSocket.recv(2)
                newlyJoinedUserLength = int(struct.unpack(">H", newlyJoinedUserBytes)[0])
                newlyJoinedUser = self.getStringFromSocketUsingLength(newlyJoinedUserLength)
                message = "{} has joined the chat\n".format(newlyJoinedUser)
                self.frames[displayChatRoom].messageBox.insert(tk.END, message)

            if (str(serverMessage) == constants.SERVER_TO_CLIENT["USER_LEFT_ROOM"]):
                leavingUserBytes = self.serverSocket.recv(2)
                leavingUserLength = int(struct.unpack(">H", leavingUserBytes)[0])
                leavingUser = self.getStringFromSocketUsingLength(leavingUserLength)
                message = "{} has left the chat\n".format(leavingUser)
                self.frames[displayChatRoom].messageBox.insert(tk.END, message)


            if (str(serverMessage) == constants.SERVER_TO_CLIENT["SEND_MESSAGE_TO_CLIENT"]):
                print("Received new message")
                newMessageLengthBytes = self.serverSocket.recv(4)
                newMessageLength = int(struct.unpack(">I", newMessageLengthBytes)[0])
                print("of length {}". format(newMessageLength))
                newMessage = self.getStringFromSocketUsingLength(newMessageLength)
                print("and content of: {}".format(newMessage))

                senderNameBytes = self.serverSocket.recv(2)
                senderNameLength = int(struct.unpack(">H", senderNameBytes)[0])
                print("with u name length of {}".format(senderNameLength))
                senderName = self.getStringFromSocketUsingLength(senderNameLength)
                print("{}: {}".format(senderName, newMessage))
                self.frames[displayChatRoom].messageBox.insert(tk.END,"{}: {}\n".format(senderName, newMessage))

            if (str(serverMessage) == constants.SERVER_TO_CLIENT["ROOM_FULL"]):
                messagebox.showinfo("Cannot join chat room", "The room you are attempting to join is full")
                self.show_frame(roomBrowser)    
            

class promptForIP(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent

        inputContainer = tk.Frame(self)
        inputContainer.pack(pady="20")

        # Server IP Label
        serverIPLabel = tk.Label(inputContainer, text="Server IP: ", height="1")
        serverIPLabel.pack()

        # ServerIP Input
        self.serverIPInput = tk.Entry(inputContainer)
        self.serverIPInput.insert(0, "127.0.0.1")
        self.serverIPInput.pack()

        # Submit button
        loginSubmitButton = tk.Button(self, text="Login", command=lambda: self.handleSubmit(
            self.serverIPInput.get()))
        loginSubmitButton.pack()
        
    def handleSubmit(self, serverIp):
        print("ServerIP: {}".format(serverIp))
        try:
            socket.inet_aton(serverIp)
            self.parentClass.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.parentClass.serverSocket.connect((str(serverIp), int(4269)))

            self.parentClass.serverListenerThread = threading.Thread(target=self.parentClass.listenForMessages, daemon=True)
            self.parentClass.serverListenerThread.start()

            self.serverIPInput.delete(0, tk.END)
            self.controller.show_frame(promptForCredentials)
        except socket.error:
            messagebox.showinfo("IP Entry", "Please enter a valid IP address")
            self.serverIPInput.delete(0, tk.END)

class promptForCredentials(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        inputContainer = tk.Frame(self)
        inputContainer.pack(pady="20")

        # Username Label
        usernameLabel = tk.Label(inputContainer, text="Username: ", height="1")
        usernameLabel.pack()
        # Username Input
        self.usernameInput = tk.Entry(inputContainer)
        self.usernameInput.pack()

        # Password Label
        passwordLabel = tk.Label(inputContainer, text="Password: ", height="1")
        passwordLabel.pack()
        # Password Input
        self.passwordInput = tk.Entry(inputContainer, show="*")
        self.passwordInput.pack()
  
        # Submit button
        loginSubmitButton = tk.Button(self, text="Login", command=lambda: self.handleSubmit(
            self.usernameInput.get(), self.passwordInput.get()))
        loginSubmitButton.pack()
    #Function to handle log in from client threads
    def handleSubmit(self, username, password):
        encodedUsername = str(username).encode("utf-8")
        usernameLength = len(encodedUsername)
        encodedPassword = str(password).encode("utf-8")
        passwordLength = len(encodedPassword)
        print("Username: {} \nPassword: {}".format(username, password))

        #Send Login flag to server
        self.parentClass.serverSocket.sendall(str(constants.CLIENT_TO_SERVER["LOGIN"]).encode("utf-8"))

        #Pack the username bytes into big endian format
        packedULength = struct.pack(">H", usernameLength)
        packedPLength = struct.pack(">H", passwordLength)
        packedUsr = struct.pack(">{}s".format(usernameLength), encodedUsername)
        packedPass = struct.pack(">{}s".format(passwordLength), encodedPassword)
        
        #Send length of parameters and parameters
        self.parentClass.serverSocket.sendall(packedULength)
        self.parentClass.serverSocket.sendall(packedUsr)
        self.parentClass.serverSocket.sendall(packedPLength)
        self.parentClass.serverSocket.sendall(packedPass)
        
        #Clear UI input  
        self.usernameInput.delete(0, tk.END)
        self.passwordInput.delete(0, tk.END)
        
class roomBrowser(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        self.roomBrowserListBox = tk.Listbox(self, selectmode="SINGLE", height="35", width="100")
        self.roomBrowserListBox.grid()
        self.roomBrowserListBox.grid_columnconfigure(0, weight=1)
        self.roomBrowserListBox.grid_rowconfigure(0, weight=1)
        for roomName in constants.chat_rooms:
            self.roomBrowserListBox.insert(0, roomName)

        buttonContainer = tk.Frame(self)
        buttonContainer.grid()
        buttonContainer.grid_columnconfigure(0, weight=1)
        buttonContainer.grid_rowconfigure(0, weight=1)

        roomBrowserConnectButton = tk.Button(buttonContainer, text="Join Room", command=lambda: self.handleAttemptConnection(self.roomBrowserListBox.get(self.roomBrowserListBox.curselection())))
        roomBrowserConnectButton.grid()
        roomBrowserConnectButton.grid_columnconfigure(0, weight=1)
        roomBrowserConnectButton.grid_rowconfigure(0, weight=1)

        roomBrowserLogoutButton = tk.Button(buttonContainer, text="Logout", command=lambda: self.handleLogout())
        roomBrowserLogoutButton.grid()
        roomBrowserLogoutButton.grid_columnconfigure(0, weight=1)
        roomBrowserLogoutButton.grid_rowconfigure(0, weight=1)


    def handleAttemptConnection(self, selection):
        # TODO: Implement
        print(selection)
        CLIENT_APPLICATION_STATE["CURRENT_ROOM"] = selection
        room_number = constants.chat_rooms_to_room_number.get(selection)
        self.parentClass.serverSocket.sendall(str(constants.CLIENT_TO_SERVER["JOIN_CHAT_ROOM"]).encode("utf-8"))
        packedRoomNumber = struct.pack(">I", room_number)
        self.parentClass.serverSocket.sendall(packedRoomNumber)

    def handleLogout(self):
        CLIENT_APPLICATION_STATE["CONNECTED_TO_SERVER"] = False
        CLIENT_APPLICATION_STATE["SERVER_IP"] = None
        CLIENT_APPLICATION_STATE["USERNAME"] = None
        CLIENT_APPLICATION_STATE["ROOM_LIST"] = None
        print("Sending logout to server")
        self.parentClass.serverSocket.sendall(str(constants.CLIENT_TO_SERVER["LOGOUT"]).encode("utf-8"))
        self.controller.show_frame(promptForIP)
        
class displayChatRoom(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.messageBox = tk.Text(self, width=50)
        self.messageBox.grid(row=0, column=0, padx=10, pady=10)

        self.messageEntry = tk.Entry(self, width=50)
        self.messageEntry.grid(row=1, column=0, padx=10, pady=10)

        self.roomBrowserLogoutButton = tk.Button(self, text="Leave", command=lambda: self.handleLeave())
        self.roomBrowserLogoutButton.grid(row = 2, column=1, padx=10, pady=10)

        self.sendMessageButton = tk.Button(self, text="Send Message", command=lambda: self.handleSendMessage(self.messageEntry.get()))
        self.sendMessageButton.grid(row = 2, column=0, padx=10, pady=10)

    def handleLeave(self):
        self.parentClass.serverSocket.sendall(str(constants.CLIENT_TO_SERVER["LEAVE_CHAT_ROOM"]).encode("utf-8"))
        self.controller.show_frame(roomBrowser)

    def handleSendMessage(self, message):
        if len(message) == 0:
            self.messageEntry.delete(0, tk.END)
            return
        
        encodedMessage = str(message).encode("utf-8")
        encodedMessageLength = len(encodedMessage)
        packedMessageLength = struct.pack(">I", encodedMessageLength)
        packedMessage = struct.pack(">{}s".format(encodedMessageLength), encodedMessage)
        self.messageBox.insert(tk.END,"You: {}\n".format(message))
        self.messageEntry.delete(0, tk.END)
        print(encodedMessageLength)
        print(packedMessageLength)
        self.messageEntry.delete(0, tk.END)
        self.parentClass.serverSocket.sendall(str(constants.CLIENT_TO_SERVER["SEND_MESSAGE_TO_ROOM"]).encode("utf-8"))
        self.parentClass.serverSocket.sendall(packedMessageLength)
        self.parentClass.serverSocket.sendall(packedMessage)
