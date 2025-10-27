"""
arduino weather station data logger and live plotter.
Reads temperature and humidity data from an Arduino over serial,
logs it to a CSV file on the desktop, and displays a live-updating plot.
"""

import serial
import time
import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

arduino = serial.Serial('COM5', 9600, timeout=1)
time.sleep(2)  


desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
filename = os.path.join(desktop_path, "weather_log.csv")
print("CSV will be saved to:", filename)

file_exists = os.path.isfile(filename)
csvfile = open(filename, "a", newline="")
csvwriter = csv.writer(csvfile)

if not file_exists:
    csvwriter.writerow(["Timestamp", "Temperature(°C)", "Humidity(%)"])
temps = []
hums = []
timestamps = []
plt.style.use("ggplot")  
fig, ax = plt.subplots()
ax.set_xlabel("Readings")
ax.set_ylabel("Value")
ax.set_title("Live Weather Data")
line1, = ax.plot([], [], label="Temperature (°C)")
line2, = ax.plot([], [], label="Humidity (%)")
ax.legend()

def animate(i):
    try:
        line = arduino.readline().decode('utf-8').strip()
        if line:
            temp_str, hum_str = line.split(",")
            temp = float(temp_str)
            hum = float(hum_str)
            timestamp = datetime.now().strftime("%H:%M:%S")

            temps.append(temp)
            hums.append(hum)
            timestamps.append(timestamp)

            # Log to CSV
            csvwriter.writerow([timestamp, temp, hum])
            csvfile.flush()

            # Update plot
            line1.set_data(range(len(temps)), temps)
            line2.set_data(range(len(hums)), hums)
            ax.relim()
            ax.autoscale_view()
            ax.set_xticks(range(len(timestamps)))
            ax.set_xticklabels(timestamps, rotation=45, ha='right')
    except Exception as e:
        print("Error:", e)

ani = FuncAnimation(fig, animate, interval=2000)
plt.show()
