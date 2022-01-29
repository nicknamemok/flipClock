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
NUMBER_OF_TEETH = 2048
GEAR_RATIO = 3
NUMBER_OF_FLAPS = 12
DELAY_FLIP = 0.5
DELAY_STEP = 0.0005
SERVO_PINS = [[1,2,3,4],        # Hour, digit 1
              [1,2,3,4],        # Hour, digit 2
              [12,16,20,21],    # Minute, digit 1
              [5,6,13,19]]      # Minute, digit 2


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

    def setPosition(self, position: int) -> None:
        self.currentPosition = position


class Controller:

    def __init__(self, numberOfTeeth: int, gearRatio: int, numberOfFlaps: int, stepDelay: float, flipDelay: float) -> None:
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
        self.servos = [Servo(pins) for pins in SERVO_PINS]

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
        {print(servo.currentPosition) for servo in self.servos}

    # Unit test cycle all flaps
    def cycleTest(self):
        for i in range(self.numberOfFlaps):
            self.moveTo([i]*4)
            {print(servo.currentPosition) for servo in self.servos}
            time.sleep(self.flipDelay)
        self.moveTo([0]*4)

            

def main():

    # Instantiate controller object
    controller = Controller(NUMBER_OF_TEETH, GEAR_RATIO, NUMBER_OF_FLAPS, DELAY_STEP, DELAY_FLIP)

    # Options handling
    args = sys.argv[1:]
    optlist, args = getopt.getopt(args, 'm:sa',['m1=','m2=','m3=','m4='])
    for opt, arg in optlist:
        # Single flip test
        if opt in ("-s"):
            print("Single step test")
            controller.unitTest()
            return
        # Cycle flip test
        if opt in ("-a"):
            print("Cycle test")   
            controller.cycleTest()
            return
        # Move single servo
        if opt in ("-m"):
            print("Stepping",arg,"servo.")
            controller.moveSingle(int(arg))
        # Manually step servos by x steps
        if opt in ('--m1'):
            print("Stepping servo 1:",arg,"steps")
            {controller.moveSingle(1) for i in arg}
            return
        if opt in ('--m2'):
            print("Stepping servo 2:",arg,"steps")
            {controller.moveSingle(1) for i in arg}
            return
        if opt in ('--m3'):
            print("Stepping servo 3:",arg,"steps")
            {controller.moveSingle(1) for i in arg}
            return
        if opt in ('--m4'):
            print("Stepping servo 4:",arg,"steps")
            {controller.moveSingle(1) for i in arg}
            return
        
    else:
        # Infinite loop that updates time according to current time, updates at 1 Hz
        while(True):
            controller.moveTo(getCurrentTime())
            time.sleep(1)

    GPIO.cleanup()

if __name__ == "__main__":
    main()
