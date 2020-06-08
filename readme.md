# V5 Serial Plotter

The V5 Serial Plotter is intended to be used with the VEX V5 System and the PROS language, although it can be used with any external device capable of Serial communication with a windows machine. 

### Setting up the V5 Serial Plotter

Until the V5 Serial Plotter is converted to windows executable files, the following Python packages must be available to plotter.py

Command-Line Interface (master branch):
1. Time (default install with Python distribution)
2. Sys (default install with Python distribution)
3. PySerial
4. Matplotlib

Graphical Interface (GUI branch):
1. Time (default install)
2. Sys (default install)
3. PySerial
4. Matplotlib
5. Tkinter

### Using the V5 Serial Plotter

1. Connect to the V5 Brain or external device through serial port.
2. If using the Command Line Interface, load the PROS Terminal to find the name of the V5-User port that is connected. 
3. Run plotter.py
4. Select or enter the name of the V5-user port.
5. You have 2 options for the duration of the data collection: time-based, or stop-character based. The example code in PROS_Code is set up to use stop-character based (default method).
6. When outputting data to be plotted, format the data as follows: output {START} to begin data collection, output data to be graphed as {x_axis, y_axis1, y_axis2, etc} followed by a newline, and end collection with {STOP}. Note: Include braces as these are the delimiters for interpreting data. See PROS_Code/include/AutonFunctions.h for an example.
