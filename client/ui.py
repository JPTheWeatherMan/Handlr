import socket
from state import CLIENT_APPLICATION_STATE
from tkinter import messagebox
import tkinter as tk
import constants
import sys
sys.path.append("..")
from shared import util
from shared import config


class HandlrClientUI(tk.Tk):

    def __init__(self, *args):
        tk.Tk.__init__(self, *args)
        container = tk.Frame(self)
        self.geometry("800x600")
        self.resizable(tk.FALSE, tk.FALSE)
        container.pack(side=tk.TOP, fill=tk.BOTH, expand = True, anchor=tk.CENTER)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (promptForIP, roomBrowser, displayChatRoom):
            frame = F(container, self)
            self.frames[F] = frame
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

    def showRoomBrowser(self):
        self.roomBrowserFrame = self.roomBrowser(self.globalParent)
    
    def showIpPrompt(self):
        print("I'm running")
        self.ipFrame = self.promptForIP(self.globalParent)

class promptForIP(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        inputContainer = tk.Frame(self)
        inputContainer.pack(pady="20")

        # Server IP Label
        serverIPLabel = tk.Label(inputContainer, text="Server IP: ", height="1")
        serverIPLabel.pack()

        # ServerIP Input
        self.serverIPInput = tk.Entry(inputContainer)
        self.serverIPInput.pack()

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
            self.serverIPInput.get(), self.usernameInput.get(), self.passwordInput.get()))
        loginSubmitButton.pack()
        
    def handleSubmit(self, serverIp, username, password):
        if (config.DEBUG_MODE): print("ServerIP: {} \nUsername: {} \nPassword: {}".format(serverIp, username, password))
        try:
            socket.inet_aton(serverIp)
            #TODO: move socket connection to use threaded connection and work off of pipeline
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((str(serverIp), int(config.SERVICE_PORT)))
            #TODO: Validate user, save username to state, save server ip to state
          
            self.serverIPInput.delete(0, tk.END)
            self.usernameInput.delete(0, tk.END)
            self.passwordInput.delete(0, tk.END)
            self.controller.show_frame(roomBrowser)
        except socket.error:
            messagebox.showinfo("IP Entry", "Please enter a valid IP address")
            self.serverIPInput.delete(0, tk.END)
        
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
