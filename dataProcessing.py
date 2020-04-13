#Some imports
import serial
import matplotlib.pyplot as plt
import time
import sys

#Function that takes string type UTF-8 encoded serial plotting and return a list of floats
def preProcessData(incomingDatum):
    incomingDatum = incomingDatum.decode('utf-8')
    incomingDatum = incomingDatum.strip('\n')
    incomingDatum = incomingDatum[6:] #6 is unique to this situation. It might not be necessary at all.

    #splits incoming values at the comma, packs into a list
    incomingDatum = incomingDatum.split(',')
    return incomingDatum

#Accepts user input for the serial port as well as the test duration
comPort = str(input("Please enter the V5 User port to be used:    "))
testLen = float(input("Please enter the duration of collection:     "))

#This block of code handles the chance of no data stream being supplied by user on specified port. 
exceptionCounter = 0
while (1):
    #Attempts to find data stream from serial port. 
    try:
        dataStream = serial.Serial(comPort, baudrate = 115200,timeout = 1) #Set to maximum baud for pReCIsIoN.
        print("Data Stream Found. Starting collection with user input end time.")
        break

    #Error handling in the chance of no serial link found
    except:
        if (exceptionCounter > 7):
            print("Timed out while waiting for data on "+comPort+". Program Ending.")
            sys.exit()
        print("No data stream found on "+comPort+". Re-trying In 2 seconds.")
        time.sleep(2)
        exceptionCounter+=1

#Empty list to hold data
fullDataSet = []
xAxis = []

#Failure variable for looping
lineDropCount = 0

#timed run counter
startTime = time.time()

#main loop
while(time.time() - startTime < testLen):

    #Runs if data is available
    if (dataStream.is_open):

        #unpacks and decodes serial lines
        incomingDatum = preProcessData(dataStream.readline())

        #Convert list of strings into a list of float
        for stringDatumIndex in range(len(incomingDatum)):
            incomingDatum[stringDatumIndex] = float(incomingDatum[stringDatumIndex])
                
        xAxis.append(incomingDatum[0]) #Apppend the x-series value to our x-list
        incomingDatum.pop(0) #Delete x-series value from the datum list
        fullDataSet.append(incomingDatum) #append the n-series' of single element list to full set

print("Plotting")

#Using matplotlib pyplot to create graphic
plt.figure(1)
plt.plot(xAxis, fullDataSet)
plt.show()