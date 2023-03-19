import socket
import threading
from tkinter import messagebox
import tkinter as tk
import constants
import struct


class HandlrClientUI(tk.Tk):

    def __init__(self, *args):
        tk.Tk.__init__(self, *args)

        #Tkinter boilerplate
        container = tk.Frame(self)
        self.geometry("800x600")
        self.resizable(tk.FALSE, tk.FALSE)
        container.pack(side=tk.TOP, fill=tk.BOTH, expand = True, anchor=tk.CENTER)

        #Thread for listening for messages coming from server
        self.serverListenerThread = None

        #Socket which maintains connection with serer
        self.serverSocket = None

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        #Build each UI page and map it to a local object
        for F in (promptForIP, promptForCredentials, roomBrowser, displayChatRoom):
            frame = F(container, self)
            self.frames[F] = frame
            self.frames[F].parentClass = self
            frame.grid(row=0, column=0, sticky="nsew")
            frame.grid_columnconfigure(0, weight=1)
            frame.grid_rowconfigure(0, weight=1)

        # Raise the IP prompt to the top of the view
        self.show_frame(promptForIP)

        self.mainloop()

    # Reads a string from the socket with a specified length
    # param: self - The parent UI object giving access to the socket
    # param: length - The amount of bytes we are expecting to read from the stream
    # returns: string - the decoded utf-8 message read from the stream
    def getStringFromSocketUsingLength(self, length):
        string = ""
        for i in range(length):
            newChar = self.serverSocket.recv(1)
            string += struct.unpack(">c", newChar)[0].decode("utf-8")
        return string

    # Raises a frame to the top the UI
    # param: self - The parent UI object which allows us to raise a particular frame to the top of the view
    # returns: void
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    # Handles the signal for closing the window to ask the user if that's what they want
    # param: self - the parent UI object
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            exit(0)

    # Handles listening for incoming messages from the server
    # Read a 4 byte window and decode as UTF-8 and map to a particular command and follow that logic down
    # param: self - the parent UI object containing the listener thread and socket
    # returns: void
    def listenForMessages(self):
        while True:
            try:
                serverMessage = self.serverSocket.recv(4).decode("utf-8")
            except socket.error as e:
                print("Had socket error: \t{}".format(e))
                messagebox.showinfo("Connection Error", "Socket experienced error")

            print("received: \t{}\n".format(serverMessage))

            #Valid Login
            if (str(serverMessage) == constants.SERVER_TO_CLIENT["VALID_LOGIN"]):
                self.show_frame(roomBrowser)

            #Invalid username or password
            if (str(serverMessage) == constants.SERVER_TO_CLIENT["INVALID_USERNAME_OR_PASSWORD"]):
                messagebox.showinfo("Invalid Login Warning", "You have entered wrong credentials")
                self.show_frame(promptForCredentials)

            #Already logged in
            if (str(serverMessage) == constants.SERVER_TO_CLIENT["ALREADY_LOGGED_IN"]):
                messagebox.showinfo("Invalid Login Warning", "Your account is currently in use")
                self.show_frame(promptForCredentials)

            #Have not joined a room
            if (str(serverMessage) == constants.SERVER_TO_CLIENT["NOT_JOINED_ROOM"]):
                messagebox.showinfo("No room", "You have not joined a chat room yet")
                self.show_frame(roomBrowser)

            #Have not joined a room
            if (str(serverMessage) == constants.SERVER_TO_CLIENT["ILLEGAL_OPERATION_NOT_LOGGED_IN"]):
                messagebox.showinfo("Error", "You have not logged in yet")
                self.show_frame(promptForCredentials)

            #Have not joined a room
            if (str(serverMessage) == constants.SERVER_TO_CLIENT["ILLEGAL_ROOM_NUMBER"]):
                messagebox.showinfo("Error", "You have attempted to join an invalid room")
                self.show_frame(roomBrowser)

            #I joined a room
            #Read the welcome message
            #Build a message
            #display the message on the chatroom interface
            if (str(serverMessage) == constants.SERVER_TO_CLIENT["I_JOINED_ROOM"]):
                welcomeMessageBytes = self.serverSocket.recv(2)
                welcomeMessageLength = int(struct.unpack(">H", welcomeMessageBytes)[0])
                welcomeMessage = self.getStringFromSocketUsingLength(welcomeMessageLength)
                self.show_frame(displayChatRoom)
                self.frames[displayChatRoom].messageBox.delete("1.0", tk.END)
                self.frames[displayChatRoom].messageBox.insert(tk.END,"Server: {}\n".format(welcomeMessage))

            #Someone else joined my room
            #Determine which user it is
            #Build a message
            #display the message on the chatroom interface
            if (str(serverMessage) == constants.SERVER_TO_CLIENT["USER_JOINED_ROOM"]):
                newlyJoinedUserBytes = self.serverSocket.recv(2)
                newlyJoinedUserLength = int(struct.unpack(">H", newlyJoinedUserBytes)[0])
                newlyJoinedUser = self.getStringFromSocketUsingLength(newlyJoinedUserLength)
                message = "{} has joined the chat\n".format(newlyJoinedUser)
                self.frames[displayChatRoom].messageBox.insert(tk.END, message)

            #Someone else left my room
            #Determine which user it is
            #Build a message
            #display the message on the chatroom interface
            if (str(serverMessage) == constants.SERVER_TO_CLIENT["USER_LEFT_ROOM"]):
                leavingUserBytes = self.serverSocket.recv(2)
                leavingUserLength = int(struct.unpack(">H", leavingUserBytes)[0])
                leavingUser = self.getStringFromSocketUsingLength(leavingUserLength)
                message = "{} has left the chat\n".format(leavingUser)
                self.frames[displayChatRoom].messageBox.insert(tk.END, message)

            #There is a message to interpret and display on the UI
            if (str(serverMessage) == constants.SERVER_TO_CLIENT["SEND_MESSAGE_TO_CLIENT"]):
                print("Received new message")
                # newMessageLengthBytes = self.serverSocket.recv(4)
                # newMessageLength = int(struct.unpack(">I", newMessageLengthBytes)[0])
                # print("of length {}". format(newMessageLength))
                # newMessage = self.getStringFromSocketUsingLength(newMessageLength)
                # print("and content of: {}".format(newMessage))

                # self.frames[displayChatRoom].messageBox.insert(tk.END,"Other user: {}\n".format(newMessage))


                senderNameBytes = self.serverSocket.recv(2)
                senderNameLength = int(struct.unpack(">H", senderNameBytes)[0])
                print("with u name length of {}".format(senderNameLength))
                senderName = self.getStringFromSocketUsingLength(senderNameLength)
                message = "from: {}".format(senderName)
                self.frames[displayChatRoom].messageBox.insert(tk.END,"{}\n".format(message))
                # print("{}: {}".format(senderName, newMessage))
                # self.frames[displayChatRoom].messageBox.insert(tk.END,"{}: {}\n".format(senderName, newMessage))

            #The room we are trying to join is full
            if (str(serverMessage) == constants.SERVER_TO_CLIENT["ROOM_FULL"]):
                messagebox.showinfo("Cannot join chat room", "The room you are attempting to join is full")
                self.show_frame(roomBrowser)    
            

