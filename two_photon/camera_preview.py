#!/bin/env python3

from http import server
import io
import os
import OpenSSL
import socket
import socketserver
import ssl
import threading
import time

import picamera

import constants



PORT = 4443
KEY_FILE = "/tmp/camera_preview_server.key"
CERT_FILE = "/tmp/camera_preview_server.crt"
PAGE = f"""\
<html>
<body>
<img src="stream.mjpg" width="{constants.CAMERA_RESOLUTION[0]}" height="{constants.CAMERA_RESOLUTION[1]}"/>
</body>
</html>
"""



def generate_ssl_certificate(
  emailAddress="emailAddress",
  commonName="commonName",
  countryName="CN",
  localityName="localityName",
  stateOrProvinceName="stateOrProvinceName",
  organizationName="organizationName",
  organizationUnitName="organizationUnitName",
  serialNumber=0,
  validityStartInSeconds=0,
  validityEndInSeconds=10*365*24*60*60,
  key_file="private.key",
  cert_file="selfsigned.crt"):
  # create a key pair
  key = OpenSSL.crypto.PKey()
  key.generate_key(OpenSSL.crypto.TYPE_RSA, 4096)

  # create a self-signed cert
  cert = OpenSSL.crypto.X509()
  cert.get_subject().C = countryName
  cert.get_subject().ST = stateOrProvinceName
  cert.get_subject().L = localityName
  cert.get_subject().O = organizationName
  cert.get_subject().OU = organizationUnitName
  cert.get_subject().CN = commonName
  cert.get_subject().emailAddress = emailAddress
  cert.set_serial_number(serialNumber)
  cert.gmtime_adj_notBefore(0)
  cert.gmtime_adj_notAfter(validityEndInSeconds)
  cert.set_issuer(cert.get_subject())
  cert.set_pubkey(key)
  cert.sign(key, "sha512")

  with open(cert_file, "wt") as f:
    f.write(OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, cert).decode("utf-8"))

  with open(key_file, "wt") as f:
    f.write(OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, key).decode("utf-8"))



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
  if not os.path.isfile(CERT_FILE) or not os.path.isfile(KEY_FILE):
    print("Could not find certificate file and key file")
    print("Generating new certificate file and key file")

    if os.path.isfile(CERT_FILE):
      os.remove(CERT_FILE)

    if os.path.isfile(KEY_FILE):
      os.remove(KEY_FILE)

    generate_ssl_certificate(serialNumber=int(time.time()), key_file=KEY_FILE, cert_file=CERT_FILE)

  else:
    print("Found certificate file and key file")

  with picamera.PiCamera() as camera:
    camera.resolution = constants.CAMERA_RESOLUTION
    output = StreamingOutput()
    camera.start_recording(output, format="mjpeg")

    try:
      address = get_current_private_ip()
      server = StreamingServer((address, PORT), StreamingHandler)
      server.socket = ssl.wrap_socket(server.socket, keyfile=KEY_FILE, certfile=CERT_FILE, server_side=True)
      print(f"https://{address}:{PORT}/index.html")
      print("Press CTRL+C to exit")
      server.handle_request()
      server.handle_request()
      server.handle_request()
      server.handle_request()
      server.handle_request()
      server.handle_request()
      server.handle_request()

      while True:
        pass

    finally:
      camera.stop_recording()
