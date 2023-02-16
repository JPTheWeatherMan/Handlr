WINDOW_TITLE_FOR_UI = "Handlr Client"

"""
SERVER_REQUESTS stores the flags required to request data from the server.
    Properties: The operation name in english
    Values:     The flag identifier expressed as a hex string
"""
SERVER_REQUESTS = {
    "LOGIN": "0x10",
    "LOGOUT": "0x14",
    "GET_CHAT_ROOMS": "0x17",
    "JOIN_CHAT_ROOM": "0x11",
    "LEAVE_CHAT_ROOM": "0x1B",
    "GET_USERS_IN_ROOM": "0x18",
    "SEND_MESSAGE_TO_ROOM": "0x12",
    "CHANGE_NICKNAME": "0x16",
}

