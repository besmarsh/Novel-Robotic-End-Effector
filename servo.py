import RPi.GPIO as GPIO
from time import sleep

class Servo:
    _degree = 10/180
    def __init__(self, pin: int):
        GPIO.setup(pin, GPIO.OUT)
        self._servo = GPIO.PWM(pin, 50)
        self._servo.start(0)
    
    def min(self):
        self._servo.ChangeDutyCycle(2)
        sleep(1)
    
    def max(self):
        self._servo.ChangeDutyCycle(12)
        sleep(1)

    def turn(self, fromPos: int, toPos: int, speed: int):

        if not type(fromPos) == int or fromPos < 0 or fromPos > 180 \
            or not type(toPos) == int or toPos < 0 or toPos > 180:
            raise ValueError("Positions must be integers between 0 and 180 degrees inclusive")
        
        if not type(speed) == int or speed < 1 or speed > 5:
            raise ValueError("Speed must be an integer between 1 and 5 inclusive")
        try:
            self._servo.ChangeDutyCycle(2+(fromPos*Servo._degree))
            for i in range(fromPos, toPos, (speed if toPos > fromPos else -speed)):
                self._servo.ChangeDutyCycle(2+(i*Servo._degree))
                sleep(0.02)
            self._servo.ChangeDutyCycle(2+(toPos*Servo._degree))
            sleep(0.3)
        except Exception:
            self._servo.stop()
            raise Exception
    
    def stop(self):
        self._servo.stop()

try:
    GPIO.setmode(GPIO.BCM)
    finger_motor = Servo(23)
    base_plate_motor = Servo(24)

    # Fully open fingers
    finger_motor.min()
    # Rotate base lifting plate to West-facing position
    base_plate_motor.min()

    # Close fingers
    finger_motor.turn(0, 180, 3)
    sleep(1)
    # Rotate base lifting plate under object (North-facing position)
    base_plate_motor.turn(0, 80, 3)
    # Time to demonstrate grasp
    sleep(5)
    # Rotate base lifting plate out from under object (West-facing position)
    base_plate_motor.turn(80, 0, 3)
    sleep(1)
    # Open fingers
    finger_motor.turn(180, 0, 3)
    sleep(1)

finally:
    finger_motor.stop()
    base_plate_motor.stop()
    GPIO.cleanup()