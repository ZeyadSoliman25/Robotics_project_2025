import cv2
from cvzone.HandTrackingModule import HandDetector
import SignLanguageModel as SLM
from tkinter import *
import threading
import Uarm
import time

class App:
    def __init__(self):
        self.x = 10
        self.y = 10
        self.z = 10
        self.offset = 1

        ADDRESS = "https://192.168.45.146:4747/video" # IP address of the phone webcam (from DroidCam)
        self.cap = cv2.VideoCapture(0) # Initialize the video capture object from OpenCv
        #self.cap.open(ADDRESS) # Connect to the phone webcam 
        #self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Reduce frame buffer size

        self.detector = HandDetector(maxHands=1) # Initialize Hand-detector object

        # Initialize PredictSign class
        self.sign_predictor = SLM.PredictSign()
        self.last_prediction = 0

        # Initialize variables to store hands and frame objects
        self.hands = 0
        self.frame = 0

        self.client_id, self.object_handle, self.gripper_handle, self.joint_handles, self.servo_base, self.servo_shoulder, self.servo_elbow = Uarm.StartConnection()
        self.servo_base.write(90)
        self.servo_shoulder.write(95)
        self.servo_elbow.write(90)

        # Start video feed and prediction in separate threads
        self.video_thread = threading.Thread(target=self.show_video_feed)
        self.video_thread.daemon = True
        self.video_thread.start()

        self.update_prediction()

    def show_video_feed(self):
        while True:
            # Capture the frame from OpenCV
            success, self.frame = self.cap.read()
            self.hands, self.frame = self.detector.findHands(self.frame)

            # Show the frame using OpenCV (in a separate window)
            if self.frame is not None:
                cv2.imshow("Video Feed", self.frame)

            # Wait for key press (to close OpenCV window) and update every 10ms
            cv2.waitKey(1)
    
    def update_prediction(self):
        prediction = self.sign_predictor.predict_frame(img=self.frame, hands=self.hands)
        if prediction:

            if prediction == 'A':
                print(prediction)
                if (self.x < 25):
                    angles = Uarm.Move_XYZ(client_id=self.client_id, object_handle=self.object_handle, joint_handles=self.joint_handles, x=self.x+self.offset, y=self.y, z=self.z)
                    self.x += self.offset
                elif (self > 10):
                    angles = Uarm.Move_XYZ(client_id=self.client_id, object_handle=self.object_handle, joint_handles=self.joint_handles, x=self.x-self.offset, y=self.y, z=self.z)
                    self.x -= self.offset

                self.servo_base.write(angles[0])

                angle_shoulder = angles[2] + 60
                angle_elbow = angles[1] - 24

                if (angle_shoulder > 173):
                    self.servo_shoulder.write(173)
                    self.servo_shoulder_pos = 173
                elif (angle_shoulder < 95):
                    self.servo_shoulder.write(95)
                    self.servo_shoulder_pos = 95
                else:
                    self.servo_shoulder.write(angle_shoulder)
                    self.servo_shoulder_pos = angle_shoulder
                
                if (angle_elbow > 130):
                    self.servo_elbow.write(130)
                    self.servo_elbow_pos = 130
                elif (angle_elbow < 30):
                    self.servo_elbow.write(30)
                    self.servo_elbow_pos = 30
                else:
                    self.servo_elbow.write(angle_elbow)
                    self.servo_elbow_pos = angle_elbow

                time.sleep(1)
    
            elif prediction == 'B':
                print(prediction)

                if (self.y < 20):
                    angles = Uarm.Move_XYZ(client_id=self.client_id, object_handle=self.object_handle, joint_handles=self.joint_handles, x=self.x, y=self.y+self.offset, z=self.z)
                    self.y += self.offset
                elif (self.y > 10):
                    angles = Uarm.Move_XYZ(client_id=self.client_id, object_handle=self.object_handle, joint_handles=self.joint_handles, x=self.x, y=self.y-self.offset, z=self.z)
                    self.y -= self.offset
                
                self.servo_base.write(angles[0])

                angle_shoulder = angles[2] + 60
                angle_elbow = angles[1] - 24

                if (angle_shoulder > 173):
                    self.servo_shoulder.write(173)
                    self.servo_shoulder_pos = 173
                elif (angle_shoulder < 95):
                    self.servo_shoulder.write(95)
                    self.servo_shoulder_pos = 95
                else:
                    self.servo_shoulder.write(angle_shoulder)
                    self.servo_shoulder_pos = angle_shoulder
                
                if (angle_elbow > 130):
                    self.servo_elbow.write(130)
                    self.servo_elbow_pos = 130
                elif (angle_elbow < 30):
                    self.servo_elbow.write(30)
                    self.servo_elbow_pos = 30
                else:
                    self.servo_elbow.write(angle_elbow)
                    self.servo_elbow_pos = angle_elbow

                time.sleep(1)
            
            elif prediction == 'c':
                print(prediction)

                if (self.z < 25):
                    angles = Uarm.Move_XYZ(client_id=self.client_id, object_handle=self.object_handle, joint_handles=self.joint_handles, x=self.x, y=self.y, z=self.z+self.offset)
                    self.z += self.offset
                elif (self.z > 10):
                    angles = Uarm.Move_XYZ(client_id=self.client_id, object_handle=self.object_handle, joint_handles=self.joint_handles, x=self.x, y=self.y, z=self.z-self.offset)
                    self.z -= self.offset
                
                self.servo_base.write(angles[0])

                angle_shoulder = angles[2] + 60
                angle_elbow = angles[1] - 24

                if (angle_shoulder > 173):
                    self.servo_shoulder.write(173)
                    self.servo_shoulder_pos = 173
                elif (angle_shoulder < 95):
                    self.servo_shoulder.write(95)
                    self.servo_shoulder_pos = 95
                else:
                    self.servo_shoulder.write(angle_shoulder)
                    self.servo_shoulder_pos = angle_shoulder
                
                if (angle_elbow > 130):
                    self.servo_elbow.write(130)
                    self.servo_elbow_pos = 130
                elif (angle_elbow < 30):
                    self.servo_elbow.write(30)
                    self.servo_elbow_pos = 30
                else:
                    self.servo_elbow.write(angle_elbow)
                    self.servo_elbow_pos = angle_elbow

                time.sleep(1)


    def close_app(self):
        # Release resources and close the app
        self.cap.release()
        cv2.destroyAllWindows()
        Uarm.EndConnection(client_id=self.client_id)

   
if __name__ == "__main__":
    root = Tk()
    app = App()
    
    while True:
        app.update_prediction()
        time.sleep(1)