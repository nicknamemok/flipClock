import RPi.GPIO as GPIO
import time

# Set up output pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
servo_pins =  [[12,16,20,21], [5,6,13,19]]
for i in servo_pins:
    for j in i:
        GPIO.setup(j, GPIO.OUT)

stepOutput = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
stepOutputIdx = 0

for i in range(512*4):
    for j in range(4):
        # servo 1
        GPIO.output(servo_pins[0][j], stepOutput[stepOutputIdx][j])
        # servo 2
        GPIO.output(servo_pins[1][j], stepOutput[stepOutputIdx][j])
        # increment stepoutput index cyclically
    if stepOutputIdx == 3:
        stepOutputIdx = 0
    else:
        stepOutputIdx += 1
    print(i)
    time.sleep(0.0020)

GPIO.cleanup()