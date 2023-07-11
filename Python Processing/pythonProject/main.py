import serial.tools.list_ports
import configModules
import time

# Print out active COM ports
ports = serial.tools.list_ports.comports()
for port in ports:
    print(port)

# Ask user to input COM port number
print("Please enter port number:")
portNumber = input(">")
portNumber = 'COM' + portNumber

# Establish serial connection. When opened, arduino resets. Arduino will send
# a message when its serial is ready, so python listens for this message
serialInst = serial.Serial(port=portNumber, baudrate=115200)
print("Connecting...")
connected = False
while not connected:
    if serialInst.in_waiting:
        rawLine = serialInst.readline().strip().decode()
        if rawLine == "SR":       # Arduino sends "Serial Ready" when serial is ready
            connected = True
            print('Connected!')


platform_selection = "GHK AKS-74U"
propellant_selection = "CO2"
validExperiment = False
while not validExperiment:
    if configModules.select_mode() == 'Experiment Configuration':
        mass_selection = configModules.select_mass()
        interval_selection = configModules.select_interval()
        print("\nExperiment Summary:")
        print("- " + str(platform_selection))
        print("- " + str(propellant_selection))
        print("- " + str(mass_selection) + "g")
        print("- " + str(interval_selection) + "ms")
        print("\nConfirm experiment and upload? y/n")
        try:
            if input(">") == 'y':
                validExperiment = True
        except ValueError:
            validExperiment = False
    else:
        print("Not finished")

send_config = ("CR" + "S" + str(interval_selection) + "I")
print(send_config)
serialInst.write(send_config.encode('utf-8'))
print("Configuration Uploading. . .")
config_uploaded = False
while not config_uploaded:
    if serialInst.in_waiting:  # 1 or more characters in the input buffer
        rawLine = serialInst.readline().strip().decode()
        if rawLine == "CU":
            config_uploaded = True
            print("Configuration Uploaded")

print("\nEnsure platform is unloaded, then press 1 to begin calibration")
input(">")
print("\nCalibrating...")
send_calibration = str("BC")
serialInst.write(send_calibration.encode('utf-8'))
calibration_completed = False
while not calibration_completed:
    if serialInst.in_waiting:  # 1 or more characters in the input buffer
        rawLine = serialInst.readline().strip().decode()
        if rawLine == "CC":
            calibration_completed = True
            print("Calibration Complete")

while True:
    if serialInst.in_waiting:
        rawLine = serialInst.readline().strip().decode()
        print("Calibration Offset: " + str(rawLine))
