import serial
import matplotlib.pyplot as plt

dataStream = serial.Serial('COM12', baudrate = 115200,timeout = 1)

distances = []
commandVelocity = []
actualVelocity = []

for i in range (100):
    if (dataStream.is_open):
        incomingDatum = dataStream.readline()
        incomingDatum = incomingDatum.decode('utf-8')
        incomingDatum = incomingDatum.strip('\n')
        incomingDatum = incomingDatum[6:]
        print(incomingDatum)
        (currentDist, currentActualVel, currentCommandVel) = incomingDatum.split(',')

        currentDist = float(currentDist)
        currentActualVel = float(currentActualVel)
        currentCommandVel = float(currentCommandVel)
        
        distances.append(currentDist)
        commandVelocity.append(currentCommandVel)
        actualVelocity.append(currentActualVel)

plt.figure(1)
plt.plot(distances, commandVelocity)
plt.plot(distances, actualVelocity)
plt.show()