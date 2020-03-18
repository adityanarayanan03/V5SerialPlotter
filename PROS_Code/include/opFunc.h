#include "motors.h"
#include "okapi/api.hpp"
#include "main.h"



void forward(float distance) {
  distance = (.7771*distance) + 7.0163;
  float distance_traveled_left = 0.0;
  rightDTEnc.reset();
  leftDTEnc.reset();
  float power;
  float maxPower = 200;

  while(distance_traveled_left < 5.082493377) {
      distance_traveled_left = leftDTEnc.get()*(3.14159265/180.0)*2.0;
      power = 80.0 * sqrt(distance_traveled_left) + 26.0;
      if (power > 200){
        power = 200.0;
      }
      chassis.arcade(0, power/200.0);
    }
    while(distance_traveled_left < (distance - 10.97623188)) {
      distance_traveled_left = leftDTEnc.get()*(3.14159265/180.0)*2.0;
      power = 200;
      chassis.arcade(0, power/200.0);
    }
    distance_traveled_left = 0.0;
    rightDTEnc.reset();
    leftDTEnc.reset();
    while(distance_traveled_left < distance) {
      distance_traveled_left = leftDTEnc.get()*(3.14159265/180.0)*2.0;
      power = 200 - sqrt(distance_traveled_left)*sqrt((3.0*(200)*(200))/(distance));
      chassis.arcade(0, power/200.0);
    }
    chassis.arcade(0,0);
  }