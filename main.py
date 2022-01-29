import os
import time
import datetime
from typing import List
import requests
import json
import sys
import getopt
from controller import Controller
from servo import Servo

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
            

def main():

    # Instantiate controller object
    controller = Controller(NUMBER_OF_TEETH, GEAR_RATIO, NUMBER_OF_FLAPS, DELAY_STEP, DELAY_FLIP, SERVO_PINS)

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
