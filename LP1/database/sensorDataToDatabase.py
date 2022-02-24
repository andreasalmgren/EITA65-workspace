#Libraries
import RPi.GPIO as GPIO
import time
#import sys
import redis
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

# create the redis connection(s)
r_conn0 = redis.Redis(host='localhost', port=6379, db = 0)
 
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
 
if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            ##original_stdout = sys.stdout # Save a reference to the original standard output # if you uncomment this line and the rest of the block directly below :P, remeber to uncomment in library section #import sys

            ## with open('filename.txt', 'w') as f:
                ##sys.stdout = f # Change the standard output to the file we created.
                ##print ("Measured Distance = %.1f cm" % dist)
                ##sys.stdout = original_stdout # Reset the standard output to its original value
            
            ##print (dist)
            
            
            # create a key-value pair with key (sen data to database)
            # retrieve the value(s) by using the key(s)
            r_conn0.set('distance', dist)
            
            value0 = r_conn0.get('distance').decode() 
            print("distance_to_object -->", value0)

            
            time.sleep(1)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
