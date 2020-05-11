from flask import Flask, render_template, request
from time import sleep
import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib

#define GPIO pins
GPIO_pins = (14, 15, 18) # Microstep Resolution MS1-MS3 -> GPIO Pin
direction= 20	       # Direction -> GPIO Pin
step = 26      # Step -> GPIO Pin
lamp = 12

# Declare an named instance of stepper class pass GPIO pins numbers
mymotor = RpiMotorLib.A4988Nema(direction, step, GPIO_pins, "A4988")

GPIO.setup(lamp, GPIO.OUT)
GPIO.output(lamp, 0)

app = Flask(__name__)

@app.route("/")
def home():

    return render_template('index.html')

@app.route("/next")
def next():

    mymotor.motor_go(False, "Full" , 432, 0.0009, False, .05)
    print("Moving to the next frame!")

    return render_template('index.html')

@app.route("/back")
def back():

    mymotor.motor_go(True, "Full" , 432, 0.0009, False, .05)
    print("Moving back a frame!")

    return render_template('index.html')

@app.route("/stb1")
def stb1():

    mymotor.motor_go(True, "Full" , 8, .001, False, .05)
    print("Back on step")

    return render_template('index.html')

@app.route("/stf1")
def stf1():

    mymotor.motor_go(False, "Full" , 8, .001, False, .05)
    print("Foward one step!")

    return render_template('index.html')

@app.route("/lamp")
def lamp():

    if GPIO.input(12): # if port 12 == 1
        print "LAMP OFF!"
        GPIO.output(12, 0)         # set port/pin value to 1/HIGH/True
    else:
        print "LAMP ON!"
        GPIO.output(12, 1)         # set port/pin value to 0/LOW/False
    sleep(0.1)         # wait 0.1 seconds

    return render_template('index.html')



# Run the app on the local development server
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
