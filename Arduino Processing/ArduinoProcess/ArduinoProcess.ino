#include <Wire.h>

int zeroValue = 0;


bool config_uploaded = false;
bool calibrating = false;


String shotInterval;

void setup() {
  Serial.begin(115200);
  Wire.begin();
  Wire.setClock(400000);

  Serial.println("SR");

  byte data[2];
  String configString;
  int intervalIndex;
  int shotIndex;

  char startFlags[2] = {'C', 'R'};
  char intervalFlags[2] = { 'S', 'I' };
  char countFlags[2] = { 'B', 'N' };

  while (!config_uploaded) {
    if (Serial.available() > 0) {
      configString = Serial.readStringUntil('\n');
      if (configString[0] == startFlags[0] and configString[1] == startFlags[1]) {
        Serial.println("entering config");
        config_uploaded = true;
      }
    }
  }
  Serial.println(configString);

  int index1 = configString.indexOf(intervalFlags[0]);
  int index2 = configString.indexOf(intervalFlags[1]);
  String intervalString = configString.substring(index1 + 1, index2);
  Serial.println(intervalString);

  int index3 = configString.indexOf(countFlags[0]);
  int index4 = configString.indexOf(countFlags[1]);
  String countString = configString.substring(index3 + 1, index4);
  Serial.println(countString);

  Serial.println("CU");





  while (!calibrating) {
    if (Serial.available() > 0) {
      String msg = Serial.readString();
      Serial.println("CC");
      for (int i = 0; i < 100; i++) {
        zeroValue += conversion();
      }
      zeroValue = zeroValue / 100;
    }
  }
  Serial.println(zeroValue);
}

void loop() {

  Serial.println(zeroValue);
}


void configureADS1115() {
  // Compile write data configure ADS1115
  Wire.beginTransmission(0b01001000);  // Communicate with ADS1115 slave address
  Wire.write(0b00000001);              // Select config register on ADS1115
  Wire.write(0b10001110);              // Configure config register byte 1
  Wire.write(0b11100011);              // Configure config register byte 2
  // Send the configuration data. ADS1115 is now configured
  Wire.endTransmission();
  // Compile write data to request data from ADS1115
  Wire.beginTransmission(0b01001000);
  Wire.write(0b00000000);  // Select conversion data register
  Wire.endTransmission();  // Send the request for data
}


int16_t conversion() {
  // Send read request to ADS1115
  Wire.requestFrom(0b01001000, 2);
  uint8_t MSB = Wire.read();
  uint8_t LSB = Wire.read();
  int16_t data = LSB | (MSB << 8);
  return data;
}
