from socket import *
import threading
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

#hold sockets for connected clients
connectedClients = set()
#hold connected client thread to keep track of locking/unlocking 
clientThreads = set()

threadLock = threading.Lock()

#For testing
MAX_USERS_PER_ROOM = 10


#Pre-defined chats
chat_rooms = {
    "csc460" : {
        "room_number": 1,
        "currentUserCount": 0,
        "welcomeMessage": "Welcome to csc460 chat",
        "capacity": MAX_USERS_PER_ROOM,
        "current_users": [],
        "connected_client_addresses" : [],
    },
    "csit" : {
        "room_number": 2,
        "currentUserCount": 0,
        "welcomeMessage": "Welcome to csit chat",
        "capacity": MAX_USERS_PER_ROOM,
        "current_users": [],
        "connected_client_addresses" : [],
    },
    "general" : {
        "room_number": 3,
        "currentUserCount": 0,
        "capacity": MAX_USERS_PER_ROOM,
        "welcomeMessage": "Welcome to general chat",
        "current_users": [],
        "connected_client_addresses" : [],
    },
    "roomKim" : {
        "room_number": 4,
        "currentUserCount": 0,
        "capacity": MAX_USERS_PER_ROOM,
        "welcomeMessage": "Welcome to roomKim chat",
        "current_users": [],
        "connected_client_addresses" : [],
    },
    "roomHale" : {
        "room_number": 5,
        "currentUserCount": 0,
        "welcomeMessage": "Welcome to roomHale chat",
        "capacity": MAX_USERS_PER_ROOM,
        "current_users": [],
        "connected_client_addresses" : [],
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
     },
     "user4": {
        "password": "user4",
        "is_logged_in": False
     },
     "user5": {
        "password": "user5",
        "is_logged_in": False
     },
     "user6":{
        "password": "user6",
        "is_logged_in": False
     },
     "user7": {
        "password": "user7",
        "is_logged_in": False
     },
     "user8": {
        "password": "user8",
        "is_logged_in": False
     },
     "user9":{
        "password": "user9",
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

#read the id as a parameter and mark the user as logged out 
def logoutUser(id):
    print("ID passed to logout user {}".format(id))
    users[id]["is_logged_in"] = False

# Adjust current users and the count as one leaves the room 
def leaveRoom(roomNumber, id, clientAddress):
    chat_rooms[roomNumber]["currentUserCount"]-=1
    chat_rooms[roomNumber]["current_users"].remove(id)
    chat_rooms[roomNumber]["connected_client_addresses"].remove(clientAddress)

# Gets a string of length n from the clientSocket
# param: length - The length of the string we expect to receive
def getStringFromSocketUsingLength(length):
    string = ""
    for i in range(length):
        newChar = clientSocket.recv(1)
        print("raw new character:{}".format(newChar))
        unpackedChar = struct.unpack(">s", newChar)[0].decode("utf-8")
        if(str(unpackedChar).isalpha() or str(unpackedChar).isnumeric()):
            string+=str(unpackedChar)
        print("received character: {}".format(newChar))
        print("to create string so far: {}".format(string))
    return string

# Adjust current users and the count as one joins the room 
def pushUser (id, roomName, clientAddress):
    chat_rooms[roomName]["current_users"].append(id)
    chat_rooms[roomName]["currentUserCount"]+=1
    chat_rooms[roomName]["connected_client_addresses"].append(clientAddress)

#Converter between room and roomID to make it more accessible in code 
def getRoomNameForRoomId(room_number):
    for room in chat_rooms:
        if(chat_rooms.get(room).get("room_number") == room_number):
            return room
        

def lockThreadsExcluding():
    threadList = threading.enumerate()
    for i in threadList :
        if (i != threading.current_thread() and i != threading.main_thread()):
            threadLock.acquire()
            print("Locked a thread {}".format(i))

def unlockThreadsExcluding():
    #threading.Condition.notify_all()
    threadList = threading.enumerate()
    for i in threadList :
        if(i != threading.current_thread() and i != threading.main_thread()):
            threadLock.release()
            print("unlocked thread {}".format(i))
   
    
        
# function which handles all of the received data from clients
# param: clientSocket - representation of the connected client's TCP socket
# param: clientAddress - the string representation of a client's address
def clientThread(clientSocket, clientAddress):
    #Local thread state
    CONNECTED = True
    CLIENT_USERNAME = ""
    CLIENT_CHAT_ROOM = ""

    while CONNECTED:
        try:
            command = clientSocket.recv(4).decode("utf-8")
        except Exception as e:
            print("an error occurred: {}".format(e))
            clientSocket.close()
            connectedClients.remove(clientSocket)
        print("Received command: {}".format(command))

        if(command[0:2] == "0x"):
             # This is a request for log in from client to server 
            if (str(command) == constants.CLIENT_TO_SERVER["LOGIN"]):
                lockThreadsExcluding()
                print("Handling Login")

                #This is for reading an id 
                userNameLengthBytes = clientSocket.recv(2)
                userNameLength = int(struct.unpack(">H", userNameLengthBytes)[0])
                userName = getStringFromSocketUsingLength(userNameLength)

                #This is for reading a password 
                passwordLengthBytes = clientSocket.recv(2)
                passwordLength = int(struct.unpack(">H", passwordLengthBytes)[0])
                password = getStringFromSocketUsingLength(passwordLength)  

                print("Received Login Request with username: {} and password: {}".format(userName, password))

                #Validate that the user has the correct information
                validatedUser = loginUser(userName, password)
                if(validatedUser == True):
                    print("User {} has been validated".format(userName))
                    clientSocket.sendall(str(constants.SERVER_TO_CLIENT["VALID_LOGIN"]).encode("utf-8"))
                    #Assign CLIENT_USERNAME upon validated
                    CLIENT_USERNAME = userName
                    print("Did pass validation")
                    unlockThreadsExcluding()

                #This will send a invalid log in message to those who enter wrong password
                if(validatedUser == False and users[userName]["is_logged_in"] == False):
                    print("User {} has FAILED validation".format(userName))
                    clientSocket.sendall(str(constants.SERVER_TO_CLIENT["INVALID_USERNAME_OR_PASSWORD"]).encode("utf-8"))
                    unlockThreadsExcluding()

                #This will send a invalid log in to those who are already logged in 
                if(validatedUser == False and users[userName]["is_logged_in"] == True):
                    print("User {} has PASSED validation but is already logged in".format(userName))
                    clientSocket.sendall(str(constants.SERVER_TO_CLIENT["ALREADY_LOGGED_IN"]).encode("utf-8"))
                    unlockThreadsExcluding()
            
            #This is a request for log out  from client to server
            if (str(command) == constants.CLIENT_TO_SERVER["LOGOUT"]):
                lockThreadsExcluding()
                print("Received logout from {}".format(CLIENT_USERNAME))
                CONNECTED = False
                clientThreads.remove(CLIENT_USERNAME)
                logoutUser(CLIENT_USERNAME)
                unlockThreadsExcluding()
                
            #This is a request for joining a chat room 
            if(str(command) == constants.CLIENT_TO_SERVER["JOIN_CHAT_ROOM"]):
                lockThreadsExcluding()
                #If there is no username then the client has not logged in yet
                if CLIENT_USERNAME == "":
                    clientSocket.sendall(str(constants.SERVER_TO_CLIENT["ILLEGAL_OPERATION_NOT_LOGGED_IN"]).encode("utf-8"))
                    unlockThreadsExcluding()

                #Get the room to join
                room_number_bytes = clientSocket.recv(4)
                room_number = int(struct.unpack(">I", room_number_bytes)[0])
                
                #get the room name from the room number given to us from the client
                room_name = getRoomNameForRoomId(room_number)
                print("Received request to join room {} from {}".format(room_number, CLIENT_USERNAME))
                
                #Ensure the chat room is not at capacity
                if(chat_rooms[room_name].get("currentUserCount") < chat_rooms[room_name].get("capacity")):
                    pushUser(CLIENT_USERNAME, room_name, clientAddress)
                    CLIENT_CHAT_ROOM = room_name

                    #Grab the welcome message for the chat
                    encodedWelcomeMessage = str(chat_rooms[room_name]["welcomeMessage"]).encode("utf-8")
                    welcomeMessageLen = len(encodedWelcomeMessage)

                    #encode welcome message length + message
                    packedWelcomeMessageLen = struct.pack(">H", welcomeMessageLen)
                    packedWelcomeMessage = struct.pack(">{}s".format(welcomeMessageLen), encodedWelcomeMessage)

                    #Send the welcome message to our client
                    clientSocket.sendall(str(constants.SERVER_TO_CLIENT["I_JOINED_ROOM"]).encode("utf-8"))
                    clientSocket.sendall(packedWelcomeMessageLen)
                    clientSocket.sendall(packedWelcomeMessage)

                    #Build sending notification to other clients
                    encodedUserName = str(CLIENT_USERNAME).encode("utf-8")
                    usernameLength = len(encodedUserName)
                    packedUserLength = struct.pack(">H", usernameLength)
                    packedUser = struct.pack(">{}s".format(usernameLength), encodedUserName)
                    print("{} has successfully joined {}".format(CLIENT_USERNAME, CLIENT_CHAT_ROOM))
                    #send message to all clients in the chat when one joins the chat 
                    for socket in connectedClients:
                        for address in chat_rooms[CLIENT_CHAT_ROOM]["connected_client_addresses"]:
                            #Except for the one who joins 
                            if (socket is not clientSocket) and (address is not clientAddress):
                                print("Notifying socket: \t{}\n with address:\t{}\n that user: \t{}\nhas joined".format(socket, address, CLIENT_USERNAME))
                                socket.sendall(str(constants.SERVER_TO_CLIENT["USER_JOINED_ROOM"]).encode("utf-8"))
                                socket.sendall(packedUserLength)
                                socket.sendall(packedUser)
                    
                    unlockThreadsExcluding()
                #if the room is full send the CHAT_ROOM_FULL flag to the client
                else:           
                    clientSocket.sendall(str(constants.SERVER_TO_CLIENT["ROOM_FULL"]).encode("utf-8"))
                    unlockThreadsExcluding()


            #Remove Client from currentUsers, and decrement the currentUserCount
            # NOTE: the room is preserved by the clientThread and thus does not need to be sent from client
            if (str(command) == constants.CLIENT_TO_SERVER["LEAVE_CHAT_ROOM"]):
                lockThreadsExcluding()
                #If the client has not joined a room, send the error flag corresponding to not joined room
                if CLIENT_CHAT_ROOM == "":
                    clientSocket.sendall(str(constants.SERVER_TO_CLIENT["NOT_JOINED_ROOM"]).encode("utf-8"))
                    unlockThreadsExcluding()

                #If there is no username then the client has not logged in yet
                if CLIENT_USERNAME == "":
                    clientSocket.sendall(str(constants.SERVER_TO_CLIENT["ILLEGAL_OPERATION_NOT_LOGGED_IN"]).encode("utf-8"))
                    unlockThreadsExcluding()

                print("User {} has left the room {}".format(CLIENT_USERNAME,CLIENT_CHAT_ROOM))

                #remove the client from the room
                leaveRoom(CLIENT_CHAT_ROOM, CLIENT_USERNAME, clientAddress)

                #encode the user who has left the chat
                encodedUserName = str(CLIENT_USERNAME).encode("utf-8")
                usernameLength = len(encodedUserName)
                packedUserLength = struct.pack(">H", usernameLength)
                packedUser = struct.pack(">{}s".format(usernameLength), encodedUserName)
                print(chat_rooms[CLIENT_CHAT_ROOM]["connected_client_addresses"])

                #Handle propagating message to clients in same room
                for socket in connectedClients:
                    for address in chat_rooms[CLIENT_CHAT_ROOM]["connected_client_addresses"]:
                        #Except for the one who left
                        if (socket is not clientSocket) and (address is not clientAddress):
                            print("Notifying socket: \t{}\n with address:\t{}\n that user: \t{}\nhas left".format(socket, address, CLIENT_USERNAME))
                            socket.sendall(str(constants.SERVER_TO_CLIENT["USER_LEFT_ROOM"]).encode("utf-8"))
                            socket.sendall(packedUserLength)
                            socket.sendall(packedUser)

                #Empty out local thread room state because user has left their room
                CLIENT_CHAT_ROOM = ""
                unlockThreadsExcluding()


                
            #This handles sending messages to all clients in the same chat                             
            if(str(command) == constants.CLIENT_TO_SERVER["SEND_MESSAGE_TO_ROOM"]):
                lockThreadsExcluding()
                #If the client has not joined a room, send the error flag corresponding to not joined room
                if CLIENT_CHAT_ROOM == "":
                    clientSocket.sendall(str(constants.SERVER_TO_CLIENT["NOT_JOINED_ROOM"]).encode("utf-8"))

                print("Received a message from {} to be sent to room {}".format(CLIENT_USERNAME, CLIENT_CHAT_ROOM))
                messageLengthBytes = clientSocket.recv(4)
                messageLength = int(struct.unpack(">I", messageLengthBytes)[0])
                print("got message length: {}".format(messageLength))
                message = getStringFromSocketUsingLength(messageLength)
                print("got message {}: ".format(message))  

                encodedMessage = str(message).encode("utf-8")
                encodeMessageLength = len(encodedMessage)
                packedMessageLength = struct.pack(">I", encodeMessageLength)
                packedMessage = struct.pack(">{}s".format(encodeMessageLength), encodedMessage)

                encodedName = str(CLIENT_USERNAME).encode("utf-8")
                encodedNameLength = len(encodedName)
                packedNameLength = struct.pack(">H", encodedNameLength)
                packedName = struct.pack(">{}s".format(encodedNameLength), encodedName)            
                print("with name: {}".format(encodedName))

                #For all clients connected
                for socket in connectedClients:
                    #For all clients in the chat 
                    for address in chat_rooms[CLIENT_CHAT_ROOM]["connected_client_addresses"]:
                        #Except for the one who sent the message , send message packet 
                        if (socket is not clientSocket) and (address is not clientAddress):
                            print("With connected clients: \t {}\n".format(chat_rooms[CLIENT_CHAT_ROOM]["connected_client_addresses"]))
                            print("Sending message: \t{}\n to: \t{}\n from: \t{}\n".format(message, CLIENT_CHAT_ROOM,CLIENT_USERNAME))
                            socket.sendall(str(constants.SERVER_TO_CLIENT["SEND_MESSAGE_TO_CLIENT"]).encode("utf-8"))
                            socket.sendall(packedMessageLength)
                            socket.sendall(packedMessage)
                            socket.sendall(packedNameLength)
                            socket.sendall(packedName)
                unlockThreadsExcluding()
        else:
            print("Misunderstood command {}".format(command))

        # If no data is read from the socket then we assume the connection has been lost, remove 
        # them from the room and log them out, while closing the connection
        if not command:
            print("{} stopped sending data".format(clientAddress))
            logoutUser(CLIENT_USERNAME)
            leaveRoom(CLIENT_CHAT_ROOM, CLIENT_USERNAME, clientAddress)
            clientSocket.close()
            clientSocket.shutdown()
            connectedClients.remove(clientSocket)
   

while True:
    try:
        #Accept any connection which attempts
        clientSocket, clientAddress = server.accept()

        #Add the socket to our set for keeping track of connected clients
        connectedClients.add(clientSocket)

        print("Connection established with {}".format(clientAddress))

        #kick off client listener thread
        thread = threading.Thread(target=clientThread, args=(clientSocket, clientAddress))
        thread.start()

    except KeyboardInterrupt:
        exit(0)
