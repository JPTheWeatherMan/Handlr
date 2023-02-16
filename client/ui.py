import socket
from state import CLIENT_APPLICATION_STATE
from tkinter import messagebox
import tkinter as tk
import constants
import sys
sys.path.append("..")
from shared import util
from shared import config


class HandlrClientUI:

    def __init__(self):
        self.globalParent = tk.Tk()
        self.globalParent.geometry('800x600')
        self.globalParent.maxsize(800, 600)
        self.globalParent.minsize(800, 600)
        self.globalParent.title(constants.WINDOW_TITLE_FOR_UI)
        self.promptForIP(self.globalParent)
        self.roomBrowser(self.globalParent)
        self.globalParent.mainloop()

    def on_closing(self, root):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.globalParent.destroy()


    class promptForIP:
        def __init__(self, master):
            self.master = master
            self.frame = tk.Frame(self.master)

            # Server IP Label
            serverIPLabel = tk.Label(self.frame, text="Server IP: ", height="1")
            serverIPLabel.grid(row=0, column=0, padx=10, pady=5, sticky="e")

            # ServerIP Input
            serverIPInput = tk.Entry(
                self.frame, width="25")
            serverIPInput.grid(row=0, column=3, padx=10, pady=5, sticky="w")

            # Username Label
            usernameLabel = tk.Label(self.frame, text="Username: ", height="1")
            usernameLabel.grid(row=1, column=0, padx=10, pady=5, sticky="e")

            # Username Input
            usernameInput = tk.Entry(
                self.frame, width="25")
            usernameInput.grid(row=1, column=3, padx=10, pady=5, sticky="w")

            # Password Label
            passwordLabel = tk.Label(self.frame, text="Password: ", height="1")
            passwordLabel.grid(row=2, column=0, padx=10, pady=2)

            # Password Input
            passwordInput = tk.Entry(
                self.frame, show="*", width="25")
            passwordInput.grid(row=2, column=3, pady=2)

            # Submit button
            loginSubmitButton = tk.Button(self.frame, text="Submit", command=lambda: self.handleSubmit(
                serverIPInput.get(), usernameInput.get(), passwordInput.get()))
            loginSubmitButton.grid(row=4, column=0, columnspan=4, pady=5, sticky=tk.W+tk.E)

            self.frame.pack(pady=(150,0))
            
        def handleSubmit(self, serverIp, username, password):
            try:
                socket.inet_aton(serverIp)
            except socket.error:
                messagebox.showinfo(
                    "IP Entry", "Please enter a valid IP address")
            
            if (config.DEBUG_MODE):
                print("ServerIP: {} \nUsername: {} \nPassword: {}".format(
                    serverIp, username, password))
            #TODO: Validate user, save username to state, save server ip to state
            self.frame.pack_forget()
            


    class roomBrowser:
        def __init__(self, master):
            self.master = master
            self.frame = tk.Frame(self.master)

            roomBrowserListBox = tk.Listbox(
                self.frame, selectmode="SINGLE", width="50")
            roomBrowserListBox.grid(
                row=0, column=0, columnspan=20, rowspan=20, padx=5, pady=5, sticky="W")

            roomBrowserConnectButton = tk.Button(
                self.frame, text="Join Room", command=lambda: self.handleAttemptConnection("TEMP VALUE"))
            roomBrowserConnectButton.grid(row=0, column=21, pady=5)

            roomBrowserLogoutButton = tk.Button(
                self.frame, text="Logout", command=lambda: self.handleLogout())
            roomBrowserLogoutButton.grid(row=1, column=21, pady=2, padx=2, ipadx=7)

            self.frame.pack()

        def handleAttemptConnection(self, roomID):
            # TODO: Implement
            CLIENT_APPLICATION_STATE["CURRENT_ROOM"] = roomID
            self.frame.destroy()

        def handleLogout(self):
            CLIENT_APPLICATION_STATE["CONNECTED_TO_SERVER"] = False
            CLIENT_APPLICATION_STATE["SERVER_IP"] = None
            CLIENT_APPLICATION_STATE["USERNAME"] = None
            CLIENT_APPLICATION_STATE["ROOM_LIST"] = None
            self.frame.destroy()


    def displayChatRoom(self):
        def onConnect():
            # TODO: Get Users in chatroom
            # TODO: Prompt for nickname -- assert uniqueness at room scope
            # TODO: announce to server I have connected
            pass

        def handleLeave():
            CLIENT_APPLICATION_STATE["CURRENT_ROOM"] = None
            CLIENT_APPLICATION_STATE["NICKNAME_IN_ROOM"] = None

        def handleSendMessage(message):
            pass

        def handleReceivedNewMessage(message):
            pass

        def userHasJoined():
            pass

        def userHasLeft():
            pass

        chatRoom = tk.Tk()
        chatRoom.geometry('600x800')
        chatRoom.maxsize(600, 800)
        chatRoom.minsize(600, 800)
        chatRoom.title(constants.WINDOW_TITLE_FOR_UI)

        onConnect()
        chatRoom.protocol("WM_DELETE_WINDOW",
                          lambda: self.on_closing(chatRoom))
        chatRoom.mainloop()
