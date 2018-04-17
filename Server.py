import numpy as np
import cv2
import socket
import time
import pyaudio
import threading
from threading import Thread

#Video
cap = cv2.VideoCapture(0)
cap.set(3,320)
cap.set(4,240)


#Video Socket
s = socket.socket()
host = socket.gethostname()
port = 3000
s.bind((host,port))
s.listen(5)
c, addr = s.accept()


#Audio
chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()

stream = p.open(format = FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = True,
                frames_per_buffer = chunk)

#Audio Socket Initialization
audioSocket = socket.socket()
port1 = 5000
audioSocket.bind((host,port1))
audioSocket.listen(5)
cAudio, addr = audioSocket.accept()

def recordAudio():
    time.sleep(5)
    while True:
        data = stream.read(chunk)
        if data:
            cAudio.sendall(data)

def recordVideo():
    time.sleep(5)    
    while True:
        ret, frame = cap.read()
        d = frame.flatten()
        video = d.tostring()
        c.sendall(video)
        time.sleep(0.2)

print 'Connection accepted from ', addr

Thread(target = recordAudio).start()
Thread(target = recordVideo).start()

#c.close()
