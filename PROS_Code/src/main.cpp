#include "main.h"
#include "opFunc.h"

using namespace okapi;

void initialize() {
  pros::lcd::initialize();
}//Don't know if this is really gonna be used

void disabled() {} //Runs while robot is disabled. Not sure if we're gonna use this

void competition_initialize() {} //Probably put an autonomous selector here

void autonomous() {
} 

void opcontrol()
{
  float distance = 1.0;
  float commandVelocity = 200.0;
  float actualVelocity = 180.0;
  Controller masterController;
  while(true){
    chassis.arcade(masterController.getAnalog(ControllerAnalog::leftX),
                   masterController.getAnalog(ControllerAnalog::leftY));
    printf("%f", leftDTEnc.get());
    printf("%s", ",");
    printf("%f", 200.0*masterController.getAnalog(ControllerAnalog::leftY));
    printf("%s", ",");
    printf("%f \n", dtLF.getActualVelocity());
    pros::delay(20);
  }
}
