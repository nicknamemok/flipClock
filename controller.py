from typing import List
import RPi.GPIO as GPIO
import time
from servo import Servo

class Controller:

    def __init__(self, numberOfTeeth: int, gearRatio: int, numberOfFlaps: int, stepDelay: float, flipDelay: float, servo_pins: List[List[int]]) -> None:
        # Initializing controller constants based on user input
        totalSteps = gearRatio*numberOfTeeth
        self.numberOfFlaps = numberOfFlaps
        self.normalSteps = int(totalSteps/self.numberOfFlaps)
        self.lastSteps = totalSteps-(numberOfFlaps-1)*self.normalSteps
        self.flipDelay = flipDelay
        self.stepDelay = stepDelay
        # GPIO setup
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.servos = [Servo(pins) for pins in servo_pins]

    # Move to input position
    def moveTo(self, command: List[int]) -> None:
        # Calculate steps needed for move
        movement = [0]*len(self.servos)
        for i in range(len(self.servos)):
            servoPosition = self.servos[i].currentPosition
            # O(1) calculation of servo steps to reach commanded location
            if self.servos[i].currentPosition < command[i]:
                movement[i] = self.normalSteps*(command[i]-self.servos[i].currentPosition)
            elif self.servos[i].currentPosition > command[i]:
                movement[i] = (self.numberOfFlaps-1-self.servos[i].currentPosition+command[i])*self.normalSteps+self.lastSteps
            else:
                movement[i] = 0
        # While any value in the array is above 0, we will loop through to step each servo if needed
        while any(movement):
            for i in range(len(self.servos)):
                if movement[i] > 0:
                    self.servos[i].stepServo()
                    movement[i] -= 1
                    time.sleep(self.stepDelay)
        {self.servos[i].setPosition(command[i]) for i in range(len(self.servos))}

    # Move single servo 1 flap
    def moveSingle(self, servo: int) -> None:
        if self.servos[i].currentPosition < self.numberOfFlaps:
            {self.servos[i].stepServo() for i in range(self.normalSteps)}
            self.servos[i] += 1
        else:
            {self.servos[i].stepServo() for i in range(self.lastSteps)}
            self.servos[i] = 0

    # Unit test to time 1111
    def unitTest(self):
        self.moveTo([1,1,1,1])
        {print(servo.currentPosition, end=" ") for servo in self.servos}

    # Unit test cycle all flaps
    def cycleTest(self):
        for i in range(1,self.numberOfFlaps):
            self.moveTo([i]*4)
            {print(servo.currentPosition) for servo in self.servos}
            time.sleep(self.flipDelay)
        self.moveTo([0]*4)
