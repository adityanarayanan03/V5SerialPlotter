/* This file is to include any functions for use 
during the autonomous routine. All functions and 
variables declared here will receive global scope.
All motors and objects used here will have brake modes
set according to AutonBrakeMode.h*/
#include "main.h"

void plotLine()
{
    /*
    Function to demonstrate serial plotter. Will create linear plot.
    */
    plotTimer.placeMark();
    printf("%s \n", "{START}");
    pros::delay(1000);

    std::vector<double> plotterPass;

    while (plotTimer.getDtFromMark().convert(second) < 10.0)
    {
        plotterPass = {plotTimer.getDtFromMark().convert(second), 2.0*plotTimer.getDtFromMark().convert(second), 5.0};
        plotterPrint(plotterPass);
        pros::delay(20);
    }

    printf("%s \n", "{STOP}");
    pros::delay(1000);
}