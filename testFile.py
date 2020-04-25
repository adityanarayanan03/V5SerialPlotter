from tkinter import *
import time
import sys
import serial
import serial.tools.list_ports
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
        self.testLen = None
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
            self.comPort = comPortInput.get()
            self.usesStopChar = not(usesDuration.get())
            if(self.usesStopChar == False):
                try:
                    self.testLen = float(testLenEntryBox.get())
                except:
                    popUpError = Tk()
                    popUpError.geometry("200x150")
                    popUpError.title("Error!")
                    errorText = Label(popUpError, text = 'Enter a number for test duration')
                    errorText.place(relx = .025, rely = .5)
            self.setUpFlag = True
    
    def findSerialConnection(self):
        '''
        This function will find a serial connection on the specified port.
        Once the dataStream variable is set, this function should not be run 
        again without reset(). This should be proofed by the self.connectionFlag.
        '''
        try:
            self.dataStream = serial.Serial(self.comPort, baudrate = 115200,timeout = 1) #Set to maximum baud for pReCIsIoN.
            return True

        #Error handling in the chance of no serial link found
        except:
            return False

    def waitForStart(self):
        '''
        This function blocks code until the "START" command is received.
        '''
        #This loop waits for the START Command from V5 Brain
        print("Waiting for data stream to start.")
        startTime = time.time()
        while (time.time() - startTime < 30.0):
            if(preProcessData(self.dataStream.readline())[0] == 'START'): #I know (is) is preferred to == but for some reason only == works.
                print("Start command received. Starting Collection")
                return True
        return False
    
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
                                
                    self.xAxis.append(incomingDatum[0]) #Apppend the x-series value to our x-list
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
        if (savePlot.get()):
            if (savePathWindow != None):
                #plt.savefig()
                pass #take this out when update path
            else:
                #plt.savefig() but to default path
                pass #Take this out when update path
        plt.show()
        
class savePathFrame:
    def onWindowClose(self):
        '''
        Procedure for saving path on exit button
        '''
        self.savePath = self.savePathInputBox.get()
        self.savePathWindow.destroy()

    '''
    This class contains the pop up frame for entering a new save path
    '''
    def __init__(self):
        '''
        Standard method to initialize object
        '''
        self.savePath = None #Should really be default path of this program.
        self.savePathWindow = Tk()
        self.savePathWindow.geometry("220x100")
        self.savePathWindow.title("Enter Save Path")
        self.savePathInputBox = Entry(self.savePathWindow)
        self.savePathInputBox.place(anchor = 'n', relx = .5, rely = .5)
        self.savePathInputTitle = Label(self.savePathWindow, text = 'Enter the file path to save plots to:')
        self.savePathInputTitle.place(anchor = 's', relx = .5, rely = .5)

        self.savePathWindow.protocol("WM_DELETE_WINDOW", self.onWindowClose)

        #self.savePathWindow.mainloop()

def runTest():
    '''
    Function to run the main testing loop.
    '''
    thisTest = Run() #Creating object for current run
    thisTest.setUp() #Set up the test. Double set up protection is contained in setUp()
    connectionFound = thisTest.findSerialConnection()
    if (connectionFound):
        print("Do Some Stuff")
        startReceived = thisTest.waitForStart()
        if (startReceived):
            thisTest.loop()
            thisTest.plot()
            thisTest.reset()
        else:
            popUpError2 = Tk()
            popUpError2.geometry("300x100")
            popUpError2.title("Error!")
            errorText2 = Label(popUpError2, text = 'Timed out waiting for start command.')
            errorText2.place(relx = .5, rely = .5, anchor = CENTER)
    else:
        popUpError = Tk()
        popUpError.geometry("200x150")
        popUpError.title("Error!")
        errorText = Label(popUpError, text = 'Enter an available COM Port')
        errorText.place(relx = .5, rely = .5, anchor = CENTER)


def createDurationEntry():
    global testLenEntryBox
    #Create the settings title
    settingsHeader = Label(text = 'Enter the duration')
    settingsHeader.place(anchor = 'w', rely = horiz2, relx=vert3)

    #Create the entry box for entering duration
    testLenEntryBox.place(anchor = 'w', rely = horiz2, relx = vert4)

savePathWindow = None
def enterSavePath():
    global savePathWindow
    savePathWindow = savePathFrame()

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

#This block is all for creating the File and Help menu at the top of the window
menuBar = Menu(mainWindow)
fileMenu = Menu(menuBar, tearoff = 0)
fileMenu.add_command(label = "Save Path", command = enterSavePath)
fileMenu.add_separator()
helpMenu = Menu(menuBar, tearoff = 0)
helpMenu.add_command(label = "About")
menuBar.add_cascade(label="File", menu=fileMenu)
menuBar.add_cascade(label = "Help", menu = helpMenu)
mainWindow.config(menu = menuBar)

#Create the settings title
settingsHeader = Label(text = 'Settings:')
settingsHeader.config(font = ("Times", 15))
settingsHeader.place(anchor = 'w', rely =vert1, relx=horiz1)

#Create the drop-down menu for Serial port selection
comPortInput = StringVar(mainWindow)
comPortInput.set("Select Serial Port") #Setting Default Value
comPortOptions = [comport.device for comport in serial.tools.list_ports.comports()] #This is where the list of available ports will go
comPortSelector = OptionMenu(mainWindow, comPortInput, *comPortOptions)
comPortSelector.place(anchor='w', rely = horiz2, relx = vert1)

#Create the save plot selector
savePlot = BooleanVar()
savePlotCheckButton = Checkbutton(mainWindow, text = 'Save Plot', variable= savePlot)
savePlotCheckButton.place(anchor = 'w', rely = horiz3, relx = vert1)

#Create the checkbox to use duration-based test
usesDuration = BooleanVar()
usesDurationCheckButton = Checkbutton(mainWindow, text = 'Time-based data collection', variable = usesDuration, command = createDurationEntry)
usesDurationCheckButton.place(anchor = 'w', rely = horiz2, relx = vert2)

testLenEntryBox = Entry(mainWindow)

#Create a run button
runButton = Button(text = 'Run', command = runTest)
runButton.place(relx = .5, rely = .5, anchor = 'w')

mainWindow.mainloop()