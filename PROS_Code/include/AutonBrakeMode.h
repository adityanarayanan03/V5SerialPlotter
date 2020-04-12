//This file is used to set the brake types of motors during autonomous.
//They will be overwritten by UserBrakeMode.h in OPControl.
#include "main.h"

//Setting brake modes for each of left and right.
//They are controlled independently for turns
leftDT.setBrakeMode(AbstractMotor::brakeMode::coast);
rightDT.setBrakeMode(AbstractMotor::brakeMode::coast);

//Setting brake mode for chassis as a whole.
//Basically just for the sake of redundancy.
chassis.setBrakeMode(AbstractMotor::brakeMode::coast);