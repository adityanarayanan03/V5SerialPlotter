//This file overwrites the brake mode set by autonomous
//for user control.
#include "main.h"

//Setting brake modes for each of left and right.
//They are controlled independently for turns
leftDT.setBrakeMode(AbstractMotor::brakeMode::coast); //Coast mode for Driver
rightDT.setBrakeMode(AbstractMotor::brakeMode::coast);

//Setting brake mode for chassis as a whole.
//Basically just for the sake of redundancy.
chassis.setBrakeMode(AbstractMotor::brakeMode::coast); //Cost mode for Driver