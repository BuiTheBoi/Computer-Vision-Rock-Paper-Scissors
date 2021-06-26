import cv2 as cv
import mediapipe as mp
import HandTrackingModule
import GameFunctions


def main():
    capture = cv.VideoCapture(0)
    detector = HandTrackingModule.hand_detector()
    frames = 0
    count = 3

    # When video is playing
    while True:
        flag, img = capture.read()
        img = detector.findHands(img)

        landmarks = detector.findPositions(img, draw=False)

        print(f"Frame: {frames}")

        if (len(landmarks) != 0):
            img = cv.putText(img, str(count), (30, 30),
                             cv.FONT_HERSHEY_PLAIN, 1.0, (0, 255, 0), 2)
            if (frames % 25 == 0 and count != 0):
                count -= 1
            # leftOrRight = GameFunctions.detectLeftOrRight(landmarks)
            # if (leftOrRight == 'l'):
            #     print("Left Hand")
            # elif (leftOrRight == 'r'):
            #     print("Right Hand")

            # Counting down to detect hand

            if (count == 0):
                # Detecting user's choice of rock/paper/scissors
                fingersUp = GameFunctions.trackFingers(landmarks)
                userChoice = GameFunctions.userMove(fingersUp)
                GameFunctions.instructions(img, f"You chose: {userChoice}")

            cv.imshow("Rock Paper Scissors", img)
            frames += 1

        else:
            count = 3
            cv.imshow("Rock Paper Scissors", img)
            frames += 1

        # Press escape to exit program
        if (cv.waitKey(30) & 0xff == 27):
            break


if __name__ == "__main__":
    main()
