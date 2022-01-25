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

        # Related to stepPosition function
        self.m_currentPosition = 0
        self.m_numberOfFlaps = 12
        self.m_stepOrder = [512]*self.m_numberOfFlaps
        self.m_stepOrderIndex = 0

        # Related to stepServo function
        self.flipDelay = flipDelay
        self.stepDelay = stepDelay
        self.m_stepOutput = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
        self.m_stepOutputIndex = 0

        # Initialize pins to output mode
        {GPIO.setup(i, GPIO.OUT) for i in self.m_pins}

    # Steps servo by input steps
    def stepServo(self, steps: int) -> None:

        for i in range(steps):
            self.m_stepOutputIndex = 0 if self.m_stepOutputIndex == len(self.m_stepOutput)-1 else self.m_stepOutputIndex + 1
            for pin in range(len(self.m_pins)):
                GPIO.output(self.m_pins[pin],self.m_stepOutput[self.m_stepOutputIndex][pin])
            time.sleep(self.stepDelay)

    # Step by 1 flap
    def stepPosition(self) -> None:
        # Call function to step servo appropriate number of steps
        self.stepServo(self.m_stepOrder[self.m_stepOrderIndex])
        # Increment step order index and current position cyclically
        if self.m_stepOrderIndex<self.m_numberOfFlaps-1:
            self.m_stepOrderIndex += 1
        else:
            self.m_stepOrderIndex = 0
        self.m_currentPosition = self.m_stepOrderIndex

    # Unit test for servo
    def test(self) -> None:
        for i in [1,2,3,4,5,6,7,8,9,10,11,0]:
            print("Current position: ", self.m_currentPosition,". Going to position: ",i)
            time.sleep(self.flipDelay)
            self.stepPosition()
        print("Test Done\n")


class Controller(Functionalities):

    def __init__(self, stepDelay: float =0.01, flipDelay: float =0) -> None:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.m_servos = [Servo(i, stepDelay, flipDelay) for i in SERVO_PINS]
        self.flipDelay = flipDelay

    # Commands controller to current time
    def toCurrentTime(self) -> None:
        # doneStatus = [False, False, False, False]
        doneStatus = [False, False]
        current_time = self.getCurrentTime()
        print(current_time)

        # Only servos 3 and 4, corresponding to minutes
        while not all(doneStatus):
            for i in range(len(doneStatus)):
                if current_time[i+2] is not self.m_servos[i+2].m_currentPosition:
                    self.m_servos[i+2].stepPosition()
                else:
                    doneStatus[i] = True
            time.sleep(self.flipDelay)
            

        # while not all(doneStatus):
        #     for i in range(len(doneStatus)):
        #         if time[i] != self.m_servos[i].m_currentPosition:
        #             self.m_servos[i].stepPosition()
        #         else:
        #             doneStatus[i] = True
        # print([i.m_currentPosition for i in self.m_servos])

    # Unit test for controller
    def test(self) -> None:
        for servo,i in zip(self.m_servos,[1,2,3,4]):
            print("Testing servo: ",i)
            servo.test()
            time.sleep(2)
            

def main():

    # Instantiate controller object
    controller = Controller(DELAY_STEP, DELAY_FLIP)

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
