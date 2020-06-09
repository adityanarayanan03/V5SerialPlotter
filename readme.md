# About The V5 Serial Plotter

Serial monitors and serial plotters are some of the most useful tools for debugging programs and obtaining data on program performance over time. For the VEX Cortex/VEX V5 system, a serial monitor is readily available within the coding environment in both PROS and VEXCode; however, both environments lack a serial monitor capable of graphically displaying data collected from the Cortex/Brain. Currently, the most widely used method of graphing data from the brain is to save said data to an SD card as a .csv file and plot using plotting tools such as Excel or Google Sheets. The V5 Serial Plotter aims to provide a more efficient process by creating a serial plotter with a graphical interface for creating easily customizable graphs with a permanent link to the Cortex/V5 Brain.

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
