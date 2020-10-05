import time
import sys
import socket
import threading
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

host = "127.0.0.1" #set to server ip or hostname
port = 4098

timeout = 2

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientSocket.settimeout(timeout)

#msg, server = clientSocket.recvfrom(2048)

data = {}

x = []
y = []

def sender():
    i = 1
    while True:
        message = str.encode(str(i))
        time.sleep(0.01)
        data[str(i)] = time.time()
        clientSocket.sendto(message, (host, port))
        i += 1

def receiver():
    while True:
        message, server = clientSocket.recvfrom(2048)
        message = message.decode()
        if message in data:
            # print((message, time.time() - data[message]))
            x.append(int(message))
            elapsed = time.time() - data[message]
            y.append(elapsed)
            data.pop(message)
        else:
            print("unknown sequence number %s" % (message))

t = threading.Thread(target=sender)
t.start()

t2 = threading.Thread(target=receiver)
t2.start()

GRAPH_WIDTH = 500

fig, ax = plt.subplots()
line, = ax.plot([],[])
ax.grid()

def init():
    ax.set_ylim(0,0.025)
    ax.set_xlim(1, GRAPH_WIDTH)
    line.set_data(x, y)
    return line,

def animate(i):
    line.set_data(np.array(x), np.array(y))
    current = max(GRAPH_WIDTH, len(y))
    ax.set_xlim(current - GRAPH_WIDTH + 1, current)
    return line,

anim = animation.FuncAnimation(fig, animate, interval=10, init_func=init)

plt.show()

