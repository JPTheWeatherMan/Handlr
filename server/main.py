#Listen for connection and start a new thread over port 4269 2
from socket import *
from threading import *
import constants
import struct

# Connection Data
#My local machine's IP 
host = '127.0.0.1'
port = 4269

# Starting Server with TCP Connection 
server = socket(AF_INET, SOCK_STREAM)

#To avoid https://stackoverflow.com/questions/6380057/python-binding-socket-address-already-in-use
server.setsockopt(SOL_SOCKET, SO_REUSEADDR,1)
server.bind((host, port))
print("Listening for connections on {}:{}".format(host,port))
server.listen()

connectedClients = set()
#Pre-defined chats
chat_rooms = {
    "csc460" : {
        "current_users": [],
        "current_nicknames": []
    },
    "csit" : {
        "current_users": [],
        "current_nicknames": []
    },
    "general" : {
        "current_users": [],
        "current_nicknames": []
    },
    "roomKim" : {
        "current_users": [],
        "current_nicknames": []
    },
    "roomHale" : {
        "current_users": [],
        "current_nicknames": []
    },
}
#Pre-defined users
users = {
     "user1": {
        "password": "abcdef",
        "is_logged_in": False
     },
     "user2": {
        "password": "123456",
        "is_logged_in": False
     },
     "user3":{
        "password": "chatroom",
        "is_logged_in": False
     }
}

#read the id and password from client thread
def loginUser(id , password):
    #Go through the users that we have to find a match 
    for user in users:
        #If valid user name
        if(user == id):
            userProfile = users.get(id)
            print(userProfile)
            print(password)
            #If match validate and change log in status if not return false 
            if(password == userProfile.get("password") and userProfile.get("is_logged_in") == False):
                users[id]["is_logged_in"] = True
                print(users[id]["is_logged_in"])
                return True
            else:
                return False
    return False

#read the id and password from client thread
def logoutUser(id):
    users[id]["is_logged_in"] = False

def getStringFromSocketUsingLength(length):
    string = ""
    for i in range(length):
        newChar = clientSocket.recv(1)
        string += struct.unpack(">s", newChar)[0].decode("utf-8")
    return string

def clientThread(clientSocket, clientAddress):
    command = clientSocket.recv(4).decode("utf-8")
    THREAD_STATE = {
        "ID": None
    }
    print("Received command: {}".format(command))

    # This is a request for log in from client to server 
    if (str(command) == constants.CLIENT_TO_SERVER["LOGIN"]):
        print("Login Sent")

        #This is for reading an id 
        userNameLengthBytes = clientSocket.recv(2)
        userNameLength = int(struct.unpack(">H", userNameLengthBytes)[0])
        userName = getStringFromSocketUsingLength(userNameLength)

        #This is for reading a password 
        passwordLengthBytes = clientSocket.recv(2)
        passwordLength = int(struct.unpack(">H", passwordLengthBytes)[0])
        password = getStringFromSocketUsingLength(passwordLength)  

        print("Received Login Request with username: {} and password: {}".format(userName, password))
        validatedUser = loginUser(userName, password)
        if(validatedUser == True):
            clientSocket.send(str(constants.SERVER_TO_CLIENT["VALID_LOGIN"]).encode("utf-8"))
            THREAD_STATE["ID"] = userName
            print("Did pass validation")

        #This will send a invalid log in message to those who enter wrong password
        if(validatedUser == False and users[userName]["is_logged_in"] == False):
            print("Did not pass validation")
            clientSocket.send(str(constants.SERVER_TO_CLIENT["INVALID_USERNAME_OR_PASSWORD"]).encode("utf-8"))

        #This will send a invalid log in to those who are already logged in 
        if(validatedUser == False and users[userName]["is_logged_in"] == True):
            print("Did not pass validation")
            clientSocket.send(str(constants.SERVER_TO_CLIENT["ALREADY_LOGGED_IN"]).encode("utf-8"))
    
    #This is a request for log out  from client to server
    if (command == constants.CLIENT_TO_SERVER["LOGOUT"]):
        THREAD_STATE["ID"]= None
        logoutUser(THREAD_STATE.get("ID"))
   

while True:
    clientSocket, clientAddress = server.accept()
    connectedClients.add(clientSocket)
    print("Connection established with {}".format(clientAddress))
    thread = Thread(target=clientThread, args=(clientSocket, clientAddress))
    thread.start()
                                  


