import kbhit
import os
import sys
import time
import WumpusGameEngine

ESC = chr(27)
ANSI = ESC + "["
CR = chr(13)

CHAT_START = 8
CHAT_END = 22
INPUT_LINE = 24

REFRESH_INTERVAL = 1

HOST = 'localhost'
PORT = '8080'
URL = ""
SESSION = ""

# Utils
def enable_ansi():
    if sys.platform[0 : 3] == "win":
        os.system('')

def clear_screen():
    print_part(ANSI + "2J")

def move_line(n):
    print_part(ANSI + str(n) + "H")

def erase_line(n):
    move_line(n)
    print_part(ANSI + "K")

def erase_lines(start, end):
    for line in range(start, end + 1):
        erase_line(line)

def print_part(s):
    print(s, end="", flush=True)

def input_async(timeout, echo=True):
    kb = kbhit.KBHit()

    ret = ""
    elapsed = 0
    while True:
        if kb.kbhit():
            c = kb.getch().capitalize()
            ret += c
            if echo==True:
                print_part(c)
            if c == CR:
                break
        else:
            time.sleep(0.1)
            elapsed += 0.1
            if elapsed > timeout:
                break
    return ret

# App Code
def list_users():
    print("TODO: get and print users")

def lobby_screen(login):
    clear_screen()
    print("Hello {}! You are now in the lobby. Other people here are:".format(login))
    print()
    list_users()
    print()
    print("Press the ENTER (or RETURN) key to start with the current players")
    while True:
        input = input_async(REFRESH_INTERVAL, echo=False)
        if len(input) > 0 and input[-1]==CR:
            break

chat_line = CHAT_START

def add_chat(s):
    global chat_line

    move_line(chat_line)
    print_part(s)
    chat_line = chat_line + 1
    if (chat_line > CHAT_END):
        chat_line = CHAT_START
        erase_lines(CHAT_START, CHAT_END)

def get_cmd():
    cmd = ""

    while True:
        erase_line(INPUT_LINE)
        print_part("> {}".format(cmd))

        input = input_async(REFRESH_INTERVAL)
        if len(input) > 0 and input[-1]==CR:
            input = input.rstrip()
            done = True
            break
        cmd += input

        idle()
    return cmd

def idle():
    add_chat("TODO: Print other users commands")
    # TODO poll server for chats
    # TODO poll server for round results

def game_screen():
    clear_screen()
    print("Hold down CTRL and press C (and ignore the call stack) to quit ...")
    print()

    WumpusGameEngine.displayRoomInfo()
    while True:
        cmd = get_cmd()
        print()
        convert_cmd_to_data(cmd)
        print("TODO: Send '{}' to server".format(cmd))

def convert_cmd_to_data(command):
    # JSH Assumption: It is better to have parsed the command into constituent parts for the backend
    # Move (M), Shoot (S), or Quit (Q)
    # TODO: We need to validate input sent to server.
    split_command = command.split()
    if len(split_command) > 1:
        if (split_command[0] == "MOVE" or split_command[0] == "M"):
            print("Sending Server Vote for MOVE")
            postMoveVote(SESSION, URL, {"MOVE" : split_command[1]})
        elif (split_command[0] == "SHOOT" or split_command[0] == "S"):
            print("Sending Server Vote for SHOOT")
            postMoveVote(SESSION, URL, {"SHOOT" : split_command[1]})
    else:
        if (command == "QUIT" or command == "Q"):
            # TODO: Client gracefully exits the game
            print("TODO: Client gracefully exits the game")
        if (command == "HELP" or command == "H"):
            print("Requesting help...")
            WumpusGameEngine.show_instructions()

async def init_connection_to_server(host, port):
    async with aiohttp.ClientSession() as SESSION:
        URL = 'http://{}:{}'.format(host, port)

async def postMoveVote(session, url, data):
    # InsertValue API call
    async with session.post(url, json=data) as response:
        return await response.text()

async def postStartGame(session, url, data):
    # StartGame API call
    async with session.post(url, json=data) as response:
        return await response.text()

async def postRegisterUser(session, url, data):
    # RegisterUser API call
    async with session.post(url, json=data) as response:
        return await response.text()

async def GetListUsers(session, url, data):
    # ListUsers API call
    async with session.post(url, json=data) as response:
        return await response.text()

async def GetVoteResult(session, url, data):
    # ListUsers API call
    async with session.post(url, json=data) as response:
        return await response.text()

def main():
    enable_ansi()
    WumpusGameEngine.init()
    init_connection_to_server(HOST, PORT)

    clear_screen()
    print("Welcome to PI Wumpus!")
    print()
    print("Please enter your name, handle, or other identifier:")

    login = input()
    lobby_screen(login)

    clear_screen()
    WumpusGameEngine.banner()

    game_screen()

if __name__ == "__main__":
    main()

