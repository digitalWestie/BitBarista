import io
import time
import picamera
from PIL import Image

# Create the in-memory stream
stream = io.BytesIO()

for i in range(10):
  with picamera.PiCamera() as camera:
    #camera.start_preview()
    time.sleep(0.1)
    camera.capture(stream, format='jpeg')
  # "Rewind" the stream to the beginning so we can read its content
  stream.seek(0)
  image = Image.open(stream)
  image.save("your_file.jpeg")

