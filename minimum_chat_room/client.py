from socket import *
from threading import *
import tkinter as tk
from tkinter import messagebox

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

hostIp = "127.0.0.1"
portNumber = 4269

clientSocket.connect((hostIp, portNumber))

class clientGUI():
    def __init__(self, *args):
        self.window = tk.Tk()
        self.window.title("Minimum Client")

        self.messageBox = tk.Text(self.window, width=50)
        self.messageBox.grid(row=0, column=0, padx=10, pady=10)

        self.messageEntry = tk.Entry(self.window, width=50)
        self.messageEntry.insert(0,"Your message")
        self.messageEntry.grid(row=1, column=0, padx=10, pady=10)

        sendMessageBtn = tk.Button(self.window, text="Send", width=20, 
                                   command=lambda: self.sendMessage())
        sendMessageBtn.grid(row=2, column=0, padx=10, pady=10)

        self.recvThread = Thread(target=self.listenForMessages, daemon=True)
        self.recvThread.start()
        self.window.mainloop()


    def listenForMessages(self):
        while True:
            serverMessage = clientSocket.recv(1024).decode("utf-8")
            print(serverMessage)
            self.messageBox.insert(tk.END, str("\n"+serverMessage))

    def sendMessage(self):
        clientMessage = self.messageEntry.get()
        self.messageEntry.delete(0, tk.END)
        self.messageBox.insert(tk.END, str("\n" + "You: "+ clientMessage))
        clientSocket.send(clientMessage.encode("utf-8"))

clientGUI()







