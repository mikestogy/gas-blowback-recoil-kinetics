import serial.tools.list_ports
import configModules
import time

ports = serial.tools.list_ports.comports()
for port in ports:
    print(port)

print("Please enter port number:")
portNumber = input(">")
portNumber = 'COM' + portNumber

# Arduino serial takes marginally longer to begin, rather than
# implementing delays, wait for arduino to tell python its ready
serialInst = serial.Serial(port=portNumber, baudrate=115200)
print("Connecting . . .")
connected = False
while not connected:
    if serialInst.in_waiting:
        rawLine = serialInst.readline().strip().decode()
        if rawLine == "Serial Ready":       # Arduino sends "Serial Ready" when serial is ready
            connected = True
            print('Connected to Arduino!')


mass_selection = "NA"
propellant_selection = "NA"
platform_selection = "NA"
validExperiment = False
while not validExperiment:
    #if configModules.select_mode() == 'Experiment Configuration':
     #   platform_selection = configModules.select_platform()
      #  propellant_selection = configModules.select_propellant()
       # mass_selection = configModules.select_mass()
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
    #else:
     #   print("not configured, please try another")

experiment = str(interval_selection)
serialInst.write(experiment.encode('utf-8'))
print("Uploading experiment. . .")

experiment_uploaded = False
while not experiment_uploaded:
    if serialInst.in_waiting:  # 1 or more characters in the input buffer
        rawLine = serialInst.readline().strip().decode()
        if rawLine == "Experiment Received":
            experiment_uploaded = True

print("Experiment uploaded to Arduino!")








'''print("\nSending experiment . . .")
time.sleep(2)
print("Experiment loaded")

print("\nWARNING - To calibrate, ensure platform is unloaded. Then, press 1.")
input(">")

print("\nCalibrating platform . . .")
time.sleep(2)
print("Calibration complete. Current offset:")

print("WARNING - To continue, arm the platform. Then, press 1.")
input(">")

print("WARNING - Press 1 to initiate experiment.")
input(">")'''



