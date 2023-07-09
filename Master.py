import cv2
import time
import HandTrackingModule as htm
import math

################################
wCam, hCam = 640, 480
################################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
detector = htm.handDetector(detectionCon=0.7)
flag=True

while True:
    success, img = cap.read()
    img = detector.findHands(img,draw=False)
    lmList = detector.findPosition(img,draw=False)

    if(len(lmList)!=0):
        lengths = []
        for x in range(8, 21, 4):
            length = math.hypot(lmList[x - 4][1] - lmList[x][1], lmList[x - 4][2] - lmList[x][2])
            lengths.append(length)

        basel = []
        for x in range(8, 21, 4):
            length = math.hypot(lmList[x][1] - lmList[x-3][1], lmList[x][2] - lmList[x-3][2])
            basel.append(length)

        if(basel[0]<40 and basel[1]<40 and basel[2]<40 and basel[3]<40):
            print("ROCK")
        elif(lengths[0]>70 and lengths[1]>50 and lengths[2]>43 and lengths[3]>50 and basel[3]>80):
            print("PAPER")
        elif(lengths[1]>55 and lengths[3]<50):
            print("SCISSOR")


    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    tempimg = cv2.flip(img, 1)
    cv2.putText(tempimg, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)
    cv2.imshow("Live Image", tempimg)
    if cv2.waitKey(1) == 13 or flag == False:  # 13 is the Enter Key
        break
