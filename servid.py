import io
import time
import picamera
from PIL import Image

camera = PiCamera()
camera.resolution = (640,480)
sleep(1) #warmup

for i in range(20):
  sleep(0.1)
  camera.capture('foo.jpg')
