import RPi.GPIO as GPIO
from typing import List

class Servo:

    def __init__(self, pins: List[int]):
        # Initialize pins
        self.m_pins = pins
        # State variables of servo
        self.m_stepOutput = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
        self.m_stepOutputIndex = 0
        self.currentPosition = 0
        # Initialize pins to output mode
        {GPIO.setup(i, GPIO.OUT) for i in self.m_pins}

    # Steps servo one step
    def stepServo(self) -> None:
        # Output array to pins
        for pin in range(len(self.m_pins)):
            GPIO.output(self.m_pins[pin],self.m_stepOutput[self.m_stepOutputIndex][pin])
        # Increment stepoutput index cyclically
        if self.m_stepOutputIndex == len(self.m_stepOutput)-1:
            self.m_stepOutputIndex = 0 
        else:
            self.m_stepOutputIndex += 1

    # Access function required for controller access
    def setPosition(self, position: int) -> None:
        self.currentPosition = position