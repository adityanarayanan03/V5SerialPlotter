#include "main.h"

Motor dtLF(18, false, AbstractMotor::gearset::green, AbstractMotor::encoderUnits::degrees); //dt = drive Train
Motor dtLB(10, false, AbstractMotor::gearset::green, AbstractMotor::encoderUnits::degrees); //dt = drive Train
Motor dtRF(1, false, AbstractMotor::gearset::green, AbstractMotor::encoderUnits::degrees);
Motor dtRB(13, false, AbstractMotor::gearset::green, AbstractMotor::encoderUnits::degrees);