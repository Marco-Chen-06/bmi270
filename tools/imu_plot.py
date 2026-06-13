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
for i in range (7):
    channels.append(deque([0] * WINDOW_WIDTH, maxlen=WINDOW_WIDTH))

def update(frame):
    while ser.in_waiting:
        raw_data = ser.readline()
        try:
            decoded_data = raw_data.decode("ascii").strip().split(",")
            if len(decoded_data) != 7:
                continue
            sample = [int(p) for p in decoded_data]
        except (UnicodeDecodeError, ValueError):
            continue
        for i in range(7):
            channels[i].append(sample[i])
    return []

# 0, 1, 2 return 0 (represents left plot). 3, 4, 5 return 1 (right plot). 6 returns 0 (edge case for acc_mag)
def axis_helper(i):
    # handle the acc_mag case
    if i == 6:
        return 0
    return i // 3 


# create 6 subplots with the same x axes
fig, ax = plt.subplots(1, 2, sharex=True)

labels = ["acc_x", "acc_y", "acc_z", "gyr_x", "gyr_y", "gyr_z", "acc_mag"]
lines = []
for i in range(7):
    a = axis_helper(i)
    lines.append(ax[a].plot(range(WINDOW_WIDTH), channels[i], label=labels[i])[0])

ax[0].set_title("acceleration")
ax[1].set_title("gyroscope")
ax[0].legend(loc="upper right")
ax[1].legend(loc="upper right")

def update_plot(frame):
    update(frame)
    for i in range(7):
        a = axis_helper(i)
        lines[i].set_ydata(channels[i])
        ax[a].relim();
        ax[a].autoscale_view(scalex=False)
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