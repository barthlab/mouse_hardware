#include <FileIO.h>

//String filename;

const char filename = "/mnt/sda1/arduino/www/asdf.txt";

void setup() {
    // https://docs.arduino.cc/retired/archived-libraries/YunBridgeLibrary
    Bridge.begin();
    FileSystem.begin();
}

void loop() {
    FileSystem.remove(filename);
    // open the file
    File dataFile = FileSystem.open(filename, FILE_APPEND);
    // if the file is available, write to it
    if (dataFile) {
        dataFile.println("Starting");
        dataFile.close();
    }
}

