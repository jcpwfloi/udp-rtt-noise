import time
import sys
import socket
import threading
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import animation

host = "167.172.203.146" #set to server ip or hostname
port = 4098

timeout = 2
alpha = 0.2
beta = 0.3

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientSocket.settimeout(timeout)

#msg, server = clientSocket.recvfrom(2048)

data = {}

x = []
y = []
rtoy = []
rto2y = []

def sender():
    i = 1
    while True:
        message = str.encode(str(i))
        time.sleep(0.01)
        data[str(i)] = time.time()
        clientSocket.sendto(message, (host, port))
        i += 1


def receiver():
    avg = 0
    avg2 = 0
    while True:
        try:
            message, server = clientSocket.recvfrom(2048)
        except socket.error:
            print("Timeout occurred")
            continue
        message = message.decode()
        if message in data:
            # print((message, time.time() - data[message]))
            x.append(int(message))
            elapsed = time.time() - data[message]
            y.append(elapsed)
            avg = elapsed if avg == 0 or len(y) < 3 else avg * (1 - alpha) + elapsed * alpha
            avg2 = avg if avg2 == 0 or len(y) < 3 else avg2 * (1 - alpha) + avg * alpha
            rtoy.append(avg)
            rto2y.append(avg2)
            data.pop(message)
        else:
            print("unknown sequence number %s" % (message))

t = threading.Thread(target=sender)
t.start()

t2 = threading.Thread(target=receiver)
t2.start()

GRAPH_WIDTH = 300

fig, ax = plt.subplots()
line, = ax.plot([],[])
rtoline, = ax.plot([],[], color='red')
rto2line, = ax.plot([],[], color='green')
ax.grid()

def init():
    ax.set_ylim(0.07,0.15)
    ax.set_xlim(1, GRAPH_WIDTH)
    line.set_data(x, y)
    return line,

def animate(i):
    line.set_data(x, y)
    rtoline.set_data(x, rtoy)
    rto2line.set_data(x, rto2y)
    current = max(GRAPH_WIDTH, len(y))
    ax.set_xlim(current - GRAPH_WIDTH + 1, current)
    if i % 50 == 0:
        sample = np.array(y[-GRAPH_WIDTH:])
        ax.set_ylim(np.min(sample), np.max(sample))
    return line,

anim = animation.FuncAnimation(fig, animate, interval=10, init_func=init)

plt.show()

