# Copyright (c) 2021 BuiTheBoi

# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

# Reference: https://www.youtube.com/watch?v=01sAkU_NvOY

import cv2 as cv
import mediapipe as mp
import time


class hand_detector():
    # Constructor
    def __init__(self, mode=False, max_hands=2, detection_confidence=0.5, track_confidence=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.detection_confidence = detection_confidence
        self.track_confidence = track_confidence

        # Initializations
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            self.mode, self.max_hands, self.detection_confidence, self.track_confidence)
        self.mpDraw = mp.solutions.drawing_utils

    # Sees if there is a hand that exists on camera
    def findHands(self, img, draw=True):
        # Must be converted to RGB before usage
        img_RGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(img_RGB)  # Gets all of the landmarks

        if(self.results.multi_hand_landmarks != None):  # If a hand is tracked
            for hand_landmarks in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, hand_landmarks,
                                               self.mpHands.HAND_CONNECTIONS)
        return img  # Returns image with drawing

    # Finds and returns a list of all landmarks on a single hand
    def findPositions(self, img, handNo=0, draw=True):
        landmark_list = []
        if(self.results.multi_hand_landmarks != None):
            # In case if there were multiple hands
            myHand = self.results.multi_hand_landmarks[handNo]

            for index, landmark in enumerate(myHand.landmark):
                height, width, channel = img.shape  # Gets width and height
                center_x, center_y = int(   # To get x and y coordinates
                    landmark.x * width), int(landmark.y * height)
                landmark_list.append([index, center_x,  center_y])

                if (draw):  # Draw large pink circle on desired landmark if True
                    cv.circle(img, (center_x, center_y),
                              25, (255, 0, 255), cv.FILLED)

        return landmark_list
