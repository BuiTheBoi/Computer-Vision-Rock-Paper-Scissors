import cv2 as cv
import mediapipe as mp
import random


def detectLeftOrRight(landmarks):
    # Thumb tip on LEFT of pinky tip
    if (landmarks[4][1] > landmarks[20][1]):
        return "r"
    # Thumb tip on RIGHT of pinky tip
    elif (landmarks[4][1] < landmarks[20][1]):
        return "l"


def instructions(img, sentence):
    # img = cv.rectangle(img, (0, 450),
    #                    (img.shape[1], img.shape[0]), (0, 0, 0), -1)
    img = cv.putText(img, sentence, (2, 460),
                     cv.FONT_HERSHEY_PLAIN, 2.0, (0, 255, 0), 2)
    return img


# Tracks which fingers are up and which are down
# If up, then append list with 1, if down then append with 0
def trackFingers(landmarks):
    tipIDs = [4, 8, 12, 16, 20]

    fingers = []

    # Thumb
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

# def computersMove(fingers):
