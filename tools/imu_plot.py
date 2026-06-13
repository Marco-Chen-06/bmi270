# imu_plot.py
# real-time serial plotter for imu accelerometer and gyroscope data
#
# expects stm32 to print one line per sample over uart in the following format:
# acc_x,acc_y,acc_z,gyr_x,gyr_y,gyr_z/r/n
#
# uses pyserial and matplotlib

import serial
from collections import deque
import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation

PORT = "/dev/ttyACM0"
BAUDRATE = 115200
WINDOW_WIDTH = 200 # number of samples on screen at a time

ser = serial.Serial(PORT, BAUDRATE, timeout=1)
ser.reset_input_buffer()

channels = []
values = []
for i in range (6):
    channels.append(deque([0] * WINDOW_WIDTH, maxlen=WINDOW_WIDTH))

def update(frame):
    while ser.in_waiting:
        raw_data = ser.readline()
        try:
            decoded_data = raw_data.decode("ascii").strip().split(",")
            if len(decoded_data) != 6:
                continue
            sample = [int(p) for p in decoded_data]
        except (UnicodeDecodeError, ValueError):
            continue
        for i in range(6):
            channels[i].append(sample[i])
    return []


def grid_helper(i):
    row = i % 3
    col = i // 3 # floor division
    return row, col

# create 6 subplots with the same x axes
fig, ax = plt.subplots(3, 2, sharex=True)

lines = []
for i in range(6):
    r, c = grid_helper(i)
    lines.append(ax[r][c].plot(range(WINDOW_WIDTH), channels[i])[0])

labels = ["acc_x", "acc_y", "acc_z", "gyr_x", "gyr_y", "gyr_z"]
for i in range(6):
    r, c = grid_helper(i)
    ax[r][c].set_ylabel(labels[i])



def update_plot(frame):
    update(frame)
    for i in range(6):
        r, c = grid_helper(i)
        lines[i].set_ydata(channels[i])
        ax[r][c].relim();
        ax[r][c].autoscale_view(scalex=False)
    return lines


try:
    anim = FuncAnimation(fig, update_plot, interval=50, cache_frame_data=False)
    plt.show()

except KeyboardInterrupt:
    print("keyboard interrupt detected")

finally:
    if ser.is_open:
        ser.close()
        print("serial port closed")