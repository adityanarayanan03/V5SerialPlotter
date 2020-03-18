#include "main.h"
#include "okapi/api.hpp"

using namespace okapi;

Motor dtLF(18, false, AbstractMotor::gearset::green); //dt = drive Train
Motor dtLB(10, false, AbstractMotor::gearset::green); //dt = drive Train
Motor dtRF(1, false, AbstractMotor::gearset::green);
Motor dtRB(13, false, AbstractMotor::gearset::green);

MotorGroup leftDrive({dtLF, dtLB});
MotorGroup rightDrive({dtRF, dtRB});

auto chassis = ChassisControllerFactory::create(
    leftDrive, rightDrive,
    AbstractMotor::gearset::green,
    {4.25, 12.0});
auto leftDTEnc = IntegratedEncoder(dtLF);
auto rightDTEnc = IntegratedEncoder(dtRF);
