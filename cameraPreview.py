#!/bin/env python3

from http import server
import io
import socket
import socketserver
import sys
import threading
import time

import picamera



CAMERA_RESOLUTION = (1024, 768)
PORT = 8080
PAGE=f"""\
<html>
<body>
<img src="stream.mjpg" width="{CAMERA_RESOLUTION[0]}" height="{CAMERA_RESOLUTION[1]}"/>
</body>
</html>
"""



def get_current_private_ip():
  """Function that gets the current private ip address"""
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.connect(("8.8.8.8", 80)) # 8.8.8.8 is a google server
  out = s.getsockname()[0]
  s.close()
  return(out)



class StreamingOutput(object):
  """Class that streams the output of the raspberry pi camera."""
  def __init__(self):
    self.frame = None
    self.buffer = io.BytesIO()
    self.condition = threading.Condition()

  def write(self, buf):
    if buf.startswith(b"\xff\xd8"):
      self.buffer.truncate()
      with self.condition:
        self.frame = self.buffer.getvalue()
        self.condition.notify_all()
      self.buffer.seek(0)
    return self.buffer.write(buf)



class StreamingHandler(server.BaseHTTPRequestHandler):
  """Handler that updates the HTTP stream with the streaming output."""
  # to silence the handler
  def log_message(self, format, *args):
    return

  def do_GET(self):
    if self.path == "/index.html":
      content = PAGE.encode("utf-8")
      self.send_response(200)
      self.send_header("Content-Type", "text/html")
      self.send_header("Content-Length", len(content))
      self.end_headers()
      self.wfile.write(content)

    elif self.path == "/stream.mjpg":
      self.send_response(200)
      self.send_header("Age", 0)
      self.send_header("Cache-Control", "no-cache, private")
      self.send_header("Pragma", "no-cache")
      self.send_header("Content-Type", "multipart/x-mixed-replace; boundary=FRAME")
      self.end_headers()

      try:
        while True:
          # output is defined way below
          with output.condition:
            output.condition.wait()
            frame = output.frame

          self.wfile.write(b"--FRAME\r\n")
          self.send_header("Content-Type", "image/jpeg")
          self.send_header("Content-Length", len(frame))
          self.end_headers()
          self.wfile.write(frame)
          self.wfile.write(b"\r\n")

      except Exception as e:
        pass

    else:
      self.send_error(404)
      self.end_headers()



class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
  allow_reuse_address = True
  daemon_threads = True



if "__main__" == __name__:
  with picamera.PiCamera() as camera:
    camera.resolution = CAMERA_RESOLUTION
    output = StreamingOutput()
    camera.start_recording(output, format="mjpeg")
    try:
      address = get_current_private_ip()
      server = StreamingServer((address, PORT), StreamingHandler)
      print(f"http://{address}:{PORT}/index.html")
      print("Press CTRL+C to exit")
      server.handle_request()
      server.handle_request()
      while True:
        pass
    finally:
      camera.stop_recording()
