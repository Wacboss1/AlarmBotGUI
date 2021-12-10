import socket
from matplotlib.collections import PathCollection
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from FoundObject import FoundObject

IP = '192.168.1.1'
port = 288

def SendCommand(response):
    if(responce == "mf"):
        amount = int(input("How far?\n"))
        MoveForward(amount)
    if(responce == 'mb'):
        amount = int(input("How far?\n"))
        MoveBackward(amount)
    elif(responce == 's'):
        try:
            objectsSeen = GetObjectsFromScan()
            df = CreateDataFrame(objectsSeen)
            CreateGraph(df)
        except KeyError:
            print("No objects fmound")
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
            WaitForStopBit(s)

def CreateGraph(dataFrame):
    angles = dataFrame[['angle']].apply(np.deg2rad)
    distances = dataFrame[['distance']]
    colors = dataFrame['color']
    widths = 10 * dataFrame['width']

    plot = plt.subplot(111, polar=True)
    ticks = np.arange(0, 50, 5)
    plot.set_ylim(0, 50)
    plot.set_yticks(ticks)
    plot.set_thetamin(0)
    plot.set_thetamax(180)
    plt.scatter(angles, distances, c=colors, s=widths)
    plt.show()

def CreateDataFrame(objectsSeen):
    df = pd.DataFrame.from_records([o.toDict() for o in objectsSeen])
    print(df.head())
    return df

def GetObjectsFromScan():
    objects = []
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((IP, port))
        s.send(b'y')
        while True:
            reply = s.recv(8)
            if(reply[0] == 2):
                newObject = FoundObject(reply[1], reply[3], reply[2])
                objects.append(newObject)
            elif(reply[0] == 0):
                break
    return objects

def ProccessTriggers(packet):
    if packet[1] == 16:
        print("left bumper hit")
    elif packet[1] == 32:
        print("right bumper hit")
    
    if packet[2] != 0:
        print("cliff dectected")
    
    if packet[3] == 1:
        print("boundary dectected")
    
def MoveForward(amount):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((IP, port))
        s.send(b'W')
        WaitForStopBit(s)
        s.send(amount.to_bytes(1, 'little'))
        while True:
            reply = s.recv(8)
            if (reply[0]==3):
                ProccessTriggers(reply)
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
            if(reply[0] == 0):
                break

def WaitForStopBit(socket):
    while True:
        reply = socket.recv(8)
        if(reply[0] == 0):
            return True

def MoveBackward(amount):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((IP, port))
        s.send(b'B')
        WaitForStopBit(s)
        s.send(amount.to_bytes(1, 'little'))

while True:
    responce = input("use a command\n")
    SendCommand(responce)
