# Requests

Note: all commends in hex (0x00) are going to be 1 byte

each index of a hex number requires 4 bits to represent 0-15

# Client --> Server

* Login
    * 1 byte 0x10
    * 2 bytes id_len
    * id_len id
    * 2 bytes pw_len
    * pw_len pw

# Server --> Client

* Successful Login
    * 1byte 0x82

