import serial.tools.list_ports
import numpy as np
import matplotlib.pyplot as plt
import time

ports = serial.tools.list_ports.comports()
print("Available COM ports:")
for port in ports:
    print(port)

connected = False
while not connected:
    try:
        portName = input("Enter COM port number: ")
        portName = "COM" + portName
        ports = serial.tools.list_ports.comports()
        serialInst = serial.Serial(port=portName, baudrate=115200)
        print("Connected to COM 3 succesfully.")
        connected = True
    except serial.SerialException:
        print("Error: Invalid COM Selection")
        connected = False

print("Configure experimental setup:")
print("Select propellant")
propellantList = ["Propane", "Propylene", "CO2"]


for index, propellant in enumerate(propellantList):
    print(f"{index}. {propellant}")

propSelected = False
while not propSelected:
    try:
        propSelection = int(input("Enter propellant selection: "))
        propSelection = propellantList[int(propSelection)]
        propSelected = True
    except ValueError:
        propSelected = False
    except IndexError:
        propSelected = False

massSelected = False
while not massSelected:
    try:
        massSelection = int(input("Enter mass of gas being tested: "))
        if 0 < massSelection < 50:
            massSelected = True
    except ValueError:
        propSelected = False
    except IndexError:
        propSelected = False

input()

# Clear buffer
time.sleep(1)
serialInst.read_all()

command = input("Press 1 to begin experiment configuration: ")
serialInst.write(command.encode('utf-8'))

collecting = True

rawLineList = []
counter = 0
# Accepts data while argument is true
print("Collecting...")
while counter < 1000:
    if serialInst.in_waiting:  # 1 or more characters in the input buffer
        rawLine = serialInst.readline()  # Reads one line of data as 'bytes'
        rawLineList.append(rawLine)  # Adds line to list
        counter += 1
print("Finished")
serialInst.close()

# Converts each value in rawLineList to usable/desired format into a new list of lists
cleanLineList = []
for x in range(len(rawLineList)):
    cleanLine = rawLineList[x]  # Take the first line, or 'bytes', from rawLineList
    cleanLine = cleanLine.decode().split()  # Decode and split the bytes of ASCII characters into a list of strings
    for j in range(len(cleanLine)):
        cleanLine[j] = float(cleanLine[j])  # Converts all string elements of list to float
    cleanLineList.append(cleanLine)  # Adds line to list

# Convert cleanLineList to a numpy array called dataArray
dataArray = np.array(cleanLineList)

# X values represent time in microseconds
x = dataArray[:, 0]
timeZero = x[0]
for i in range(len(x)):
    x[i] = x[i] - timeZero  # Zero out the time to the first data point
    x[i] = x[i] / 1000  # Convert to milliseconds

xDelta = []

for i in range((len(x)) - 1):
    xDelta.append(x[i + 1] - x[i])

# Y values represent the converted differential voltage
y = dataArray[:, 1]
# Converted differential ADC value, or Y, is equal to (resolution/FSR) * V_in
# Solving for V_in, divide Y by (resolution/FSR)
for i in range(len(y)):
    y[i] = float(y[i])
    y[i] = y[i] * ((2 * 0.256) / 65536)  # This is the raw differential voltage
    y[i] = y[i] * (1 / 0.001) * (5 / 5)  # Convert to kg
    y[i] = y[i] * 9.81  # Newtons of force

impulse = 0
for i in range(len(xDelta)):
    impulse += xDelta[i] * y[i]

print(impulse)

# Make the plot
plt.figure(figsize=(14, 8), facecolor='lightgray')
plt.grid(True, color='gray', linestyle='--', linewidth=0.25)
plt.xticks(np.arange(min(x), max(x) + 1, 50))
plt.yticks(np.arange(0, max(y) + 1, 2))
plt.xlabel("Time (ms)")
plt.ylabel("Force (N)")
plt.title("Impulse")
ax = plt.gca()
ax.set_facecolor("darkgray")

plt.scatter(x, y)
plt.show()
