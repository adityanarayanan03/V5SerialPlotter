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
  while(true){
    printf("%f\n", 1.0);
  }
}
