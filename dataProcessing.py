import serial
import matplotlib.pyplot as plt
import time
import sys

#Accepts user input for the serial port as well as the test duration
comPort = str(input("Please enter the V5 User port to be used:    "))
testLen = float(input("Please enter the duration of collection:     "))

#This block of code handles the chance of no data stream being supplied by user on specified port. 
exceptionCounter = 0
while (1):
    #Attempts to find data stream from serial port. 
    try:
        #Baudrate should be specified better
        dataStream = serial.Serial(comPort, baudrate = 9600,timeout = 1)
        print("Data Stream Found. Starting collection with user input end time.")

    #Error handling in the chance of no serial link found
    except:
        if (exceptionCounter > 7):
            print("Timed out while waiting for data on "+comPort+". Program Ending.")
            sys.exit()
        print("No data stream found on "+comPort+". Re-trying In 2 seconds.")
        time.sleep(2)
        exceptionCounter+=1

#Empty lists to hold data
distances = []
commandVelocity = []
actualVelocity = []

#Failure variable for looping
lineDropCount = 0


#timed run
startTime = time.time()
#Starting loop with 5.0 second time condition
while(time.time() - startTime < 6.0):
    #Runs if data is available
    if (dataStream.is_open):
        #unpacks and decodes serial lines
        incomingDatum = dataStream.readline()
        incomingDatum = incomingDatum.decode('utf-8')
        incomingDatum = incomingDatum.strip('\n')
        incomingDatum = incomingDatum[6:] #6 is unique to this situation. It might not be necessary at all.
        
        try:
            #splits incoming values at the comma (3 required), packs into a tuple
            (currentDist, currentCommandVel, currentActualVel) = incomingDatum.split(',')

            #Typecast string values into float
            currentDist = float(currentDist)
            currentActualVel = float(currentActualVel)
            currentCommandVel = float(currentCommandVel)

            #Add datum to various lists
            distances.append(currentDist)
            commandVelocity.append(currentCommandVel)
            actualVelocity.append(currentActualVel)

        except:
            if (lineDropCount > 49):
                print("Too many dropped lines. Exiting to Plotting")
                break

            print("Dropped line. Did not receive 3 unpackable values.")
            lineDropCount+=1

print("Plotting")

#Using matplotlib pyplot to create graphic
plt.figure(1)
plt.plot(distances, commandVelocity, color = 'blue')
plt.plot(distances,actualVelocity, color = 'red')
plt.show()