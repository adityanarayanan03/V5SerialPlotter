import time
import sys
import serial
import matplotlib.pyplot as plt

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

class Run:

    def __init__(self):
        self.usesStopChar = False
        self.testLen = 0
        self.comPort = None
        self.dataStream = None
        self.xAxis = []
        self.fullDataSet = []

    def reset(self):
        self.xAxis = []
        self.fullDataSet = []
        self.testLen = 0

    def setUp(self):
        self.comPort = str(input("Please enter the V5 User port to be used:    "))
        for i in range(3):
            stopCharAsk = str(input("Do you want to end data collection with a stop character? (y/n)"))
            #Structure to determine if the user wants duration based test or length based.
            if (stopCharAsk in ["y", "Y", "yes", "Yes", "YES"]):
                self.usesStopChar = True
                break
            elif (stopCharAsk in ["n", "N","No","no","NO"]): 
                self.testLen = float(input("Please enter the duration of collection (seconds):     "))
                break
            else:
                print("That character was not understood. Please try again. ("+str(i+1)+"/3)")
                time.sleep(1)
                if (i==2):
                    print("System Exiting")
                    sys.exit()
    
    def findSerialConnection(self):
        print("Finding Serial Connection...")
        time.sleep(2)
        exceptionCounter = 1 #Variable to count the number of time-outs.
        while (1):
            #Attempts to find data stream from serial port. 
            try:
                self.dataStream = serial.Serial(self.comPort, baudrate = 115200,timeout = 1) #Set to maximum baud for pReCIsIoN.
                print("Serial Connection Found. Waiting for data input.")
                break

            #Error handling in the chance of no serial link found
            except:
                if (exceptionCounter > 7):
                    print("Timed out while waiting for connection to "+self.comPort)
                    sys.exit()
                print("No serial connection found on "+self.comPort+". Re-trying in 2 seconds. ("+str(exceptionCounter)+"/7)")
                time.sleep(2)
                exceptionCounter+=1

    def waitForStart(self):
        #This loop waits for the START Command from V5 Brain
        print("Waiting for data stream to start.")
        while (1):
            if(preProcessData(self.dataStream.readline())[0] == 'START'): #I know (is) is preferred to == but for some reason only == works.
                print("Start command received. Starting Collection")
                break
    
    def loop(self):
        #Failure variable for looping
        lineDropCount = 0

        #main loop
        #timed run counter
        startTime = time.time()
        while(self.usesStopChar or time.time() - startTime < self.testLen):

            #Runs if data stream has been opened
            if (self.dataStream.is_open):

                #unpacks and decodes serial lines
                incomingDatum = preProcessData(self.dataStream.readline())
                if(incomingDatum[0]=="STOP"):
                    print("Stop Command Received.")
                    time.sleep(1)
                    break
                print(time.time() - startTime)
                #Convert list of strings into a list of float
                try:
                    for stringDatumIndex in range(len(incomingDatum)):
                        incomingDatum[stringDatumIndex] = float(incomingDatum[stringDatumIndex])
                                
                    self.xAxis.append(time.time() - startTime) #Apppend the x-series value to our x-list
                    incomingDatum.pop(0) #Delete x-series value from the datum list
                    self.fullDataSet.append(incomingDatum) #append the n-series' of single element list to full set
                except:
                    print("Something went wrong! Continuing collection.")
                    lineDropCount += 1
                    if (lineDropCount > 50):
                        print("Too many errors. Stopping collection")
                        sys.exit()
    def plot(self):
        plt.plot(self.xAxis, self.fullDataSet)
        plt.show()
        

def runWithSetup():
    currentRun = Run()
    currentRun.setUp()
    currentRun.findSerialConnection()
    currentRun.waitForStart()
    currentRun.loop()
    currentRun.plot()
    return currentRun

def runWithoutSetup(currentRun):
    currentRun.reset()
    #currentRun.findSerialConnection()
    currentRun.waitForStart()
    currentRun.loop()
    currentRun.plot()
    return currentRun

#Main loop:
currentRun = runWithSetup()
while (1):
    runAgain = str(input("Would you like to run the program again?"))
    if (runAgain in ["y", "Y", "yes", "Yes", "YES"]):
        setupYesOrNo = str(input("Would you like to run setup again?"))
        if(setupYesOrNo in ["y", "Y", "yes", "Yes", "YES"]):
            currentRun = runWithSetup()
        else:
            currentRun = runWithoutSetup(currentRun)
    elif (runAgain in ["n", "N", "no","NO","No"]):
        break
    else:
        print("That command was not understood!")