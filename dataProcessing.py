import serial
import matplotlib.pyplot as plt

dataStream = serial.Serial('COM12', baudrate = 115200,timeout = 1)

while(1):
    if (dataStream.is_open):
        incomingDatum = dataStream.readline()
        incomingDatum = incomingDatum.decode('utf-8')
        incomingDatum = incomingDatum.strip('\n')
        incomingDatum = incomingDatum[6:]
        incomingDatum = float(incomingDatum)
        print(incomingDatum)