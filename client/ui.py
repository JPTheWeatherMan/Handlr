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

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            exit()

    def listenForMessages(self):
        while True:
            serverMessage = self.serverSocket.recv(4).decode("utf-8")
            if (str(serverMessage) == constants.SERVER_TO_CLIENT["VALID_LOGIN"]):
                self.show_frame(roomBrowser)
                pass
            if (str(serverMessage) == constants.SERVER_TO_CLIENT["INVALID_USERNAME_OR_PASSWORD"]):
                messagebox.showinfo("Invalid Login Warning", "You have entered wrong credentials")
                self.show_frame(promptForCredentials)
                pass
            if (str(serverMessage) == constants.SERVER_TO_CLIENT["ALREADY_LOGGED_IN"]):
                messagebox.showinfo("Invalid Login Warning", "Your account is currently in use")
                self.show_frame(promptForCredentials)
                pass    
            

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
        # if (config.DEBUG_MODE): print("ServerIP: {} \nUsername: {} \nPassword: {}".format(serverIp, username, password))
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
        # if (config.DEBUG_MODE): print("ServerIP: {} \nUsername: {} \nPassword: {}".format(serverIp, username, password))
        try:
            encodedUsername = str(username).encode("utf-8")
            usernameLength = len(encodedUsername)
            encodedPassword = str(password).encode("utf-8")
            passwordLength = len(encodedPassword)
            print("Username Length:{}\nPassword Length:{}".format(usernameLength, passwordLength))
            print("Username: {} \nPassword: {}".format(username, password))
            print("encoded username:{}\nEncoded password:{}".format(encodedUsername, encodedPassword))

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
        except socket.error:
            self.usernameInput.delete(0, tk.END)
            self.passwordInput.delete(0, tk.END)
        
class roomBrowser(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        roomBrowserListBox = tk.Listbox(self, selectmode="SINGLE", height="35", width="100")
        roomBrowserListBox.grid()
        roomBrowserListBox.grid_columnconfigure(0, weight=1)
        roomBrowserListBox.grid_rowconfigure(0, weight=1)
        # roomBrowserListBox.insert({})

        buttonContainer = tk.Frame(self)
        buttonContainer.grid()
        buttonContainer.grid_columnconfigure(0, weight=1)
        buttonContainer.grid_rowconfigure(0, weight=1)

        roomBrowserConnectButton = tk.Button(buttonContainer, text="Join Room", command=lambda: self.handleAttemptConnection("TEMP VALUE"))
        roomBrowserConnectButton.grid()
        roomBrowserConnectButton.grid_columnconfigure(0, weight=1)
        roomBrowserConnectButton.grid_rowconfigure(0, weight=1)

        roomBrowserLogoutButton = tk.Button(buttonContainer, text="Logout", command=lambda: self.handleLogout())
        roomBrowserLogoutButton.grid()
        roomBrowserLogoutButton.grid_columnconfigure(0, weight=1)
        roomBrowserLogoutButton.grid_rowconfigure(0, weight=1)


    def handleAttemptConnection(self, roomID):
        # TODO: Implement
        CLIENT_APPLICATION_STATE["CURRENT_ROOM"] = roomID
        self.controller.show_frame(displayChatRoom)

    def handleLogout(self):
        CLIENT_APPLICATION_STATE["CONNECTED_TO_SERVER"] = False
        CLIENT_APPLICATION_STATE["SERVER_IP"] = None
        CLIENT_APPLICATION_STATE["USERNAME"] = None
        CLIENT_APPLICATION_STATE["ROOM_LIST"] = None
        self.controller.show_frame(promptForIP)
        
class displayChatRoom(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        roomBrowserLogoutButton = tk.Button(self, text="Logout", command=lambda: self.handleLeave())
        roomBrowserLogoutButton.pack()

    def onConnect():
        # TODO: Get Users in chatroom
        # TODO: Prompt for nickname -- assert uniqueness at room scope
        # TODO: announce to server I have connected
        pass

    def handleLeave(self):
        CLIENT_APPLICATION_STATE["CURRENT_ROOM"] = None
        CLIENT_APPLICATION_STATE["NICKNAME_IN_ROOM"] = None
        self.controller.show_frame(roomBrowser)

    def handleSendMessage(message):
        pass

    def handleReceivedNewMessage(message):
        pass

    def userHasJoined():
        pass

    def userHasLeft():
        pass