#UI implementation for getting a server IP from the user
class promptForIP(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        #Controller for switching pages
        self.controller = controller

        #The parent container
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
        
    # Will attempt a TCP connection with server and raise a UI window on socket error
    # param: self - instance of this page for referencing the parent class containing the socket
    # param: serverIp - the ip of the server to attempt connecting to
    def handleSubmit(self, serverIp):
        print("ServerIP: {}".format(serverIp))
        try:
            #Validate that the socket is a valid IP
            socket.inet_aton(serverIp)

            #Attempt connection in parent UI
            self.parentClass.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.parentClass.serverSocket.connect((str(serverIp), int(4269)))

            #Kick off listener thread
            self.parentClass.serverListenerThread = threading.Thread(target=self.parentClass.listenForMessages, daemon=True)
            self.parentClass.serverListenerThread.start()

            #Clear input and show the credentials screen
            self.serverIPInput.delete(0, tk.END)
            self.controller.show_frame(promptForCredentials)
        except socket.error:
            messagebox.showinfo("IP Entry", "Please enter a valid IP address")
            self.serverIPInput.delete(0, tk.END)

#UI implementation for getting login credentials from a user
class promptForCredentials(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #Controller for switching pages
        self.controller = controller

        #the parent container
        self.parent = parent


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

    # Attempts to login to the chat service using username and password
    # param: self - The self object containing the parent socket for sending login information to
    # param: username - The string comprising a user's username
    # param: password - the string comprising as user's password
    def handleSubmit(self, username, password):
        #Encode username and password
        encodedUsername = str(username).encode("utf-8")
        usernameLength = len(encodedUsername)
        encodedPassword = str(password).encode("utf-8")
        passwordLength = len(encodedPassword)
        print("Username: {} \nPassword: {}".format(username, password))
        
        #Pack the username bytes into big endian format
        packedULength = struct.pack(">H", usernameLength)
        packedPLength = struct.pack(">H", passwordLength)
        packedUsr = struct.pack(">{}s".format(usernameLength), encodedUsername)
        packedPass = struct.pack(">{}s".format(passwordLength), encodedPassword)

        #Send Login flag to server
        self.parentClass.serverSocket.sendall(str(constants.CLIENT_TO_SERVER["LOGIN"]).encode("utf-8"))

        #Send length of parameters and parameters
        self.parentClass.serverSocket.sendall(packedULength)
        self.parentClass.serverSocket.sendall(packedUsr)
        self.parentClass.serverSocket.sendall(packedPLength)
        self.parentClass.serverSocket.sendall(packedPass)
        
        #Clear UI input  
        self.usernameInput.delete(0, tk.END)
        self.passwordInput.delete(0, tk.END)
        
#UI implementation for a window which displays chat rooms
class roomBrowser(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        #Controller for switching pages
        self.controller = controller

        #the parent container
        self.parent = parent

        #Container for all of the rooms provided by the service
        self.roomBrowserListBox = tk.Listbox(self, selectmode="SINGLE", height="35", width="100")
        self.roomBrowserListBox.grid()
        self.roomBrowserListBox.grid_columnconfigure(0, weight=1)
        self.roomBrowserListBox.grid_rowconfigure(0, weight=1)

        #map out each room in constants to an entry in the text box
        for roomName in constants.chat_rooms:
            self.roomBrowserListBox.insert(0, roomName)

        buttonContainer = tk.Frame(self)
        buttonContainer.grid()
        buttonContainer.grid_columnconfigure(0, weight=1)
        buttonContainer.grid_rowconfigure(0, weight=1)

        #Connect to room button
        roomBrowserConnectButton = tk.Button(buttonContainer, text="Join Room", command=lambda: self.handleAttemptConnection(self.roomBrowserListBox.get(self.roomBrowserListBox.curselection())))
        roomBrowserConnectButton.grid()
        roomBrowserConnectButton.grid_columnconfigure(0, weight=1)
        roomBrowserConnectButton.grid_rowconfigure(0, weight=1)

        #User logout button
        roomBrowserLogoutButton = tk.Button(buttonContainer, text="Logout", command=lambda: self.handleLogout())
        roomBrowserLogoutButton.grid()
        roomBrowserLogoutButton.grid_columnconfigure(0, weight=1)
        roomBrowserLogoutButton.grid_rowconfigure(0, weight=1)


    #Attempts to join a chatroom on behalf of a user
    # param: self - the parent object containing the socket
    # param: selection - the name of the room we wish to join
    # returns: void
    def handleAttemptConnection(self, selection):
        #Grab the room number from the map in constants
        room_number = constants.chat_rooms_to_room_number.get(selection)

        #pack the room number
        packedRoomNumber = struct.pack(">I", room_number)
        
        #Send the join room flag
        self.parentClass.serverSocket.sendall(str(constants.CLIENT_TO_SERVER["JOIN_CHAT_ROOM"]).encode("utf-8"))

        #send room number to server
        self.parentClass.serverSocket.sendall(packedRoomNumber)

    def handleLogout(self):
        print("Sending logout to server")
        self.parentClass.serverSocket.sendall(str(constants.CLIENT_TO_SERVER["LOGOUT"]).encode("utf-8"))
        self.controller.show_frame(promptForIP)
        
#UI implementation for a single chat room
class displayChatRoom(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #Controller for switching pages
        self.controller = controller

        #the parent container
        self.parent = parent

        #Display for chats which have been sent
        self.messageBox = tk.Text(self, width=50)
        self.messageBox.grid(row=0, column=0, padx=10, pady=10)

        #Text box for entering new chats
        self.messageEntry = tk.Entry(self, width=50)
        self.messageEntry.grid(row=1, column=0, padx=10, pady=10)

        #leave room button
        self.roomBrowserLogoutButton = tk.Button(self, text="Leave", command=lambda: self.handleLeave())
        self.roomBrowserLogoutButton.grid(row = 2, column=1, padx=10, pady=10)

        #send message button
        self.sendMessageButton = tk.Button(self, text="Send Message", command=lambda: self.handleSendMessage(self.messageEntry.get()))
        self.sendMessageButton.grid(row = 2, column=0, padx=10, pady=10)
    
    # Leaves a room on behalf of a user
    # param: self - The parent object containing the socket
    # returns: void
    def handleLeave(self):
        #send the leave room flag, server will interpret and handle logic on it's side
        self.parentClass.serverSocket.sendall(str(constants.CLIENT_TO_SERVER["LEAVE_CHAT_ROOM"]).encode("utf-8"))

        #Show the room browser
        self.controller.show_frame(roomBrowser)

    # Sends a message on behalf of a user
    # param: self - The parent object containing the socket
    # param: message - the string comprising the message to send
    # returns: void 
    def handleSendMessage(self, message):
        #if there's nothing in the message don't do anything at all, just clear input
        if len(message) == 0:
            self.messageEntry.delete(0, tk.END)
            return
        
        #encode message in utf-8
        encodedMessage = str(message).encode("utf-8")
        encodedMessageLength = len(encodedMessage)
        packedMessageLength = struct.pack(">I", encodedMessageLength)
        packedMessage = struct.pack(">{}s".format(encodedMessageLength), encodedMessage)
        self.messageBox.insert(tk.END,"You: {}\n".format(message))
        self.messageEntry.delete(0, tk.END)
        print(encodedMessageLength)
        print(packedMessageLength)
        self.parentClass.serverSocket.sendall(str(constants.CLIENT_TO_SERVER["SEND_MESSAGE_TO_ROOM"]).encode("utf-8"))
        self.parentClass.serverSocket.sendall(packedMessageLength)
        self.parentClass.serverSocket.sendall(packedMessage)
