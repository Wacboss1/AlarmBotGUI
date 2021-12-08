import socket
import math
import tkinter
import time

IP = '192.168.1.1'
port = 288
speed = 115200
bits = 8

window = tkinter.Tk()
window.title("AlarmBot UI")
window.geometry(f'1500x1500')

canvas = tkinter.Canvas(window)
canvas.configure(bg="blue")
canvas.pack(fill="both", expand=True)
window.mainloop()

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.connect((IP, port))
#     s.send(b'h')
#     while 1:
#         reply = s.recv(4096)
#         print(reply)

