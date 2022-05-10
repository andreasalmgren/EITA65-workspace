from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.start_preview()
sleep(5)
camera.capture('/home/pi/diggi/EITA65-workspace/LP4/test35.jpg') #directory
camera.stop_preview()
