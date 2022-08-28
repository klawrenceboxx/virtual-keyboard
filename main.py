# in order to make the virtual keyboard work we need to import 'Controller' from 'pynput.keyboard'

import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import numpy as np
from pynput.keyboard import Controller

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(dtectionCon = 0.8)
keyboard_keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"], 
                ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"], 
                ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]

# defining an empty string to store the typed keys
final_text = ""

keyboard = Controller()

def draw(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cvzone.cornerRect(img, (button.pos[0], button.pos[1], button.size[0], button.size[0],), 20, rt = 0)
        cv2.rectangle(img, button.pos, (int(x + w), int(y + h)), (255, 144, 30), cv2.FILLED)
        cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 4)
        return img

        