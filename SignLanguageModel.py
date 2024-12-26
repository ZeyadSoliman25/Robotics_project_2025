import cv2
import numpy as np
from cvzone.ClassificationModule import Classifier
import math

IMAGESIZE = 300

offset = 20

class PredictSign:
    def __init__(self):
        """Initilization of the class Predict sign"""
        self.classifier = Classifier("Model/keras_model.h5", "Model/labels.txt")

        self.labels = ['A', 'B', 'C', '1', '2']
        
    def predict_frame(self, img, hands):
        if hands: 
            hand = hands[0]
            x, y, w, h = hand["bbox"]

            imgWhite = np.ones((IMAGESIZE, IMAGESIZE, 3), np.uint8) * 255
            imgCrop = img[y-offset:y+h+offset, x-offset:x+w+offset]

            imgCropShape = imgCrop.shape 

            aspectRatio = h/w

            if aspectRatio > 1:
                k = IMAGESIZE/h
                wCal = math.ceil(k*w)
                imgResize = cv2.resize(imgCrop, (wCal, IMAGESIZE))
                imgResizeShape = imgResize.shape
                wGap = math.ceil((IMAGESIZE - wCal) / 2)
                imgWhite[:, wGap:wCal+wGap] = imgResize
            
            else:
                k = IMAGESIZE/w
                hCal = math.ceil(k*h)
                imgResize = cv2.resize(imgCrop, (IMAGESIZE, hCal))
                imgResizeShape = imgResize.shape
                hGap = math.ceil((IMAGESIZE - hCal) / 2)
                imgWhite[hGap:hCal+hGap, : ] = imgResize
            
            predication, index = self.classifier.getPrediction(imgWhite, draw=False)

            return self.labels[index]

# ADDRESS = "https://192.168.1.19:4343/video" # IP address of the phone webcam (from DroidCam)
# cap = cv2.VideoCapture(0) # Initialize the video capture object from OpenCv
# cap.open(ADDRESS) # Connect to the phone webcam 
# cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Reduce frame buffer size

# detector = HandDetector(maxHands=1) # Initialize Hand-detector object

# classifier = Classifier("Model/keras_model.h5", "Model/labels.txt")

# labels = ['A', 'B', 'C', '1', '2']   

# images_folder = "Data/2"
# images_counter = 0     

# while True: 
#     success, img = cap.read()
#     hands, img = detector.findHands(img)

#     if hands: 
#         hand = hands[0]
#         x, y, w, h = hand["bbox"]

#         imgWhite = np.ones((IMAGESIZE, IMAGESIZE, 3), np.uint8) * 255
#         imgCrop = img[y-offset:y+h+offset, x-offset:x+w+offset]

#         imgCropShape = imgCrop.shape 



#         aspectRatio = h/w

#         if aspectRatio > 1:
#             k = IMAGESIZE/h
#             wCal = math.ceil(k*w)
#             imgResize = cv2.resize(imgCrop, (wCal, IMAGESIZE))
#             imgResizeShape = imgResize.shape
#             wGap = math.ceil((IMAGESIZE - wCal) / 2)
#             imgWhite[:, wGap:wCal+wGap] = imgResize
        
#         else:
#             k = IMAGESIZE/w
#             hCal = math.ceil(k*h)
#             imgResize = cv2.resize(imgCrop, (IMAGESIZE, hCal))
#             imgResizeShape = imgResize.shape
#             hGap = math.ceil((IMAGESIZE - hCal) / 2)
#             imgWhite[hGap:hCal+hGap, : ] = imgResize
        
#         predication, index = classifier.getPrediction(imgWhite, draw=False)

#         print(labels[index])

#         #cv2.imshow("ImageCrop", imgCrop)

#     cv2.imshow("Image", img)
#     cv2.waitKey(1)

    # if key == ord('s'):

    #     if images_counter > 300: # To collect 300 images only
    #         break

    #     images_counter += 1
    #     cv2.imwrite(f"{images_folder}/Image_2_{images_counter}.jpg", imgWhite)
    #     print(images_counter)