from time import sleep
from picamera import PiCamera

camera = PiCamera()
camera.resolution = (640,480)
sleep(1) #warmup

for i in range(20):
  sleep(0.1)
  camera.capture('foo.jpg')
