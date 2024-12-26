import sim
import time
import numpy as np
import matplotlib.pyplot as plt
import math
from pyfirmata import Arduino



def StartConnection():
    # Initialize Arduino servo pins 
    board = Arduino('com4')  # Current Arduino port
    servo_base = board.get_pin('d:10:s')  # Servo base on pin 10
    servo_shoulder = board.get_pin('d:9:s')  # Servo shoulder on pin 9
    servo_elbow = board.get_pin('d:3:s')  # Servo elbow on pin 3


    # Connect to CoppeliaSim
    sim.simxFinish(-1)  # Close all opened connections
    client_id = sim.simxStart('127.0.0.1', 19997, True, True, 5000, 5)

    if client_id != -1:
        print("Connected to CoppeliaSim")

        # Set up handles
        _, object_handle = sim.simxGetObjectHandle(client_id, 'Target', sim.simx_opmode_blocking)
        _, gripper_handle = sim.simxGetObjectHandle(client_id, 'uarmGripper', sim.simx_opmode_blocking)
        
        joint_handles = []
        for i in range(1, 4):  # Assuming a 6-DOF robot
            _, joint_handle = sim.simxGetObjectHandle(client_id, f'M_Joint{i}', sim.simx_opmode_blocking)
            joint_handles.append(joint_handle)
        
        # Initialize streaming
        _, initial_pos = sim.simxGetObjectPosition(client_id, object_handle, -1, sim.simx_opmode_streaming)
        sim.simxGetObjectPosition(client_id, gripper_handle, -1, sim.simx_opmode_streaming)
        for handle in joint_handles:
            sim.simxGetJointPosition(client_id, handle, sim.simx_opmode_streaming)

        return client_id, object_handle, gripper_handle, joint_handles, servo_base, servo_shoulder, servo_elbow
    else:
        print("Failed to connect to CoppeliaSim")


def EndConnection(client_id):
    # Disconnect
    sim.simxFinish(client_id)
    print("Simulation stopped and connection closed.")


    

def Move_XYZ(client_id, object_handle, joint_handles, x, y, z):
    sim.simxSetObjectPosition(client_id, object_handle, -1, [x/100, y/100, z/100], sim.simx_opmode_oneshot)
    #time.sleep(2)  # Allow time for motion

    # Get joint angles
    angles = []
    for handle in joint_handles:
        _, angle = sim.simxGetJointPosition(client_id, handle, sim.simx_opmode_buffer)
        angles.append(math.degrees(angle))
    
    return angles


def moveJoint(servo, pos, current_pos):
    if (((pos - current_pos) > 10) or ((pos - current_pos)  < -10)): 
        servo_angle_offset = math.ceil((pos - current_pos) / 5)

        for i in range(0,5):
            current_pos += servo_angle_offset
            servo.write(current_pos)
    
    else: 
        servo.write(pos)


        


