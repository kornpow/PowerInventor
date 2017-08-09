#include <max6675.h>


int thermoDO = 13;
int thermoCS1 = 3;
int thermoCS2 = 11;
int thermoCLK = 12;

MAX6675 thermocouple1(thermoCLK, thermoCS1, thermoDO);
MAX6675 thermocouple2(thermoCLK, thermoCS2, thermoDO);
int vccPin = 3;
int gndPin = 2;

void setup() {
  Serial.begin(9600);
  // use Arduino pins
  
  // wait for MAX chip to stabilize
  delay(500);
}

void loop() {
  // basic readout test, just print the current temp

//  Serial.print("Therm1:");
//  Serial.println(thermocouple1.readFahrenheit());
//  Serial.print("Therm2:");
  Serial.println(thermocouple2.readFahrenheit());

  delay(1000);
}
