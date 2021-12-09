import socket
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from FoundObject import FoundObject

IP = '192.168.1.1'
port = 288

testAngles = np.deg2rad(np.array([90, 30]))
testValues = np.array([20, 25])

def CreateGraph():
    dataFrame = CreateDataFrame()
    angles = dataFrame[['angle']].apply(np.deg2rad)
    distances = dataFrame[['distance']]
    colors = dataFrame['color']

    plot = plt.subplot(111, polar=True)
    ticks = np.arange(0, 50, 5)
    plot.set_ylim(0, 50)
    plot.set_yticks(ticks)
    plot.set_thetamin(0)
    plot.set_thetamax(180)
    plt.scatter(angles, distances, c=colors)
    plt.show()

def CreateDataFrame():
    objectsSeen = GetObjectsFromScan()
    df = pd.DataFrame.from_records([o.toDict() for o in objectsSeen])
    print(df.head())
    return df

def GetObjectsFromScan():
    #TODO get the objects from the robot
    objects = []
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((IP, port))
        s.send(b'y')
        while True:
            reply = s.recv(8)
            print(reply)
            if(reply[0] == 2):
                newObject = FoundObject(reply[1], reply[3], reply[2])
                objects.append(newObject)
            elif(reply[0] == 0):
                break
    return objects

def moveForward():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((IP, port))
        s.send(b'w')
        while True:
            reply = s.recv(8)
            print(reply)
            if(reply[0] == 0):
                break

CreateGraph()

