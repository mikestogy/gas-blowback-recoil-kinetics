#include <Wire.h>

float zeroValue = 0;
bool config_uploaded = false;
bool calibrating = false;
String shotInterval;

void setup() {
  Serial.begin(115200);
  pinMode(9, OUTPUT);
  pinMode(2, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(2), isr, CHANGE);
  //attachInterrupt(digitalPinToInterrupt(2), isr2, RISING);
  digitalWrite(9, LOW);
  Wire.begin();
  Wire.setClock(400000);
  Serial.println("SR");

  byte data[2];
  String configString;
  int intervalIndex;
  int shotIndex;

  char startFlags[2] = { 'C', 'R' };
  char intervalFlags[2] = { 'S', 'I' };

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

  Serial.println("CU");

  while (!calibrating) {
    if (Serial.available() > 0) {
      String msg = Serial.readStringUntil('\n');
      if (msg[0] == 'B' and msg[1] == 'C') {
        calibrating = true;
      }
    }
  }

  configureADS1115();
  for (int i = 0; i < 10000; i++) {
    zeroValue += conversion();
  }
  zeroValue = zeroValue / 10000;
  Serial.println("CC");

  Serial.println(zeroValue);
  delay(2000);
}

int button1Prev = 0;
int button2Prev = 0;
bool blowbackStatus = false;
int previousTime = 0;
int shotCount = 0;
void loop() {

  // internal shot counter
  // report load cell data with shot number
  // time, shot number, load cell data

  // shot starts when forward bolt switch opens
  // shot ends when forward sled closes
  // while forward bolt open, record load cell until forward sled closes

  while (blowbackStatus == true) {
  Serial.println((String)shotCount + " " +conversion());
  }

}

void isr() {
  int currentTime = millis();
  if (currentTime - previousTime > 1) {
    if (digitalRead(2) == 1) {
      blowbackStatus = false;
    } else {
      blowbackStatus = true;
      shotCount++;
    }
    previousTime = currentTime;
  }
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
