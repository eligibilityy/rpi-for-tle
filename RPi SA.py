from http.server import BaseHTTPRequestHandler, HTTPServer
import time
from gpiozero import LED, Servo 
import RPi.GPIO as GPIO

servo = Servo(17)
led_red = LED(18)
led_green = LED(19)

ip = '10.33.3.78'

req = None

class RequestHandler_httpd(BaseHTTPRequestHandler):
	def do_GET(self):
		global req
		messagetosend = bytes('Test',"utf")
		self.send_response(200)
		self.send_header('Content-Type', 'text/plain')
		self.send_header('Content-Length', len(messagetosend))
		self.end_headers()
		self.wfile.write(messagetosend)
		req = self.requestline
		req = req[5 : int(len(req)-9)]
		print(req)
  
		if req == 'on':
			print("Feeder is ON, please don't input any more requests.")
			servo.max()  # Open the feeder
			time.sleep(1)

		if req == 'off':
			print('Feeder is OFF, waiting for request.')
			servo.min()  # Close the feeder
			time.sleep(1)
   
		
		return

server_address_httpd = (ip,8080)
httpd = HTTPServer(server_address_httpd, RequestHandler_httpd)

print('init')
httpd.serve_forever()
GPIO.cleanup()