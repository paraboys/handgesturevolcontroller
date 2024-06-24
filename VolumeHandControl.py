import cv2
import time
import mediapipe as mp
import handtracking as htm
import numpy as np
import math

from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


Widcam,Heightcam=840,780

cap=cv2.VideoCapture(0)
cap.set(3,Widcam)
cap.set(4,Hieghtcam)
pTime=0

detector=htm.handDetector(detectionCon=0.7)



devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange=volume.GetVolumeRange()
minVol=volRange[0]
maxVol=volRange[1]
vol=0
volbar=400
volper=0


while True:
    success, img=cap.read()
    detector.findHands(img)
    lmlist=detector.findPosition(img,draw=False)
    if len(lmlist)!=0:
      #print (lmlist[2],lmlist[8])
      x1,y1=lmlist[4][1],lmlist[4][2]
      x2, y2 = lmlist[8][1], lmlist[8][2]
      cx,cy=(x1+x2)//2,(y1+y2)//2
      cv2.circle(img,(x1,y1),7,(255,125,255),cv2.FILLED)
      cv2.circle(img,(x2,y2),7,(255,125,255 ),cv2.FILLED)
      cv2.line(img,(x1,y1),(x2,y2),(255,125,255),3)
      cv2.circle(img, (cx, cy), 7, (255, 255, 0), cv2.FILLED)
      length=math.hypot(x2-x1,y2-y1)
      #print(length)
      #our length range is from 5-300
      #our vol range is from -96 to 0
      vol=np.interp(length,[50,300],[minVol,maxVol])
      volbar = np.interp(length, [50, 300], [400, 150])
      volper = np.interp(length, [50, 300], [0, 100])
      print(vol)
      volume.SetMasterVolumeLevel(vol, None)
      if length<50:
          cv2.circle(img, (cx, cy), 7, (0, 255, 255), cv2.FILLED)
    cv2.rectangle(img,(50,150),(85,400),(255,0,0),3)
    cv2.rectangle(img, (50, int(volbar)), (85, 400), (255, 0, 0), cv2.FILLED)
    cv2.putText(img, f'{int(volper)}%', (40, 450), cv2.FONT_HERSHEY_PLAIN, 1, (255,0, 0), 3)
    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img,f'FPS:{int(fps)} ',(40,40),cv2.FONT_HERSHEY_PLAIN,1,(0,255,0),2)
    cv2.imshow("img",img)
    cv2.waitKey(1)
