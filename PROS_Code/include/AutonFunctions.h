/* This file is to include any functions for use 
during the autonomous routine. All functions and 
variables declared here will receive global scope.
All motors and objects used here will have brake modes
set according to AutonBrakeMode.h*/
#include "main.h"
//void forward(float targetDistance, int maxSpeed = 170);
void forward(){
    int i = 1;
    while(true){
        chassis.moveVoltage(6000);
        printf("%f",leftFrontEncoder.get());
        printf("%s", ",");
        printf("%f",chassis.getActualVelocity());
        printf("%s", ",");
        printf("%f", 300.0);
        printf("%s", ",");
        printf("%f", 250.0);
        printf("%s", ",");
        printf("%f \n", 200.0);
    }
}