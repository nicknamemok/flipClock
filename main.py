import os
import time
import datetime
from typing import List
import RPi.GPIO as GPIO
# import dotenv as env
import requests
import json
import sys
# from constants import *
import getopt

delayFlip = 0.5
delayStep = 0.0025
servoPins = [[5,6,13,19],[12,16,20,21],[1,2,3,4],[1,2,3,4]]


class Functionalities:

    def getCurrentTime(now: datetime =datetime.datetime.now()) -> List[int]:
        now = datetime.datetime.now()
        return([int(now.hour/10),now.hour%10,int(now.minute/10),now.minute%10])

    def getCurrentWeather() -> List[int]:
        env.load_dotenv()
        token = os.environ.get("api-token")
        city = os.environ.get("city")
        url = "http://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=" + token
        response = requests.get(url).json()
        temperature = round(response['main']['temp']-273.15)
        return([int(temperature/10), temperature%10, 0, 0])


class Servo:

    def __init__(self, pins: List[int], stepDelay: float, flipDelay: float):

        self.m_pins = pins

        # Related to stepPosition function
        self.m_currentPosition = 0
        self.m_numberOfFlaps = 12
        # self.m_stepOrder = [85]*11 + [89]
        # self.m_stepOrder = [170]*11 + [178]
        self.m_stepOrder = [512]*12

        # Related to stepServo function
        self.flipDelay = flipDelay
        self.stepDelay = stepDelay
        self.m_stepOrderIndex = 0
        self.m_stepOutputIndex = 0
        self.m_stepOutput = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
        self.m_subStepOutput = [[1,0,0,0],[1,1,0,0],[0,1,0,0],[0,1,1,0],[0,0,1,0],[0,0,1,1],[0,0,0,1],[1,0,0,1]]
        {GPIO.setup(i, GPIO.OUT) for i in self.m_pins}
        # {GPIO.output(pin, 0) for pin,output in zip(self.m_pins,self.m_stepOutput[self.m_stepOutputIndex])}

    def stepServo(self, steps: int) -> None:

        for i in range(steps):
            self.m_stepOutputIndex = 0 if self.m_stepOutputIndex == len(self.m_stepOutput)-1 else self.m_stepOutputIndex + 1
            # [GPIO.output(pin, 1) for pin in self.m_stepOutput[self.m_stepOutputIndex]]
            [GPIO.output(pin, 1) for pin,output in zip(self.m_pins,self.m_stepOutput[self.m_stepOutputIndex])]
            
            for pin in range(len(self.m_pins)):
                GPIO.output(self.m_pins[pin],self.m_stepOutput[self.m_stepOutputIndex][pin])
            
            time.sleep(self.stepDelay)
            # [GPIO.output(pin, 0) for pin in stepOutput[self.m_stepOutputIndex]]
            [GPIO.output(pin, 0) for pin,output in zip(self.m_pins,self.m_stepOutput[self.m_stepOutputIndex])]


    def stepPosition(self) -> None:
        self.stepServo(self.m_stepOrder[self.m_stepOrderIndex])
        self.m_stepOrderIndex = self.m_currentPosition = self.m_stepOrderIndex+1 if self.m_stepOrderIndex<self.m_numberOfFlaps-1 else 0

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
        self.m_servos = [Servo(i, stepDelay, flipDelay) for i in servoPins]
        self.m_postion = self.getCurrentTime()
        # self.toCurrentTime()
        self.flipDelay = flipDelay

    def toCurrentTime(self) -> None:
        doneStatus = [False, False, False, False]
        time = self.getCurrentTime()
        while not all(doneStatus):
            for i in range(len(doneStatus)):
                if time[i] != self.m_servos[i].m_currentPosition:
                    self.m_servos[i].stepPosition()
                else:
                    doneStatus[i] = True
        print([i.m_currentPosition for i in self.m_servos])

    def test(self) -> None:
        for servo,i in zip(self.m_servos,[1,2,3,4]):
            print("Testing servo: ",i)
            servo.test()
            time.sleep(2)
            

def main():

    controller = Controller(delayStep, delayFlip)

    args = sys.argv[1:]
    optlist, args = getopt.getopt(args, 's:m:')
    for opt, arg in optlist:
        if opt in ("-s","--single"):
            print("Testing single servo: ",arg)
            controller.m_servos[int(arg)-1].test()
            return
        if opt in ("-m","--manual"):
            print("Stepping servo: ",arg)
            controller.m_servos[int(arg)-1].stepPosition()
            return
    else:
        print("Testing all servos")   
        controller.test()

    GPIO.cleanup()


if __name__ == "__main__":
    main()
