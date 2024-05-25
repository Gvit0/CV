import cv2
import HTM
import numpy as np
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities,IAudioEndpointVolume

cap = cv2.VideoCapture(0)

handDet = HTM.handDetector(detectinCon=0.7)

audioDev = AudioUtilities.GetSpeakers()
interface = audioDev.Activate(IAudioEndpointVolume._iid_,CLSCTX_ALL,None)
volume = cast(interface,POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
volmin = volRange[0]
volmax = volRange[1]
HMIN, HMAX = 20, 140
while True:
    succeed, img = cap.read()
    img = handDet.findHand(img,True)

    lmList = handDet.findPosition(img)
    if len(lmList) != 0:
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2


        xt, yt = lmList[12][1], lmList[12][2]
        xt1, yt1 = lmList[9][1], lmList[9][2]
        xt2, yt2 = lmList[5][1], lmList[5][2]
        xt3, yt3 = lmList[17][1], lmList[17][2]
        xt4, yt4 = lmList[0][1], lmList[0][2]
                
        cv2.circle(img, (x1, y1), 15, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 0), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2),(255, 0, 0), 3)
        cv2.circle(img, (cx, cy), 15, (255, 0, 0), cv2.FILLED)
        print(xt, yt)
        if xt2 >= xt and xt <= xt3:
            if yt1 <= yt and yt >= yt4:
                legth = math.hypot(x2-x1, y2-y1)
                vol = np.interp(legth, [HMIN, HMAX], [volmin,volmax])
                print(int(legth))#120 50
                volume.SetMasterVolumeLevel(vol,None)
    cv2.imshow("Img",img)
    cv2.waitKey(1)
