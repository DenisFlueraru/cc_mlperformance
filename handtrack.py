import cv2
import mediapipe as mp
import time
import argparse
import random

from pythonosc import udp_client

data = " "
cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

parser = argparse.ArgumentParser()
parser.add_argument("--ip", default="127.0.0.1",
      help="The ip of the OSC server")
parser.add_argument("--port", type=int, default=5005,
    help="The port the OSC server is listening on")
args = parser.parse_args()

client = udp_client.SimpleUDPClient(args.ip, args.port)


while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    #print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                #print(id,lm)
                h, w, c = img.shape
                cx, cy = int(lm.x *w), int(lm.y*h)
                #if id ==0:
                cv2.circle(img, (cx,cy), 7, (255,0,255), cv2.FILLED)
                data = data + str(cx) + " " +str(cy)+ " "

                

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
            
            client.send_message("/wek/inputs", data)
            data = ""
            time.sleep(0.01)
           


    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img,str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)