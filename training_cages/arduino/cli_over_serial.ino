long linuxBaud = 250000;

void setup() {
    SERIAL_PORT_USBVIRTUAL.begin(115200);
    SERIAL_PORT_HARDWARE.begin(linuxBaud);
}

void loop() {
    int c = SERIAL_PORT_HARDWARE.read();
    if (c != -1) {
        SERIAL_PORT_USBVIRTUAL.write(c);
    }

    c = SERIAL_PORT_USBVIRTUAL.read();
    if (c != -1) {
        SERIAL_PORT_HARDWARE.write(c);
    }
}
