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

#For testing
MAX_USERS_PER_ROOM = 2


#Pre-defined chats
chat_rooms = {
    "csc460" : {
        "current_users": [],
        #message for the one who joined the chat 
        "welcomeMessage": "Welcome to csc460 chat",
         #message for the people in the chat
        "welcomeToOtherMessage": " has joined the chat",
        "leaveMessage": " has left the chat",
        "currentUserCount": 0,
        "capacity": MAX_USERS_PER_ROOM,
        "room_number": 1,
    },
    "csit" : {
        "room_number": 2,
        "currentUserCount": 0,
        "welcomeToOtherMessage": " has joined the chat",
        "leaveMessage": " has left the chat",
        "welcomeMessage": "Welcome to csit chat",
        "capacity": MAX_USERS_PER_ROOM,
        "current_users": [],
    },
    "general" : {
        "capacity": MAX_USERS_PER_ROOM,
        "currentUserCount": 0,
        "room_number": 3,
        "welcomeToOtherMessage": " has joined the chat",
        "leaveMessage": " has left the chat",
        "welcomeMessage": "Welcome to general chat",
        "current_users": [],
    },
    "roomKim" : {
        "room_number": 4,
        "currentUserCount": 0,
        "capacity": MAX_USERS_PER_ROOM,
        "welcomeToOtherMessage": " has joined the chat",
        "welcomeMessage": "Welcome to roomKim chat",
        "leaveMessage": " has left the chat",
        "current_users": [],
    },
    "roomHale" : {
        "room_number": 5,
        "current_users": [],
        "welcomeToOtherMessage": " has joined the chat",
        "leaveMessage": " has left the chat",
        "welcomeMessage": "Welcome to roomHale chat",
        "capacity": MAX_USERS_PER_ROOM,
        "currentUserCount": 0,
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
            #If match validate and change log in status if not return false 
            if(password == userProfile.get("password") and userProfile.get("is_logged_in") == False):
                users[id]["is_logged_in"] = True
                return True
            else:
                return False
    return False

#read the id and password from client thread
def logoutUser(id):
    print("ID passed to logout user {}".format(id))
    users[id]["is_logged_in"] = False

def getStringFromSocketUsingLength(length):
    string = ""
    for i in range(length):
        newChar = clientSocket.recv(1)
        string += struct.unpack(">s", newChar)[0].decode("utf-8")
    return string

def pushUser (id, roomName):
    # roomProfile = chat_rooms.get(roomName)
    chat_rooms[roomName]["current_users"].append(id)
    chat_rooms[roomName]["currentUserCount"]+=1
    print("room now looks like")
    print(chat_rooms.get(roomName))

def getRoomNameForRoomId(room_number):
    for room in chat_rooms:
        if(chat_rooms.get(room).get("room_number") == room_number):
            return room

def clientThread(clientSocket, clientAddress):
    CONNECTED = True
    THREAD_USERNAME = ""
    THREAD_ROOM = ""

    while CONNECTED:
        command = clientSocket.recv(4).decode("utf-8")
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
                THREAD_USERNAME = userName
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
        if (str(command) == constants.CLIENT_TO_SERVER["LOGOUT"]):
            print("Received logout from {}".format(THREAD_USERNAME))
            CONNECTED = False
            logoutUser(THREAD_USERNAME)

        if(str(command) == constants.CLIENT_TO_SERVER["JOIN_CHAT_ROOM"]):
            room_number_bytes = clientSocket.recv(4)
            room_number = int(struct.unpack(">I", room_number_bytes)[0])
            print("Received request to join room {} from {}".format(room_number, THREAD_USERNAME))
            #if not at capacity add the user to that room's current users
            room_name = getRoomNameForRoomId(room_number)
            print("Received request to join {}".format(room_name))
            if(chat_rooms[room_name].get("currentUserCount") < chat_rooms[room_name].get("capacity")):
                pushUser(THREAD_USERNAME, room_name)
                clientSocket.send(str(constants.SERVER_TO_CLIENT["I_JOINED_ROOM"]).encode("utf-8"))
                encodedWelcomeMessage = str(chat_rooms[room_name]["welcomeMessage"]).encode("utf-8")
                welcomeMessageLen = len(encodedWelcomeMessage)
                packedWelcomeMessageLen = struct.pack(">H", welcomeMessageLen)
                packedWelcomeMessage = struct.pack(">{}s".format(welcomeMessageLen), encodedWelcomeMessage)
                clientSocket.sendall(packedWelcomeMessageLen)
                clientSocket.sendall(packedWelcomeMessage)
                #TODO: Implement notifying other users in chat room
                #notifyOtherClients()

            #if the room is full send the CHAT_ROOM_FULL
            else:
                clientSocket.send(str(constants.SERVER_TO_CLIENT["ROOM_FULL"]).encode("utf-8"))
   

while True:
    clientSocket, clientAddress = server.accept()
    connectedClients.add(clientSocket)
    print("Connection established with {}".format(clientAddress))
    thread = Thread(target=clientThread, args=(clientSocket, clientAddress))
    thread.start()
                                  


