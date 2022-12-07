# Program to control passerelle between Android application
# and micro-controller through USB tty
import json
import os
import re
import threading
import serial
import time
import multiprocessing as mp
import hashlib


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


def verifHash(message,hash):
    result = hashlib.md5(message)
    return result.digest() == hash

def verifKey(key):
    keyVerif = "TTBM"
    return key == keyVerif.encode()

def traiterRequete(req):
    taille = int.from_bytes([req[-1]],"big")
    print("verif calc : " + str(verifHash(req[0:taille],req[-17:-1])))
    print("verif key : " + str(verifKey(req[0:4])))

    #verifHash(req[taille:],req[-13:-2])

def sendUARTMessage(msg):
    ser.write(msg)
    print("Message <" +'{:10}'.format(str(msg))+ ">----Send to micro-controller.")
    

def readUARTMessage(ser):
    while True:
        t = ser.read(32)
        print("Message <" +'{:10}'.format(str(t  ))+ ">--------Read to micro-controller.")
        traiterRequete(t)

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
        time.sleep(5)
        #sendUARTMessage(bytes("OKG\n", 'utf-8'))
        

        
