import cv2 as cv
import mediapipe as mp
import HandTrackingModule
import GameFunctions


# Global variables
userPoints = 0
computerPoints = 0


def main():
    global userPoints
    global computerPoints

    capture = cv.VideoCapture(0)
    detector = HandTrackingModule.hand_detector()
    tics = 0
    count = 5

    # When video is playing
    while True:
        flag, img = capture.read()  # img height: 480, width: 640
        img = detector.findHands(img)

        landmarks = detector.findPositions(img, draw=False)
        # img = GameFunctions.displayScoreboard(img, userPoints, computerPoints)

        # print(f"Frame: {tics}")

        if (len(landmarks) != 0):

            # Counting down to detect hand
            img = cv.putText(img, str(count), (30, 30),
                             cv.FONT_HERSHEY_PLAIN, 1.0, (0, 255, 0), 2)
            if (tics % 15 == 0 and count != 0):
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
                    img, f"You chose: {userChoice}", (20, 55), cv.FONT_HERSHEY_PLAIN, 1.5, (128, 0, 128), 2)

                # Computer's turn for rock/paper/scissors
                computerChoice = GameFunctions.computersMove()
                cv.putText(
                    img, f"The computer chose: {computerChoice}", (20, 70), cv.FONT_HERSHEY_PLAIN, 1.5, (128, 0, 128), 2)

                gameOutcome = GameFunctions.determineWinner(
                    userChoice, computerChoice)
                # Printing game outcome on the screen
                if (gameOutcome == "Draw"):
                    cv.putText(
                        img, "Draw!", ((img.shape[1] // 2) - 30, 400), cv.FONT_HERSHEY_PLAIN, 3.0, (180, 105, 255), 3)
                elif (gameOutcome == "Error"):
                    cv.putText(img, "Error detecting hand. Try again", (100,
                               400), cv.FONT_HERSHEY_PLAIN, 3.0, (0, 0, 255), 3)
                else:
                    if (gameOutcome == "You"):
                        userPoints += 1
                    else:
                        computerPoints += 1

                    if (userPoints == 2):   # Final winner is the User
                        cv.putText(
                            img, "CONGRATS! YOU WON!", (60, 400), cv.FONT_HERSHEY_PLAIN, 2.0, (255, 255, 0), 3)
                        GameFunctions.reset()
                        img = GameFunctions.displayScoreboard(
                            img, userPoints, computerPoints)
                    elif (computerPoints == 2):  # Final winner is the Computer
                        cv.putText(
                            img, "Opponent won.", (60, 390), cv.FONT_HERSHEY_PLAIN, 2.0, (255, 255, 0), 3)
                        cv.putText(
                            img, "Better luck next time!", (60, 415), cv.FONT_HERSHEY_PLAIN, 2.0, (255, 255, 0), 3)
                        GameFunctions.reset()
                        img = GameFunctions.displayScoreboard(
                            img, userPoints, computerPoints)
                    else:
                        cv.putText(
                            img, f"{gameOutcome} got a point!", (60, 400), cv.FONT_HERSHEY_PLAIN, 2.0, (255, 255, 0), 3)

                    print(f"You: {userPoints}")
                    print(f"Computer: {computerPoints}")

                # Showings results after each round until user presses a key to move on
                img = GameFunctions.displayScoreboard(
                    img, userPoints, computerPoints)
                cv.imshow("Rock Paper Scissors", img)
                cv.waitKey(0)
                count = 4

        else:
            count = 4

        img = GameFunctions.displayScoreboard(img, userPoints, computerPoints)
        cv.imshow("Rock Paper Scissors", img)
        tics += 1

        # Press escape to exit program
        if (cv.waitKey(30) & 0xff == 27):
            break


if __name__ == "__main__":
    main()
