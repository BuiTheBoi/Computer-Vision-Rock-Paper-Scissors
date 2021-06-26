import cv2 as cv
import mediapipe as mp
import HandTrackingModule
import GameFunctions
import time


def main():
    capture = cv.VideoCapture(0)
    detector = HandTrackingModule.hand_detector()
    frames = 0
    count = 5

    # When video is playing
    while True:
        flag, img = capture.read()
        img = detector.findHands(img)

        landmarks = detector.findPositions(img, draw=False)

        print(f"Frame: {frames}")

        if (len(landmarks) != 0):

            # Counting down to detect hand
            img = cv.putText(img, str(count), (30, 30),
                             cv.FONT_HERSHEY_PLAIN, 1.0, (0, 255, 0), 4)
            if (frames % 25 == 0 and count != 0):
                count -= 1

            # leftOrRight = GameFunctions.detectLeftOrRight(landmarks)
            # if (leftOrRight == 'l'):
            #     print("Left Hand")
            # elif (leftOrRight == 'r'):
            #     print("Right Hand")

            if (count == 0):
                # Detecting user's choice of rock/paper/scissors
                fingersUp = GameFunctions.trackFingers(landmarks)
                userChoice = GameFunctions.usersMove(fingersUp)
                cv.putText(
                    img, f"You chose: {userChoice}", (20, 55), cv.FONT_HERSHEY_PLAIN, 1.5, (0, 0, 255), 2)

                # Computer's turn for rock/paper/scissors
                computerChoice = GameFunctions.computersMove()
                cv.putText(
                    img, f"The computer chose: {computerChoice}", (20, 70), cv.FONT_HERSHEY_PLAIN, 1.5, (0, 0, 255), 2)

                gameOutcome = GameFunctions.determineWinner(
                    userChoice, computerChoice)
                cv.putText(
                    img, gameOutcome, (221, img.shape[0] // 2), cv.FONT_HERSHEY_PLAIN, 3.0, (0, 255, 0), 3)

                # Showing who the winner is for quick 3 seconds
                cv.imshow("Rock Paper Scissors", img)
                cv.waitKey(0)

            cv.imshow("Rock Paper Scissors", img)
            frames += 1

        else:
            count = 4
            cv.imshow("Rock Paper Scissors", img)
            frames += 1

        # Press escape to exit program
        if (cv.waitKey(30) & 0xff == 27):
            break


if __name__ == "__main__":
    main()
