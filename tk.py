import cv2
import time
import HandTrackingModule as htm
import math
import random
import threading
import tkinter as tk
from tkinter import simpledialog, messagebox
from collections import Counter

# Initialize the hand detector and video capture outside the function
wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(detectionCon=0.7)
pTime = 0

def detect_gesture():
    global pTime
    gestures = []
    start_time = time.time()

    # Capture gestures for 2 seconds
    while time.time() - start_time < 2:
        success, img = cap.read()
        img = detector.findHands(img, draw=False)
        lmList = detector.findPosition(img, draw=False)
        gesture = None

        if len(lmList) != 0:
            lengths = []
            for x in range(8, 21, 4):
                length = math.hypot(lmList[x - 4][1] - lmList[x][1], lmList[x - 4][2] - lmList[x][2])
                lengths.append(length)

            basel = []
            for x in range(8, 21, 4):
                length = math.hypot(lmList[x][1] - lmList[x-3][1], lmList[x][2] - lmList[x-3][2])
                basel.append(length)

            if basel[0] < 40 and basel[1] < 40 and basel[2] < 40 and basel[3] < 40:
                gesture = "ROCK"
            elif lengths[0] > 70 and lengths[1] > 50 and lengths[2] > 43 and lengths[3] > 50 and basel[3] > 80:
                gesture = "PAPER"
            elif lengths[1] > 55 and lengths[3] < 50:
                gesture = "SCISSOR"

            if gesture:
                gestures.append(gesture)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
        cv2.imshow("Live Image", img)
        cv2.waitKey(1)

    # Return the most common gesture
    if gestures:
        print(Counter(gestures).most_common(1)[0][0])
        return Counter(gestures).most_common(1)[0][0]
    else:
        return None

# Game logic and scorekeeping
def game():
    global rounds
    global round_number
    global player_score
    global bot_score
    global running
    global score_label

    for round_number in range(1, rounds + 1):
        if not running:
            break
        score_label['text'] = f'Round: {round_number}, Scores -> Player: {player_score}, Bot: {bot_score}'
        for i in range(3, 0, -1):
            score_label['text'] += f'\nRound starts in {i}...'
            time.sleep(1)
        player_move = detect_gesture()
        if player_move:
            bot_move = random.choice(['ROCK', 'PAPER', 'SCISSOR'])
            # print(bot_move)
            if (player_move == 'ROCK' and bot_move == 'SCISSOR') or (player_move == 'PAPER' and bot_move == 'ROCK') or (player_move == 'SCISSOR' and bot_move == 'PAPER'):
                player_score += 1
            elif player_move == bot_move:
                pass
            else:
                bot_score += 1
        score_label['text'] = f'Round: {round_number}, Scores -> Player: {player_score}, Bot: {bot_score}'

# GUI functions
def start_game():
    global rounds
    global running
    global game_thread

    if not running:
        rounds = simpledialog.askinteger("Rounds", "Enter number of rounds (3 or 5):", parent=root, minvalue=3, maxvalue=5)
        if rounds is None:  # If the user closes the input dialog
            return
        running = True
        game_thread = threading.Thread(target=game)
        game_thread.start()

def stop_game():
    global running
    global game_thread

    if running:
        running = False
        game_thread.join()

# Initialize scores, run status, and round number
player_score = 0
bot_score = 0
running = False
rounds = 0
round_number = 0

# Create the GUI
root = tk.Tk()
score_label = tk.Label(root, text='Game not started yet.')
score_label.pack()
start_button = tk.Button(root, text="Start", command=start_game)
stop_button = tk.Button(root, text="Stop", command=stop_game)
start_button.pack()
stop_button.pack()
root.mainloop()

# Clean up after closing the GUI
cap.release()
cv2.destroyAllWindows()