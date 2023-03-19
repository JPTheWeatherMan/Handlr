Hello Dr Styer:

Thanks for checking out Jarrett and Jun's chatroom implementation.

You will find many hacky code excerpts, however, allow us to provide some reason to the insanity.

-- ENVIRONMENT --
    We have done testing on Windows 10 and VERY minor testing on Ubuntu

-- REQUIREMENTS --
    We expect that Tkinter for python is installed on your computer, if it is not run the following command in CMD

        pip install tk

-- RUNNING --
    In order to run the project effectively one must have the server running initially:
        this can be accomplished via
            python ./SOME_PATH_WHERE_FILES_LIVE/Handlr/server/main.py

        This will execute the server main.py file and you should see some output indicating you are listening

    Then you can open an instance of the UI
        this can be accomplished via
            python ./SOME_PATH_WHERE_FILES_LIVE/Handlr/client/main.py

        Where you will see a Tkinter window pop up prompting for the server's IP

-- WORKING FUNCTIONALITY --
    Logging in as ANY user
        Only one client of a user can be logged in at once
        Server can handle many users being authenticated

    Joining a room
        Messages come across cleanly
        Many users can join a room
    
    Leaving a room
        Messages come across cleanly
        Many users can also leave a room

    Chatting
        Can ONLY work with one person in a room but is proven to work via server logs
        BROKEN -- many clients in one room

-- Problems --
    We are experiencing a problem in which MANY clients connected to ONE room see a "clash" in messaging.
    A SINGLE client in a SINGLE room works flawlessly as indicated by logs produced in real time by the serer.

    -- WORKING EXAMPLE --
    Launch server
    Launch one UI instance
    Login as some user ex: user1, password = "abcdef"
    Join a chat room
    Send a chat
    View logging on server CMD output, as messages from self are added locally

    -- WHERE THINGS BREAK or HOW TO RECREATE --
    Launch server
    Launch one UI instance
    Login as some user ex: user1, password = "abcdef"
    join a chat room
    Launch another UI instance
    login as ANOTHER user ex: user2, password = "123456"
    
    BEFORE JOINING A CHAT ROOM ON SECOND CLIENT
        Send chats as a single entity in a chat room to verify functionality

    Join with second UI instance into SAME room as first client
        Send chats either way has the chance to break the server BUT not crash it
        Parts of chat messages will be interpreted as commands
        chat will INTERMITTENTLY work for PARTIAL messages

    -- Questions --
        Is this thread confusion?

        Is this happening because a UI process is trying to read and write at the same time?
            This is unlikely because the server sends messages to client NON-INCLUSIVELY

        Why does the socket connection not fail?

        Why does it work with one client but fails when another client is added?

        Do we need a separate thread for sending data?

