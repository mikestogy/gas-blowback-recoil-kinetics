import serial.tools.list_ports
import time

ports = serial.tools.list_ports.comports()
for port in ports:
    print(port)

print("Please enter port number:")
portNumber = input(">")
portNumber = 'COM' + portNumber

ser = serial.Serial(port=portNumber, baudrate=115200)
ser.reset_input_buffer()
print("Connecting...")

connected = False
while not connected:
    if ser.in_waiting:
        rawLine = ser.readline().decode().strip()
        if rawLine == "RDY":
            connected = True
            print("Connected")


ser.write(b'RDY2')



while True:
    if ser.in_waiting:
        rawLine = ser.readline().strip().decode()
        print(rawLine)