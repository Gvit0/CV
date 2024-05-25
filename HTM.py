import cv2
import mediapipe as mp
import time





class handDetector():
    def __init__(self, mode=False, maxHands=10, detectinCon = 0.5, trackCon = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectinCon = detectinCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,1,self.detectinCon,self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHand(self,img,draw=False):
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.handsPoints = self.hands.process(imgRGB)
        if self.handsPoints.multi_hand_landmarks:
            for handLms in self.handsPoints.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img,handNo=0, draw=False):
        lmList= []
        if self.handsPoints.multi_hand_landmarks:
            myHand = self.handsPoints.multi_hand_landmarks[handNo]
            for id,lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx,cy = int(lm.x * w),int(lm.y * h)
                lmList.append([id,cx,cy])
                if draw:
                    cv2.circle(img,(cx,cy),15,(255,0,0),cv2.FILLED)
        return lmList

def main():
    cap = cv2.VideoCapture(0)
    mpHands = mp.solutions.hands
    hands = mpHands.Hands(False, 4)
    mpDraw = mp.solutions.drawing_utils
    detector = handDetector()
    while True:
        success, img = cap.read()
        img=detector.findHand(img,True)
        lmList =detector.findPosition(img,0)
        
        cv2.imshow("Img", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()