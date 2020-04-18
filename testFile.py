from tkinter import *
import time
import sys
import serial
import matplotlib.pyplot as plt

def preProcessData(incomingDatum):
    '''
    This function will take in a single line from the serial 
    stream (with all the mumbo jumbo) and clean it up. Decode
    using utf-8 encoding, strip of any newline characters that
    may be present, and save data between the start character({) and
    the stop character (}) to a list.
    '''
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
    '''
    This class is made for each time the file is run. The class
    contains information and functions for setting up and running
    a data collection cycle
    '''
    def __init__(self):
        self.usesStopChar = False
        self.testLen = 0
        self.comPort = None
        self.dataStream = None
        self.xAxis = []
        self.fullDataSet = []
        self.setUpFlag = False
        self.connectionFlag = False

    def reset(self):
        self.xAxis = []
        self.fullDataSet = []
        self.testLen = 0

    def setUp(self):
        '''
        This function takes input to determine settings for the run.
        This should be modified to take data from buttons rather than
        user input before the first release.
        '''
        if (not(self.setUpFlag)):
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
            self.setUpFlag = True
    
    def findSerialConnection(self):
        '''
        This function will find a serial connection on the specified port.
        Timeout is 14 seconds. Once the dataStream variable is set, this
        function should not be run again without reset(). This should be proofed
        by the self.connectionFlag.
        '''
        if (not(self.connectionFlag)):
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
            self.connectionFlag = True

    def waitForStart(self):
        '''
        This function blocks code until the "START" command is received.
        '''
        #This loop waits for the START Command from V5 Brain
        print("Waiting for data stream to start.")
        while (1):
            if(preProcessData(self.dataStream.readline())[0] == 'START'): #I know (is) is preferred to == but for some reason only == works.
                print("Start command received. Starting Collection")
                break
    
    def loop(self):
        '''
        Main loop for the data collection sequence. May be exited by
        either duration or receiving the 'STOP' command, depending on
        variables in settings.
        '''
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
        '''
        Uses Matplotlib.pyplot to plot the data set after looping.
        '''
        plt.plot(self.xAxis, self.fullDataSet)
        plt.show()
        
#Define some variables for positioning
#Percentages of frame size for relx and rely command
horiz1 = 0.025
horiz2 = 0.075
horiz3 = 0.15
vert1 = 0.025
vert2 = .30
vert3 = .6
vert4 = .75

#Create the full window that user will see
mainWindow = Tk()
mainWindow.geometry("700x700")
mainWindow.title("PROS Serial Plotter")

#Create the settings title
settingsHeader = Label(text = 'Settings:')
settingsHeader.config(font = ("Times", 15))
settingsHeader.place(anchor = 'w', rely =vert1, relx=horiz1)

#Create the drop-down menu for Serial port selection
comPortInput = StringVar(mainWindow)
comPortInput.set("Select Serial Port") #Setting Default Value
comPortOptions = ["option1","option2"] #This is where the list of available ports will go
w = OptionMenu(mainWindow, comPortInput, *comPortOptions)
w.place(anchor='w', rely = horiz2, relx = vert1)
comPortInput = comPortInput.get() #This command will prob need to go in some loop later on

#Create the save plot selector
savePlot = BooleanVar()
savePlotCheckButton = Checkbutton(mainWindow, text = 'Save Plot', variable= savePlot)
savePlotCheckButton.place(anchor = 'w', rely = horiz3, relx = vert1)

#Create the checkbox to use duration-based test
usesDuration = BooleanVar()
usesDurationCheckButton = Checkbutton(mainWindow, text = 'Time-based data collection', variable = usesDuration)
usesDurationCheckButton.place(anchor = 'w', rely = horiz2, relx = vert2)

#Create the save settings option
saveSettings = BooleanVar()
saveSettingsCheckButton = Checkbutton(mainWindow, text = 'Save Current Settings', variable = saveSettings)
saveSettingsCheckButton.place(anchor = 'w', rely = horiz3, relx =vert2)

#Create the settings title
settingsHeader = Label(text = 'Enter the duration')
settingsHeader.place(anchor = 'w', rely = horiz2, relx=vert3)

#Create the entry box for entering duration
testLen = StringVar()
testLenEntryBox = Entry(mainWindow)
testLenEntryBox.place(anchor = 'w', rely = horiz2, relx = vert4 )

mainWindow.mainloop()

