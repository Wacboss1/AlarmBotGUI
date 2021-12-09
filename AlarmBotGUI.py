import socket
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

IP = '192.168.1.1'
port = 288
speed = 115200
bits = 8

testAngles = np.deg2rad(np.array([90, 30]))
testValues = np.array([20, 25])

def CreateGraph(angles, distances):
    plot = plt.subplot(111, polar=True)
    ticks = np.arange(0, 50, 5)
    plot.set_ylim(0, 50)
    plot.set_yticks(ticks)
    plot.set_thetamin(0)
    plot.set_thetamax(180)
    plt.scatter(angles, distances)
    plt.show()

def CreateDataFrame():

    return 0

def GetObjectsFromScan():
    #TODO get the objects from the robot
    return 0

CreateGraph(testAngles, testValues)
# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.connect((IP, port))
#     s.send(b'h')
#     while 1:
#         reply = s.recv(4096)
#         print(reply)

