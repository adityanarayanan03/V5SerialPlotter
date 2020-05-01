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

    while (plotTimer.getDtFromMark().convert(second) < 10.0)
    {
        printf("%s", "{");
        printf("%f", plotTimer.getDtFromMark().convert(second));
        printf("%s", ",");
        printf("%f", plotTimer.getDtFromMark().convert(second) * .5);
        printf("%s \n", "}");
        pros::delay(20);
    }

    printf("%s \n", "{STOP}");
    pros::delay(1000);
}