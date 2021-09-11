import threading
import mqtt_sub

import RPistepper as stp
import RPi.GPIO as GPIO

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)

M1_pins = [24,25,8,7]
M1 = stp.Motor(M1_pins)

x = threading.Thread(target=mqtt_sub.run)
x.start()

def pan_left():
    for i in range(10):
        M1.move(-20)
        M1.release()
    
def pan_home():
    M1.reset()

def pan_right():
    for i in range(10):
        M1.move(20)
        M1.release()

try:
    while True:
        msg = mqtt_sub.listen_for_msgs()

        if msg == 'pan-left':
            pan_left()
            
        if msg == 'pan-home':
            pan_home()

        elif msg == 'pan-right':
            pan_right()
                    
finally:
    # After a keyboard interrupt or anything else that shuts things down,
    # turn off the LED strand
    print("BYE!")
    

#M1.cleanup()

