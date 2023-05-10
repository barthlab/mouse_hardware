# Web streaming example
# Source code from the official PiCamera package
# http://picamera.readthedocs.io/en/latest/recipes2.html#web-streaming

import io
import logging
import socketserver
import threading
from http import server
import socket

import picamera

CAMERA_RESOLUTION = (1024, 768)
PORT = 8080

PAGE=f"""\
<html>
<body>
<center><img src="stream.mjpg" width="{CAMERA_RESOLUTION[0]}" height="{CAMERA_RESOLUTION[0]}></center>
</body>
</html>
"""

def get_current_private_ip():
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.connect(("8.8.8.8", 80)) # 8.8.8.8 is a google server
  out = s.getsockname()[0]
  s.close()
  return(out)


class StreamingOutput(object):
  def __init__(self):
    self.frame = None
    self.buffer = io.BytesIO()
    self.condition = threading.Condition()

  def write(self, buf):
    if buf.startswith(b'\xff\xd8'):
      # New frame, copy the existing buffer's content and notify all
      # clients it's available
      self.buffer.truncate()
      with self.condition:
        self.frame = self.buffer.getvalue()
        self.condition.notify_all()
        self.buffer.seek(0)
    return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
  def do_GET(self):
    if self.path == '/':
      self.send_response(301)
      self.send_header('Location', '/index.html')
      self.end_headers()
    elif self.path == '/index.html':
      content = PAGE.encode('utf-8')
      self.send_response(200)
      self.send_header('Content-Type', 'text/html')
      self.send_header('Content-Length', len(content))
      self.end_headers()
      self.wfile.write(content)
    elif self.path == '/stream.mjpg':
      self.send_response(200)
      self.send_header('Age', 0)
      self.send_header('Cache-Control', 'no-cache, private')
      self.send_header('Pragma', 'no-cache')
      self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
      self.end_headers()
      try:
        while True:
          with output.condition:
            output.condition.wait()
            frame = output.frame
          self.wfile.write(b'--FRAME\r\n')
          self.send_header('Content-Type', 'image/jpeg')
          self.send_header('Content-Length', len(frame))
          self.end_headers()
          self.wfile.write(frame)
          self.wfile.write(b'\r\n')
      except Exception as e:
        logging.warning(
          'Removed streaming client %s: %s',
          self.client_address, str(e))
    else:
      self.send_error(404)
      self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
  allow_reuse_address = True
  daemon_threads = True

with picamera.PiCamera() as camera:
  camera.resolution = CAMERA_RESOLUTION
  output = StreamingOutput()
  #Uncomment the next line to change your Pi's Camera rotation (in degrees)
  #camera.rotation = 90
  camera.start_recording(output, format='mjpeg')
  try:
    address = get_current_private_ip()
    server = StreamingServer((address, PORT), StreamingHandler)
    print(f"http://{address}:{PORT}")
    server.serve_forever()
  finally:
    camera.stop_recording()

# TODO simply the code
# TODO display only once?
