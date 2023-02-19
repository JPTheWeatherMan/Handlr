#Listen for connection and start a new thread over port 4269 2
from socket import *
from threading import *

# Connection Data
#My local machine's IP 
host = '127.0.0.1'
port = 4269

# Starting Server
server = socket(AF_INET, SOCK_STREAM)
server.setsockopt(SOL_SOCKET, SO_REUSEADDR,1)
server.bind((host, port))
print("Listening for connections on {}:{}".format(host,port))
server.listen()

connectedClients = set()
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


def loginUser(id , password):
    for user in users:
        if(user == id):
            if(password == users[id]["password"]):
                users[id]["is_logged_in"] = True
                return True
            else:
                return False
    return False

def logoutUser(id):
    users[id]["isLoggedIn"] = False


def clientThread(clientSocket, clientAddress):
    client_bytes = clientSocket.recv(1024).decode("utf-8")

    """ THIS IS PSEUDO-CODE
    command = clientSocket.recv(1 byte)
    if(commmand == 0x10-LOGIN)
        id_length = clientSocket.recv(2 byte)
        id = client.recv(id_length)
        pw_length = clientSocket.recv(2 byte)
        pw = client.recv(pw_length)
        if(validateUser(id, pw))
            clientSocket.send(0x82-LOGIN_SUCCESSFUL)
            clientSocket.send(0x84-LISTROOMS)
            clientSocket.send(4bytes PUBLIC_ROOMS)

            foreach client in Clients
                clientSocket.send(4bytes ROOM_NUMBER)
                clientSocket.send(2bytes ROOM_NAME_LENGTH)
                clientSocket.send(ROOM_NAME)
    """

while True:
    clientSocket, clientAddress = server.accept()
    connectedClients.add(clientSocket)
    thread = Thread(target=clientThread, args=(clientSocket, clientAddress))
    thread.start()
                                  


