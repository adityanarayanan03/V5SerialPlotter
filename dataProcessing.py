#Some imports
import serial
import matplotlib.pyplot as plt
import time
import sys

#Function that takes string type UTF-8 encoded serial plotting and return a list of floats
def preProcessData(incomingDatum):
    incomingDatum = incomingDatum.decode('utf-8')
    incomingDatum = incomingDatum.strip('\n')

    #In the case that we are receiving steady empty string, then no start and stop characters are found
    try:
        incomingDatum = incomingDatum[incomingDatum.index('{')+len('{'):incomingDatum.index('}')] 
    except:
        #Replace datum with blank string
        incomingDatum = ''
    
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
        print("Serial Connection Found. Waiting for data input.")
        break

    #Error handling in the chance of no serial link found
    except:
        if (exceptionCounter > 7):
            print("Timed out while waiting for data on "+comPort+". Program Ending.")
            sys.exit()
        print("No data stream found on "+comPort+". Re-trying In 2 seconds.")
        time.sleep(2)
        exceptionCounter+=1

#This loop waits for the START Command from V5 Brain
print("Waiting for data stream to start.")
while (1):
    if(preProcessData(dataStream.readline())[0] == 'START'):
        print("Start command received. Starting Collection")
        break



#Empty list to hold data
fullDataSet = []
xAxis = []

#Failure variable for looping
lineDropCount = 0

#main loop
#timed run counter
startTime = time.time()
while(time.time() - startTime < testLen):

    #Runs if data stream has been opened
    if (dataStream.is_open):

        #unpacks and decodes serial lines
        incomingDatum = preProcessData(dataStream.readline())
        print(time.time() - startTime)
        #Convert list of strings into a list of float
        try:
            for stringDatumIndex in range(len(incomingDatum)):
                incomingDatum[stringDatumIndex] = float(incomingDatum[stringDatumIndex])
                        
            xAxis.append(time.time() - startTime) #Apppend the x-series value to our x-list
            incomingDatum.pop(0) #Delete x-series value from the datum list
            fullDataSet.append(incomingDatum) #append the n-series' of single element list to full set
        except:
            print("Something went wrong! Continuing collection.")
            lineDropCount += 1
            if (lineDropCount > 50):
                print("Too many errors. Stopping collection")
                sys.exit()

print("Plotting")

#Using matplotlib pyplot to create graphic
plt.figure(1)
plt.plot(xAxis, fullDataSet)
plt.show()