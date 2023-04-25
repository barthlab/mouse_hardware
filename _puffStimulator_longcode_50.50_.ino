/* ===================================================================

  Air puff stimulator w/ Arduino
  MTM
  170426

  This code will deliver air puff stimulus trains! The built-in LED on
  the arduino will blink when the trial is complete.

  Note that using delay() meangs no other sensor readings, computations,
  or pin manipulations can be made during the delay function. If you add
  any sensors (eg. switch) or calculations (eg. for timing), you cannot
  use delay().

  ====================================================================== */

// define pins
#define CH1 2 // Digital Pin 2 on Arduino to CH1 on Relay Module -> solenoid
#define CH2 7 // Digital Pin 7 on Arduno to CH2 on Relay Module -> TTL
#define CH3 3 // Digital Pin 3 on Arduino to CH3 on Relay Module -> solenoid (FAKE)
#define CH4 4 // Digital Pin 4 on Arduino to CH4 on Relay Module -> water

// variables
// note that everything is in ms
// for trouble shooting or testing, use itinialDelay = 1000, trialDelay = 500, airTime=10, offTime = 250
const long initialDelay = 100000; // a, initial delay between plugging in arduino and first trial start
const long trialDelay = 0; // b, delay between trains
const int airTime = 500; // y, open solenoid duration
const int delay1 = 500;  //delay in-between puff and water
const int waterTime = 75; //time for water duration
const int offTime = 19500; // z, time between end of puff and beginning of next puff within a train
const int puffTrain = 20; // x, number of  puffs in a train
const int numTrains = 1; // n, number of trains in a trial
 //probability of real air puff
unsigned long puffCounter; // counts number of puffs in a train
unsigned long trainCounter; // counts number of trains in a trial

unsigned long ms_on;
unsigned long ms_off;
unsigned long w_on;
unsigned long w_off;
int ct = 0; 
int prob = 50;

void setup() {
  Serial.begin(9600);
  randomSeed(analogRead(A0));
  //Setup all the Arduino Pins
  pinMode(CH1, OUTPUT);
  pinMode(CH2, OUTPUT);
  pinMode(CH3, OUTPUT);
  pinMode(CH4, OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT); // built-in LED

  // Relay
  puffCounter = 0;
  trainCounter = 0;
  digitalWrite(CH1, LOW);
  digitalWrite(CH2, LOW);
  digitalWrite(CH3, LOW);
  digitalWrite(CH4, LOW);
  digitalWrite(LED_BUILTIN, LOW);
  delay(initialDelay); // Wait initialDelay seconds before starting sequence
  // (So you have time to turn on the gas valve)
  // (If you have gas on before plugging in the arduino, you'd just have air leaking...)
}

void loop() {
  if ((puffCounter < puffTrain) && (trainCounter < numTrains)) {
    if (prob < random(100)) {
      digitalWrite(CH1, HIGH); ms_on = millis();// open solenoid
      digitalWrite(CH2, HIGH); // TTL "1" signal
      delay(airTime);
      digitalWrite(CH1, LOW); ms_off = millis(); ct+=1;// close solenoid
      digitalWrite(CH2, LOW); // TTL "0" signal
      delay(delay1);
      digitalWrite(CH4, HIGH);  w_on = millis();
      delay(waterTime);
      digitalWrite(CH4, LOW);  w_off = millis();
      delay(offTime);
      puffCounter += 1;
      Serial.println("Puff, " + String(ct) + ',' + String(ms_on) + ',' + String(ms_off)+ String(w_on) + ',' + String(w_off));
      
    }
    else {
      digitalWrite(CH3, HIGH); ms_on = millis();// open solenoid
      digitalWrite(CH2, HIGH); // TTL "1" signal
      delay(airTime);
      digitalWrite(CH3, LOW); ms_off = millis(); ct+=1;// close solenoid
      digitalWrite(CH2, LOW); // TTL "0" signal
      delay(delay1);
      digitalWrite(CH4, HIGH);  w_on = millis();
      delay(waterTime);
      digitalWrite(CH4, LOW);  w_off = millis();
      delay(offTime);
      puffCounter += 1;
      Serial.println("Blank, " + String(ct) + ',' + String(ms_on) + ',' + String(ms_off)+ String(w_on) + ',' + String(w_off));
    }
   }
  else if (trainCounter < numTrains) {
    puffCounter = 0;
    delay(trialDelay);
    trainCounter += 1;

  }
  else {
    // trial is complete, arduino light blinks
    digitalWrite(LED_BUILTIN, HIGH);
    delay(500);
    digitalWrite(LED_BUILTIN, LOW);
    delay(500);

  }


}


