import numpy
import cv2
import socket
import pyaudio
import threading
from threading import Thread

#Video Socket
s = socket.socket()
port = 3000
s.connect(('196.140.181.0', port))

#Audio
chunk = 1024
p = pyaudio.PyAudio()

stream = p.open(format = pyaudio.paInt16,
                channels = 1,
                rate = 44100,
                output = True)

#Audio Socket Initialization
audioSocket = socket.socket()
port1 = 5000
size = 1024
audioSocket.connect(('196.140.181.0',port1))

def rcvAudio():
     while True:
          audioData = audioSocket.recv(size)
          stream.write(audioData)


def rcvVideo():
     while True:
          data, addr = s.recvfrom(230400)
          frames = ""
          frames += data
          if len(frames) == (230400):

              frame = numpy.fromstring (frames,dtype=numpy.uint8)
              frame = frame.reshape (240,320,3)
              cv2.imshow('frame',frame)
              frames=""
              cv2.waitKey(1)
          else:
              frames=""

Thread(target = rcvVideo).start()
Thread(target = rcvAudio).start()

#stream.close()
#p.terminate()
