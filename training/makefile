serial_port = /dev/ttyACM0
FQBN = arduino:avr:yun
baud_rate = 9600


help:
	cat ./makefile

upload:
	sudo arduino-cli compile -u -b $(FQBN) -p $(serial_port) ./

compile:
	sudo arduino-cli compile -b $(FQBN) ./

list:
	sudo arduino-cli board list

monitor:
	alacritty -e sudo screen $(serial_port) $(baud_rate) # look into sudo arduino-cli monitor -p /dev/ttyACM0
