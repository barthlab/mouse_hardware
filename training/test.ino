#include <FileIO.h>

//String filename;

const char filename = "/mnt/sda1/arduino/www/asdf.txt";

void setup() {
  Bridge.begin();
}

void loop() {
  FileSystem.begin();
  FileSystem.remove(filename);
  // open the file
  File dataFile = FileSystem.open(filename, FILE_APPEND);
  // if the file is available, write to it
  if (dataFile) {
    dataFile.println("Starting");
    dataFile.close();
  }
}

