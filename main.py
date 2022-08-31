# in order to make the virtual keyboard work we need to import 'Controller' from 'pynput.keyboard'
# importing dependencies (libraries)
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import numpy as np
from pynput.keyboard import Controller

# lets us capture video, and sets the size of the screen
# taking real-time input from cv2.Videocapture
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, 1280)
cap.set(4, 720)

# creating an array of lists according to the layout of our keyboard
detector = HandDetector(detectionCon = 0.8)
keyboard_keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"], 
                ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"], 
                ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]

# defining an empty string to store the typed keys
final_text = ""

keyboard = Controller()

# defining a function that takes two arguments: an image, and the buttonList. returns the img
def draw(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size

        # cornerRect function inside cvzone will draw rectangle edges at the corner of each key to make our keyboard layout look nicer
        cvzone.cornerRect(img, (button.pos[0], button.pos[1], button.size[0], button.size[0],), 20, rt = 0)
        cv2.rectangle(img, button.pos, (int(x + w), int(y + h)), (255, 144, 30), cv2.FILLED)
        cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 4)
    return img

# creating a buttone class w/ position, text and size as the inputs to properly arrange our keys
class Button():
    def __init__(self, pos, text, size = [85, 85]):
        self.pos = pos
        self.size = size
        self.text = text

# loops through the keyboard keys and Button objects where the given inputs (position and text) are appended in a list called buttonList
# we can later pass this list to draw function to draw on top of our real frame
buttonList = []
for k in range(len(keyboard_keys)):
    for x, key in enumerate(keyboard_keys[k]):
        buttonList.append(Button([100 * x + 25, 100 * k + 50], key))

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bboxInfo = detector.findPosition(img)
    img = draw(img, buttonList) #change the draw function to transparent_layout for transparent
    
    if lmList:
        for button in buttonList:
            x, y = button.pos
            w, h = button.size

            if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                cv2.rectangle(img, button.pos, (x + w, y + h),
                (0, 255, 255), cv2.FILLED)
                cv2.putText(img, button.text, (x + 20, y + 65),
                cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 4)
                l, _, _ = detector.findDistance(8, 12, img, draw = False)
                print(l)

                if l < 25:
                    keyboard.press(button.text)
                    cv2.rectangle(img, button.pos, (x + w, y + h),
                    (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65),
                    cv2.FONT_HERSHEY_PLAIN, (0, 0, 0), 4)
                    final_text += button.text
                    sleep(0.20)

    cv2.rectangle(img, (25, 350), (700, 450),
                    (255, 255, 255), cv2.FILLED)
    cv2.putText(img, final_text, (60, 425),
                    cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 4)

    cv2.imshow("output", img)
    cv2.waitKey(1)