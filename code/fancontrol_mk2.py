# FanControl Mk 2 - for controlling two fans using a Slice of Relay and two Dalas 18B20 thermometers
# Tim Richardson - June 2016

# Import Libraries
import os                # To load the 1-wire modules
import time              # So we can sleep
import RPi.GPIO as GPIO  # The GPIO library
import threading         # We're using threading - a bit OTT for this, but why not!

# Initialize the GPIO Pins for 1-Wire
os.system('modprobe w1-gpio')  # Turns on the GPIO module
os.system('modprobe w1-therm') # Turns on the Temperature module

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# The location of the 1-Wire device files
W1BaseDir = '/sys/bus/w1/devices/'

# Define the two fan constants
# FanXRelay is the GPIO pin used for the relay
# FanXOnTemp is the thermometer temperature that the fan will turn on at
# FanXW1ThermometerID is the 1-Wire device directory for the thermometer
# FanXW1DeviceFile is the device file that will be read to get the temperature

# Fan 1 - the black one
Fan1Relay = 24
Fan1OnTemp = 25
Fan1W1ThermometerID = '28-0000065d1fa2'
Fan1CheckFrequency = 10

# Fan 2 - the red one
Fan2Relay = 25
Fan2OnTemp = 25
Fan2W1ThermometerID = '28-0004340e0eff'
Fan2CheckFrequency = 10

class FanControl:
    def __init__(self, FanRelay, FanOnTemp, FanW1ThermometerID, FanCheckFrequency):
        self.__FanRelay = FanRelay
        self.__FanOnTemp = Fan1OnTemp
        self.__FanW1DeviceFile = W1BaseDir + FanW1ThermometerID + '/w1_slave'
        GPIO.setup(FanRelay, GPIO.OUT)
        self.FanOff()

        # 'Hello world' - check the fans run
        for x in range(0, 1):
            self.FanOn()
            time.sleep(1)
            self.FanOff()
            time.sleep(1)

    # Monitor the temperature of the thermometer and turn the fan on if it gets too hot
    def FanControlThread(self):
        while (True):
            __tempnow = self.ReadRealTemperature()

            if (__tempnow >= self.__FanOnTemp):
                self.FanOn()
            else:
                self.FanOff()

            time.sleep(10)

    # A function that reads the sensors data
    def ReadRawTemperature(self):
        __W1DeviceFile = open(self.__FanW1DeviceFile, 'r') # Opens the temperature device file
        __lines = __W1DeviceFile.readlines() # Returns the text
        __W1DeviceFile.close()
        return __lines

    # Convert the value of the sensor into a temperature
    def ReadRealTemperature(self):
        __lines = self.ReadRawTemperature() # Read the temperature 'device file'

        # While the first line does not contain 'YES', wait for 0.2s
        # and then read the device file again.
        while __lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            __lines = self.ReadRawTemperature()

        # Look for the position of the '=' in the second line of the
        # device file.
        __equals_pos = __lines[1].find('t=')

        # If the '=' is found, convert the rest of the line after the
        # '=' into degrees Celsius, then degrees Fahrenheit
        if __equals_pos != -1:
            __temp_string = __lines[1][__equals_pos+2:]
            __temp_c = float(__temp_string) / 1000.0
            return __temp_c

    def FanOn(self):
        GPIO.output(self.__FanRelay, GPIO.HIGH)

    def FanOff(self):
        GPIO.output(self.__FanRelay, GPIO.LOW)

# Create instances
Fan1 = FanControl(Fan1Relay, Fan1OnTemp, Fan1W1ThermometerID, Fan1CheckFrequency)
Fan2 = FanControl(Fan2Relay, Fan2OnTemp, Fan2W1ThermometerID, Fan2CheckFrequency)

# Create the threads
Fan1Thread = threading.Thread(target=Fan1.FanControlThread, args=())
Fan2Thread = threading.Thread(target=Fan2.FanControlThread, args=())

# Start the threads
Fan1Thread.start()
Fan2Thread.start()

# Loop forever, or until the keyboard interrupt
while True:
    try:
        time.sleep(60)
    except KeyboardInterrupt:
        print("Bye")
        Fan1.FanOff()
        Fan2.FanOff()
        exit()
