serial_port = /dev/ttyACM0
FQBN = arduino:avr:yun
baud_rate = 9600


help:
	cat ./makefile

upload:
	arduino-cli compile -u -b $(FQBN) -p $(serial_port) ./

compile:
	arduino-cli compile -b $(FQBN) -p $(serial_port) ./

list:
	arduino-cli board list

monitor:
	alacritty -e screen $(serial_port) $(baud_rate) # look into sudo arduino-cli monitor -p /dev/ttyACM0
