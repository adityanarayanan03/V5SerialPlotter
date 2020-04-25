#include "main.h"

//Individual motor set up. No chassis is made. Hence the reversals of the right side.
Motor dtLF(18, false, AbstractMotor::gearset::green, AbstractMotor::encoderUnits::degrees);
Motor dtLB(10, false, AbstractMotor::gearset::green, AbstractMotor::encoderUnits::degrees);
Motor dtRF(1, true, AbstractMotor::gearset::green, AbstractMotor::encoderUnits::degrees);
Motor dtRB(13, true, AbstractMotor::gearset::green, AbstractMotor::encoderUnits::degrees);

//Creating motor groups per side
MotorGroup leftDT({dtLF, dtLB});
MotorGroup rightDT({dtRF, dtRB});

//Creating one motor group for full chassis
//essentially only for straights in auto.
MotorGroup chassis({dtLF, dtLB, dtRF, dtRB});

Timer autonTimer;