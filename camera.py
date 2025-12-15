import cv2
import numpy as np

class Camera:
    def __init__(self, camera_adress, camera_height=640, camera_width=640):
        self.setCamera(camera_adress, camera_height, camera_width)
        
    def setCamera(self, camera_adress, camera_height, camera_width):
        self.__camera = cv2.VideoCapture(camera_adress)
        self.__camera.set(3, camera_width)
        self.__camera.set(4, camera_height)
    
    def capture(self):
        self.__ret, frame = self.__camera.read()
        return frame
    
    def getRet(self):
        return self.__ret
    
    def exit(self):
        self.__camera.release()