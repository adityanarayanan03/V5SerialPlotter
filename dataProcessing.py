import serial
import matplotlib.pyplot as plt
import time

#Creating instance of serial class for data input from V5 Brain
dataStream = serial.Serial('COM12', baudrate = 115200,timeout = 1) 

#Empty lists to hold data
distances = []
commandVelocity = []
actualVelocity = []

#Creating timer for loop runtime
startTime = time.time()

#Starting loop with 5.0 second time condition
while(time.time() - startTime < 5.0):

    #Giving user a way to monitor time
    print(startTime - time.time())

    #Runs when data is available
    if (dataStream.is_open):

        #unpacks and decodes serial lines
        incomingDatum = dataStream.readline()
        incomingDatum = incomingDatum.decode('utf-8')
        incomingDatum = incomingDatum.strip('\n')
        incomingDatum = incomingDatum[6:] #6 is unique to this situation. It might not be necessary at all.

        #splits incoming values at the comma (3 required), packs into a tuple
        (currentDist, currentCommandVel, currentActualVel) = incomingDatum.split(',')

        #Typecast string values into float
        currentDist = float(currentDist)
        currentActualVel = float(currentActualVel)
        currentCommandVel = float(currentCommandVel)
        
        #Add datum to various lists
        distances.append(time.time() - startTime)
        commandVelocity.append(currentCommandVel)
        actualVelocity.append(currentActualVel)

#Using matplotlib pyplot to create graphic
plt.figure(1)
plt.plot(distances, commandVelocity, color = 'blue')
plt.plot(distances,actualVelocity, color = 'red')
plt.show()