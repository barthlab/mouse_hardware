#include <FileIO.h>

// PINS
const int REAL_AIR_PIN = 7;
const int FAKE_AIR_PIN = 2;
const int REAL_WATER_PIN = 8;
const int FAKE_WATER_PIN = 10;
const int IR_SENSOR_PIN = 4;
const int LICK_CAPACITIVE_SENSOR_PIN = 11;
const int DISCONNECTED_ANALOG_PIN_0 = 14;

// File Save Dir
const char storage_file_dir = "/mnt/sda1/arduino/www/temptest.txt"; // TODO redo filename
char storage_file;

// USER Modifiable Variables
const unsigned long probability_of_water = 80; // %
const unsigned long min_delay_time = 200; // milliseconds
const unsigned long max_delay_time = 800; // milliseconds
const unsigned long air_puff_time = 500; // milliseconds
const unsigned long water_release_time = 75; // milliseconds
const unsigned long air_puff_end_to_water_release_start_time = 500; // milliseconds
const unsigned long water_release_end_to_check_IR_blocked_time = 725; // milliseconds

// reading from a pin that isn't attached to anything gives us a random value
// the value is more likely to be unbiased the smaller the bit is because
// smaller random variations lead to larger changes, so we use the smallest
// bit of a disconnected analog pin
bool get_random_bit(const int DISCONNECTED_ANALOG_PIN) {
    return (1 & analogRead(DISCONNECTED_ANALOG_PIN));
}

// use get_random_bit to make a random unsigned long (which is what randomSeed takes in)
unsigned long get_random_UL(const int DISCONNECTED_ANALOG_PIN) {
    const int number_of_bits_in_UL = 32;
    unsigned long out = 0;
    for (int i = 0; i < number_of_bits_in_UL; i++) {
        out |= get_random_bit(DISCONNECTED_ANALOG_PIN);
        out << 1;
    }
    return (out);
}

String getCleanedTimeStamp() {
    String result;
    Process get_time;
    get_time.begin("date");
    get_time.addParameter("+%D-%T");
    // format: MM/DD/YY-HH:MM:SS
    // TODO assumes dragino has an internet connection
    get_time.run();

    // read the output of the command
    while (get_time.available() > 0) {
        char c = get_time.read();
        if (c != '\n') {
            result += c;
        }
    }

    result.replace("/", "_");
    result.replace("-", "~T~");
    result.replace(":", "_");
    // format: MM_DD_YY~T~HH_MM_SS

    return result;
}

void setup() {
    pinMode(REAL_AIR_PIN, INPUT);
    pinMode(FAKE_AIR_PIN, INPUT);
    pinMode(REAL_WATER_PIN, INPUT);
    pinMode(FAKE_WATER_PIN, INPUT);
    pinMode(IR_SENSOR_PIN, INPUT);
    pinMode(LICK_CAPACITIVE_SENSOR_PIN, INPUT);
    pinMode(DISCONNECTED_ANALOG_PIN_0, INPUT);

    // TODO why are we making IR_SENSOR_PIN pull up?
    digitalWrite(IR_SENSOR_PIN, HIGH);

    // TODO redo format
    String cleaneddatetime = getCleanedTimeStamp();

    // create storage_file string
    storage_file = (storage_file_dir + cleaneddatetime + ".txt").c_str();


    // https://docs.arduino.cc/retired/archived-libraries/YunBridgeLibrary
    Bridge.begin();
    FileSystem.begin();

    // read an analog pin that is not connected to get a random number
    randomSeed(get_random_UL(DISCONNECTED_ANALOG_PIN_0));

// TODO ???
//    while (digitalRead(LICKPIN)) { //if the lick pin is on when the arduino is initializing then delay so voltage can stabilize
//        delay(1000);
//    }
}

void write_data(char filename, String input_string) {
    File data_file = FileSystem.open(filename, FILE_APPEND);
    if (data_file) {
        data_file.println(input_string.c_str());
        data_file.close();
    }
}

void loop() {
    if (!digitalRead(IR_SENSOR_PIN)) {
        unsigned long real = random(100) < probability_of_water;
        unsigned int air_pin = REAL_AIR_PIN ? real : FAKE_AIR_PIN;
        unsigned int water_pin = REAL_WATER_PIN ? real : FAKE_WATER_PIN;
        // NOTE: can have issue if max_delay_time + 1 overflows
        unsigned long random_delay_time = (unsigned long) random(min_delay_time, max_delay_time + 1);

        // TODO redo data format (time (millis?), digitalRead(IR_SENSOR_PIN), digitalRead(LICK_CAPACITIVE_SENSOR_PIN), random_delay_time)

        // TODO verify that write_data takes on the order of microseconds
        write_data(storage_file, String(millis() / 1000) + "," + String(digitalRead(IR_SENSOR_PIN)) + "," + String(digitalRead(LICK_CAPACITIVE_SENSOR_PIN) << 1) + "," + (real ? "3" : "9") + "," + "0");

        delay(random_delay_time);

        digitalWrite(air_pin, HIGH);
        write_data(storage_file, String(millis() / 1000) + "," + String(digitalRead(IR_SENSOR_PIN)) + "," + String(digitalRead(LICK_CAPACITIVE_SENSOR_PIN) << 1) + "," + (real ? "4" : "9") + "," + "0");
        delay(air_puff_time);
        digitalWrite(air_pin, LOW);

        delay(air_puff_end_to_water_release_start_time);

        digitalWrite(water_pin, HIGH);
        write_data(storage_file, String(millis() / 1000) + "," + String(digitalRead(IR_SENSOR_PIN)) + "," + String(digitalRead(LICK_CAPACITIVE_SENSOR_PIN) << 1) + "," + (real ? "5" : "9") + "," + "0");
        delay(water_release_time);
        digitalWrite(water_pin, LOW);

        write_data(storage_file, String(millis() / 1000) + "," + String(digitalRead(IR_SENSOR_PIN)) + "," + String(digitalRead(LICK_CAPACITIVE_SENSOR_PIN) << 1) + "," + (real ? "7" : "9") + "," + "0");

        delay(water_release_end_to_check_IR_blocked_time);

        // wait until mouse has stopped being in the IR beam
        while (!digitalRead(IR_SENSOR_PIN)) {};
    }
}

