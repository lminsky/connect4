import requests
import random
import threading

key = "ff28efc1-7227-4bef-9a1e-7b787099217"

def get_status(api_key):
    return requests.get("https://connect4.minsky.co/api/status", headers={"api-key": api_key})

def play(api_key, column):
    return requests.post("https://connect4.minsky.co/api/play", headers={"column": column, "api-key": api_key})

def join_game(api_key):
    return requests.post("https://connect4.minsky.co/api/join_game", headers={"api-key": api_key})

def leave_game(api_key):
    return requests.post("https://connect4.minsky.co/api/leave_game", headers={"api-key": api_key})

def bot_choice(board):
    for row in board:
        print(row)
    r = play(key, str(random.choice([0,1,2,3,4,5,6])))
    print(r.json())
    if r.json()['code'] == 18:
        threading.Timer(20, full_play, [key]).start()
    

def full_play(key):
    r = get_status(key)
    if r.status_code == 200:
        if r.json()['code'] == 9:
            r = join_game(key)
            print(r.json()['text'])
        elif r.json()['code'] == 6:
            if r.json()['your turn'] == True:
                print("your turn...")
                bot_choice(r.json()['board'])
            else:
                print("Opponent's turn")
                threading.Timer(20, full_play, [key]).start()
        else:
            print(r.json()['text'])
    else:
        print(r.content)

full_play(key)
# leave_game(key)