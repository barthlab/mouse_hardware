#include <FileIO.h>

const char filename = "/mnt/sda1/arduino/www/asdf.txt";

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
  Bridge.begin();
  digitalWrite(LED_BUILTIN, HIGH);
  Serial.begin(9600);
  FileSystem.begin();
}

void loop() {
  FileSystem.remove(filename);
  Serial.println("removed");
  // open the file
  File dataFile = FileSystem.open(filename, FILE_APPEND);
  Serial.println("opened");
  // if the file is available, write to it
  if (dataFile) {
    Serial.println("writing");
    dataFile.println("writing");
    dataFile.close();
  } else {
    Serial.println("error: not writing");
    Serial.println(dataFile);
  }
  delay(1000);
}

