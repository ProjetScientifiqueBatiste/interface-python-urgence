# Program to control passerelle between Android application
# and micro-controller through USB tty
import json
import os
import re
import threading
import serial
import time
import multiprocessing as mp


HOST = "192.168.1.24"
UDP_PORT = 10000
MICRO_COMMANDS = ["TL", "LT"]

# send serial message
SERIALPORT = "/dev/ttyACM0"
BAUDRATE = 115200
ser = serial.Serial()


def initUART():
    # ser = serial.Serial(SERIALPORT, BAUDRATE)
    ser.port = SERIALPORT
    ser.baudrate = BAUDRATE
    ser.bytesize = serial.EIGHTBITS  # number of bits per bytes
    ser.parity = serial.PARITY_NONE  # set parity check: no parity
    ser.stopbits = serial.STOPBITS_ONE  # number of stop bits
    ser.timeout = None  # block read

    # ser.timeout = 0             #non-block read
    # ser.timeout = 2              #timeout block read
    ser.xonxoff = False  # disable software flow control
    ser.rtscts = False  # disable hardware (RTS/CTS) flow control
    ser.dsrdtr = False  # disable hardware (DSR/DTR) flow control
    # ser.writeTimeout = 0     #timeout for write

    print('Starting Up Serial Monitor')
    try:
        ser.open()
        print('Serial able')
    except serial.SerialException:
        print("Serial {} port not available".format(SERIALPORT))
        exit()


def sendUARTMessage(msg):
    ser.write(msg)
    print("Message <" + str(msg) + "> sent to micro-controller.")

def readUARTMessage(ser):
    while True:
        t = ser.read(7)
        print("Message <" + str(t) + "> sent to micro-controller.")

# Main program logic follows:dmesg | grep tty
if __name__ == '__main__':
    import platform
    if platform.system() == "Darwin" :
        mp.set_start_method('fork') # Nécessaire sous macos, OK pour Linux (voir le fichier des sujets)



    try:
        initUART()

    except:
        pass
    
    idProcess = mp.Process(target=readUARTMessage,args=(ser,))
    idProcess.start()

    while (True) :
        a = 1
        time.sleep(1)
        #sendUARTMessage(bytes("OKGG", 'utf-8'))
        

        
