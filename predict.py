from ultralytics import YOLO
import cv2
import torch
import numpy as np


class Detector:
    def __init__(self, detector_path, device):
        self.__device = device
        self.__load_model(detector_path)

    def __load_model(self, detector_path):
        self.__model = YOLO(detector_path).to(self.__device)
        print("Valf detector model has been loaded !")    

    def predict(self, data):
        results = self.__model(data, stream=True, verbose=False)
        return results
    
    def postprocess(self, img):
        img_np = img.squeeze().cpu().numpy().astype(np.uint8)
        img_np = cv2.cvtColor(img_np.transpose(1, 2, 0), cv2.COLOR_BGR2RGB)
        return img_np
    
    def preprocess(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = torch.from_numpy(img).permute(2, 0, 1).float()
        img = img.unsqueeze(0).to(self.__device)
        img = torch.nn.functional.interpolate(img, size=(640, 640), mode='bilinear', align_corners=False)
        
        return img


class ImgProcess:
    @staticmethod
    def crop (img):
        #topLeft = (973,371) # x,y
        #bottomRight = (1207,611)
        croppedImg = img[329:545, 928:1135]
        return croppedImg
    @staticmethod
    def rotate(image):
        height, width = image.shape[:2]

        # Döndürme merkezini hesapla
        center = (width / 2, height / 2)

        angle = -15 
        scale = 1.0 
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, scale)

        # Görüntüyü döndür
        rotated_image = cv2.warpAffine(image, rotation_matrix, (width, height))
        return rotated_image
    
    @staticmethod
    def preprocess(img, device):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = torch.from_numpy(img).permute(2, 0, 1).float()
        img = img.unsqueeze(0).to(device)
        img = torch.nn.functional.interpolate(img, size=(640, 640), mode='bilinear', align_corners=False)
        return img
    
    @staticmethod
    def postprocess(img):
        img_np = img.squeeze().cpu().numpy().astype(np.uint8)
        img_np = cv2.cvtColor(img_np.transpose(1, 2, 0), cv2.COLOR_BGR2RGB)
        return img_np

class ValfCounter:
    @staticmethod
    def counter( data, img_np):
        count_valf = 0
        # Display frame with object count
        for result in data:
            for box in result.boxes:
                confidence = box.conf[0]
                if confidence > 0.5:
                    count_valf += 1   
                    x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy()) 
                    cv2.rectangle(img_np, (x1, y1), (x2, y2), (0, 0, 255), 1)
        cv2.imwrite("D:/Prod/Valf_Analitik/img.png", img_np)
        return count_valf
