WINDOW_TITLE_FOR_UI = "Handlr Client"

"""
SERVER_REQUESTS stores the flags required to request data from the server.
    Properties: The operation name in english
    Values:     The flag identifier expressed as a hex string
"""
#instead of having to remember the right hand side, make it more rememberable and developer-friendly
SERVER_TO_CLIENT = {    
    "I_JOINED_ROOM": "0x80",
    "USER_JOINED_ROOM": "0x81",
    "USER_LEFT_ROOM": "0x83",
    "VALID_LOGIN": "0x82",
    "ILLEGAL_ROOM_NUMBER": "0xC7",
    "ILLEGAL_OPERATION_NOT_LOGGED_IN": "0xC1",
    "INVALID_USERNAME_OR_PASSWORD": "0xC2",
    "USERS_IN_ROOM": "0x85",
    "SEND_MESSAGE_TO_CLIENT": "0x86",
    "ROOM_FULL": "0xC0",
    "ALREADY_LOGGED_IN": "0xC4",
}

CLIENT_TO_SERVER = {
    "LOGIN": "0x10",
    "LOGOUT": "0x14",
    "GET_CHAT_ROOMS": "0x17",
    "JOIN_CHAT_ROOM": "0x11",
    "LEAVE_CHAT_ROOM": "0x1B",
    "SEND_MESSAGE_TO_ROOM": "0x12",
}

#Pre-defined chats
chat_rooms = ["csc460", "csit", "general", "roomKim", "roomHale"]
chat_rooms_to_room_number = {
    "csc460" : 1,
    "csit" : 2,
    "general" : 3,
    "roomKim" : 4,
    "roomHale" : 5,
}
