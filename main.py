import os
import time
import datetime
from typing import List
import RPi.GPIO as GPIO
import requests
import json
import sys
import getopt

# Session constants
DELAY_FLIP = 0.5
DELAY_STEP = 0.0025
SERVO_PINS = [[1,2,3,4],        # Hour, digit 1
              [1,2,3,4],        # Hour, digit 2
              [12,16,20,21],    # Minute, digit 1
              [5,6,13,19]]      # Minute, digit 2


class Functionalities:

    def getCurrentTime(now: datetime =datetime.datetime.now()) -> List[int]:
        now = datetime.datetime.now()
        return([int(now.hour/10),now.hour%10,int(now.minute/10),now.minute%10])

    # Currently weather not in order, API keys are not loaded in
    # def getCurrentWeather() -> List[int]:
    #     env.load_dotenv()
    #     token = os.environ.get("api-token")
    #     city = os.environ.get("city")
    #     url = "http://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=" + token
    #     response = requests.get(url).json()
    #     temperature = round(response['main']['temp']-273.15)
    #     return([int(temperature/10), temperature%10, 0, 0])


class Servo:

    def __init__(self, pins: List[int], stepDelay: float, flipDelay: float):

        # Initialize pins
        self.m_pins = pins

        # State variables of servo
        self.m_stepOutput = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
        self.m_stepOutputIndex = 0

        # Initialize pins to output mode
        {GPIO.setup(i, GPIO.OUT) for i in self.m_pins}

    # Steps servo one step
    def stepServo(self) -> None:
        # Output array to pins
        for pin in range(len(self.m_pins)):
            GPIO.output(self.m_pins[pin],outputs[pin])
        # Increment stepoutput index cyclically
        if self.m_stepOutputIndex == len(self.m_stepOutput)-1:
            self.m_stepOutputIndex = 0 
        else:
            self.m_stepOutputIndex += 1


class Controller(Functionalities):

    def __init__(self, stepDelay: float, flipDelay: float) -> None:

        self.flipDelay = flipDelay
        self.stepDelay = stepDelay

        self.m_numberOfFlaps = 12
        self.m_stepOrder = [512]*self.m_numberOfFlaps

        self.currentPositions = [0,0,0,0]

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.m_servos = [Servo(i, stepDelay, flipDelay) for i in SERVO_PINS]
        self.flipDelay = flipDelay

    # Should generalize number of servos under controller command
    # Should also make it constant time to calculate number of steps needed    
    def calculateMovement(command: List[int]) -> List[int]:
        movement = [0]*4
        for i in range(4):
            while self.currentPositions[i] is not command[i]:
                # Sum up current steps to movement
                movement[i] += self.m_stepOrder[self.currentPositions[i]]
                # Increment position cyclically
                # Note that each index is the number of steps to progress from that index flap to the next
                # i.e. for stepOrder[0] that is the number of steps from 0 -> 1
                if self.currentPositions[i] is self.m_numberOfFlaps-1:
                    self.m_currentPositions[i] = 0
                else:
                    self.m_currentPositions[i] += 1
        return movement

    def moveTo(command: List[int]) -> None:
        # Retrieve movement needed
        movement = calculateMovement(command)
        # While any value in the array is above 0, we will loop through to step
        while any(movement):
            for i in range(4):
                # If there are still steps for given servo, will step that servo
                # and then decrement number of steps needed
                if movement[i] > 0:
                    self.m_servos[i].stepServo()
                    movement[i] -= 1
                    time.sleep(self.stepDelay)

    # Commands controller to current time
    def toCurrentTime(self) -> None:

        current_time = self.getCurrentTime()
        print(current_time)

        stepCounter = []
        while (any(flapDoneStatus)):

    # Unit test to time 1111
    def unitTest():
        self.moveTo([1,1,1,1])
        print(currentPositions)

    # Unit test cycle all flaps
    def cycleTest():
        for i in range(self.m_numberOfFlaps):
            self.moveTo([i]*4)
            print(currentPositions)
            time.sleep(self.flipDelay)

            

def main():

    # Instantiate controller object
    controller = Controller(DELAY_STEP, DELAY_FLIP)

    # Test
    controller.

    # Options handling
    args = sys.argv[1:]
    optlist, args = getopt.getopt(args, 's:m:a',['m1=','m2=','m3=','m4='])
    for opt, arg in optlist:
        # Single servo cycle test
        if opt in ("-s"):
            print("Testing single servo: ",arg)
            controller.m_servos[int(arg)-1].test()
            return
        # All servo cycle test
        if opt in ("-a"):
            print("Testing all servos")   
            controller.test()
            return
        # Manually step single servo one flap
        if opt in ("-m"):
            print("Stepping servo: ",arg)
            controller.m_servos[int(arg)-1].stepPosition()
            return
        # Manually step servos by x steps
        if opt in ('--m1'):
            print("Stepping servo 1:",arg,"steps")
            {controller.m_servos[0].stepPosition() for i in range(int(arg))}
            return
        if opt in ('--m2'):
            print("Stepping servo 2:",arg,"steps")
            {controller.m_servos[1].stepPosition() for i in range(int(arg))}
            return
        if opt in ('--m3'):
            print("Stepping servo 3:",arg,"steps")
            {controller.m_servos[2].stepPosition() for i in range(int(arg))}
            return
        if opt in ('--m4'):
            print("Stepping servo 4:",arg,"steps")
            {controller.m_servos[3].stepPosition() for i in range(int(arg))}
            return
        
    else:
        # Infinite loop that updates time according to current time, updates at 1 Hz
        while(True):
            controller.toCurrentTime()
            time.sleep(1)

    GPIO.cleanup()


if __name__ == "__main__":
    main()
