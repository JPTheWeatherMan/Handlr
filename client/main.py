from ui import HandlrClientUI
from serverLink import ServerLink
from threading import *



def main():
    ui = HandlrClientUI()
    server = Thread(target=ServerLink, daemon=True).start()


if __name__ == "__main__":
    main()
