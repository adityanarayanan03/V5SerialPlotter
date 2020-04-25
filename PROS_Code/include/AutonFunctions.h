/* This file is to include any functions for use 
during the autonomous routine. All functions and 
variables declared here will receive global scope.
All motors and objects used here will have brake modes
set according to AutonBrakeMode.h*/
#include "main.h"
//void forward(float targetDistance, int maxSpeed = 170);
void forward(){
    rightFrontEncoder.reset();
    printf("%s \n", "{START}");
    pros::delay(1000);
    float targetVelocity;
    float inputVelocity;
    autonTimer.placeMark();
    while( true){
        chassis.moveVelocity(inputVelocity);
        if(autonTimer.getDtFromMark().convert(second) < 10){
            targetVelocity = 17.0 * autonTimer.getDtFromMark().convert(second);
        } 
        else if (autonTimer.getDtFromMark().convert(second) < 20){
            targetVelocity = 170;
        }
        else if (autonTimer.getDtFromMark().convert(second) < 30){
            targetVelocity = 170 - (autonTimer.getDtFromMark().convert(second)-20)*17.0;
        }
        inputVelocity = targetVelocity + .25 * (targetVelocity - chassis.getActualVelocity());
        printf("%s", "{");
        printf("%f", rightFrontEncoder.get());
        printf("%s", ",");
        printf("%f", chassis.getActualVelocity());
        printf("%s", ",");
        printf("%f", targetVelocity); printf("%s \n", "}");
        pros::delay(20);
    }
    printf("%s \n", "{STOP}");
    pros::delay(1000);
}