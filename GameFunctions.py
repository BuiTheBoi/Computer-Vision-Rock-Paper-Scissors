# Copyright (c) 2021 BuiTheBoi

# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import cv2 as cv
import mediapipe as mp
import random
import main


# Tracks which fingers are up and which are down
# If up, then append list with 1, if down then append with 0
def trackFingers(landmarks):
    tipIDs = [4, 8, 12, 16, 20]

    fingers = []

    # Thumb
    if (landmarks[tipIDs[0]][1] < landmarks[17][1]):    # Left Hand
        if (landmarks[tipIDs[0]][1] < landmarks[tipIDs[0]-1][1]):   # x axis of thumb tip
            fingers.append(1)   # Finger opened
        else:
            fingers.append(0)   # Finger closed
    elif (landmarks[tipIDs[0]][1] > landmarks[17][1]):  # Right hand
        if (landmarks[tipIDs[0]][1] > landmarks[tipIDs[0]-1][1]):   # x axis of thumb tip
            fingers.append(1)   # Finger opened
        else:
            fingers.append(0)   # Finger closed

    # Pointer, middle, ring, pinky fingers
    for id in range(1, 5):
        # If landmark at whichever finger tip is at higher position than
        # landmark below it
        if (landmarks[tipIDs[id]][2] < landmarks[tipIDs[id]-2][2]):
            fingers.append(1)   # Finger opened
        else:
            fingers.append(0)   # Finger closed

    return fingers


def usersMove(fingers):
    if (fingers == [0, 0, 0, 0, 0]):
        return "Rock"
    elif (fingers == [1, 1, 1, 1, 1]):
        return "Paper"
    elif (fingers == [0, 1, 1, 0, 0]):
        return "Scissors"
    else:
        return "Unknown"


def computersMove():
    num = random.randint(0, 2)
    moves = {
        0: "Rock",
        1: "Paper",
        2: "Scissors"
    }

    return moves[num]

# 4 possibilities: You won, computer won, draw, or error


def determineWinner(user, computer):
    # You chose 'Rock'
    if (user == "Rock"):
        if (computer == "Paper"):
            return "The Computer"
        elif (computer == "Scissors"):
            return "You"
        elif (computer == "Rock"):
            return "Draw"

    # You chose 'Paper'
    elif (user == "Paper"):
        if (computer == "Scissors"):
            return "The Computer"
        elif (computer == "Rock"):
            return "You"
        elif (computer == "Paper"):
            return "Draw"

    # You chose 'Scissors'
    elif (user == "Scissors"):
        if (computer == "Rock"):
            return "The Computer"
        elif (computer == "Paper"):
            return "You"
        elif (computer == "Scissors"):
            return "Draw"

    elif (user == "Unknown"):
        return "Error"


def displayScoreboard(img, user, computer):
    img = cv.putText(
        img, f"Your Points: {user}", (340, 440), cv.FONT_HERSHEY_PLAIN, 1.7, (0, 255, 0), 2)
    img = cv.putText(
        img, f"Computers Points: {computer}", (340, 465), cv.FONT_HERSHEY_PLAIN, 1.7, (0, 255, 0), 2)
    return img


# Global variables
userPoints = 0
computerPoints = 0


def reset():    # Resetting all stats after a new game
    global userPoints
    global computerPoints

    userPoints = 0
    computerPoints = 0
