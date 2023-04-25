import processing.serial.*;
//import controlP5.*;

Serial myPort; 
PrintWriter output;
int value;
int [] dataIn;
int j; 
String d;
//float ms;
int dy = day(); int mon = month(); int y = year();
int sec = second(); int min = minute(); int hr = hour();
String tlt;
void setup()
{
  print(Serial.list());
  String portName = Serial.list()[6];
  myPort = new Serial(this, portName, 9600);
  tlt = "E:/Mo Zhu/S1 L23 awake imaging/SST-creAi93/ACC/230412 NUF_5F/230419 NUF_5F ACC day1/230419_Arduino_P6_2 1.csv";
  //tlt = "E:/Mo Zhu/S1 L23 awake imaging/SST-creAi93/SAT/Homecage/230206 NOT_4M/230218 NOT_4M ACC day6/230218_Arduino_P6_2 2.csv";
  //tlt = "E:/Mo Zhu/S1 L23 awake imaging/SST-creAi93/DREADD/230227 NOT_8F (ACC8) - CNO control; no hM4Di/230227_Arduino_5hrs post CNO_P6_2.csv"; 
  //tlt = "E:/Mo Zhu/S1 L23 awake imaging/SST-creAi93/DREADD/220913 MTJ_F_NC (ACC2)/220913_Arduino_5hrs post CNO P6_2.csv"; 
  output = createWriter(tlt); // can save to dif folder with full pth///change to .csv
  dataIn = new int[5];
  //ms = millis();
}
void draw()
{
  while (myPort.available()>0)
  {

    d = myPort.readStringUntil('\n');
    if (d!= null) {
      //println(d);
      output.println(d);
      output.flush();  // Writes the remaining data to the file
      //output.close();  // Finishes the file
    }
  }
}
