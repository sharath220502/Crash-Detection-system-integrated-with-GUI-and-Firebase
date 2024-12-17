import RPi.GPIO as GPIO
import time
from time import sleep
import os
from datetime import datetime
import pyrebase

firebaseConfig={
    'apiKey': "",
    'authDomain': "adas-2477a.firebaseapp.com",
    'databaseURL': "https://adas-2477a-default-rtdb.firebaseio.com",
    'projectId': "adas-2477a",
    'storageBucket': "adas-2477a.appspot.com",
    'messagingSenderId': "5",
    'appId': "",
    'measurementId': "G-ZKN54HD0CL"
}
firebase=pyrebase.initialize_app(firebaseConfig)
storage=firebase.storage()

GPIO_TRIGGER = 2
GPIO_ECHO = 3
relay_ch = 26
# Set GPIO mode and pins
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Set up GPIO pins
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(relay_ch, GPIO.OUT)
def distance_measurement():
        # Send a short pulse to the trigger pin
        GPIO.output(GPIO_TRIGGER, True)
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)

        # Measure the start time of the echo pulse
        start_time = time.time()
        while GPIO.input(GPIO_ECHO) == 0:
            start_time = time.time()

        # Measure the end time of the echo pulse
            stop_time = time.time()
        while GPIO.input(GPIO_ECHO) == 1:
            stop_time = time.time()

        # Calculate the time difference between the start and end of the echo pulse
        time_elapsed = stop_time - start_time

        # Calculate the distance (in centimeters)
        speed_of_sound = 34300  # Speed of sound in cm/s
        distance = (time_elapsed * speed_of_sound) / 2

        return distance
def send_to_firebase(distance):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if distance >10:
        data = f"Distance: {distance:.2f} cm\tTimestamp: {timestamp}\n Vehicle ON\n"
    if distance<10:
        data = f"Distance: {distance:.2f} cm\tTimestamp: {timestamp}\t Vehicle OFF \n"
              
        

    with open("/home/ebdlab/Desktop/IOT_ADAS/distance.txt", "a") as file:
        file.write(data)

    # Send distance to Firebase
    time.sleep(1)
    
while(1):
    distance = distance_measurement()
    print("Distance: {:.2f} cm".format(distance))
    if distance >=10:
        GPIO.output(relay_ch, GPIO.LOW)
        time.sleep(1)
        send_to_firebase(distance)
        name='/home/ebdlab/Desktop/IOT_ADAS/distance.txt'
        storage.child(name).put(name)
        print("uploaded")
    if distance <10:
        GPIO.output(relay_ch, GPIO.HIGH)
        send_to_firebase(distance)
        name='/home/ebdlab/Desktop/IOT_ADAS/distance.txt'
        storage.child(name).put(name)
        print("uploaded")
        break


GPIO.cleanup()
