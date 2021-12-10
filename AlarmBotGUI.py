import socket
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from FoundObject import FoundObject

IP = '192.168.1.1'
port = 288

def CreateGraph(dataFrame):
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

def CreateDataFrame(objectsSeen):
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

def moveForward(amount):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((IP, port))
        s.send(b'W')
        WaitForStopBit(s)
        s.send(amount.to_bytes(1, 'little'))
        while True:
            reply = s.recv(8)
            print(reply)
            if(reply[0] == 0):
                break
            elif(reply[0] == 3):
                break

def RotateRight(amount):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((IP, port))
        s.send(b'T') 
        WaitForStopBit(s)
        s.send(amount.to_bytes(1, 'little'))
        while True:
            reply = s.recv(8)
            print(reply)
            if(reply[0] == 0):
                break

def RotateLeft(amount):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((IP, port))
        s.send(b'R')
        WaitForStopBit(s)
        s.send(amount.to_bytes(1, 'little'))
        while True:
            reply = s.recv(8)
            print(reply)
            if(reply[0] == 0):
                break

def WaitForStopBit(socket):
    while True:
        reply = socket.recv(8)
        print(reply)
        if(reply[0] == 0):
            return True

while True:
    responce = input("use a command\n")
    if(responce == "m"):
        amount = int(input("How far?\n"))
        moveForward(amount)
    elif(responce == 's'):
        objectsSeen = GetObjectsFromScan()
        df = CreateDataFrame(objectsSeen)
        CreateGraph(df)
    elif(responce == 'rr'):
        amount = int(input("How far?\n"))
        RotateRight(amount)
    elif(responce == 'rl'):
        amount = int(input("How far?\n"))
        RotateLeft(amount)
    else:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((IP, port))
            s.send(bytes(responce, 'utf-8'))
            reply = s.recv(8)
            print(reply)
            WaitForStopBit(s)
