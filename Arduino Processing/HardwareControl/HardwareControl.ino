int buttonFront = 3;
int buttonRear = 2;

int previousFrontState;
int previousRearState;

int currentFrontState;
int currentRearState;

int previousFrontTime;
int previousRearTime;

int debounceTime = 5;

int shotStart = 0;
int shotComplete = 0;

int totalReturnTime = 0;
int shotSkew = 0;
int skewTarget = 4;
bool skewBypass = false;

int shotCompleteTime = 0;
int shotStartTime = 0;

int shotBlowBackData[1000] = { 0 };
int shotCycleData[1000] = { 0 };

bool sendResults = true;
bool beginLogging = true;


void setup() {
  Serial.begin(9600);
  pinMode(buttonFront, INPUT_PULLUP);
  pinMode(buttonRear, INPUT_PULLUP);

  TCCR1A = 0;
  TCCR1B = bit(CS10);
  TCNT1 = 0;

  unsigned int cycles = TCNT1;
  Serial.println((cycles - 1) / 16);
}


void loop() {

  int currentTime = millis();
  while ((shotSkew < skewTarget) || (skewBypass == true)) {
    int currentTime = millis();
    currentFrontState = digitalRead(buttonFront);
    currentRearState = digitalRead(buttonRear);
    if ((currentTime - previousFrontTime) > debounceTime) {
      if (currentFrontState != previousFrontState) {
        if (currentFrontState == 1) {
          shotStart++;
          shotSkew++;
          shotStartTime = millis();
          beginLogging = true;
        }
        if (currentFrontState == 0) {
          totalReturnTime = millis();
          shotCycleData[shotStart] = (totalReturnTime - shotStartTime);
        }
        previousFrontState = currentFrontState;
        previousFrontTime = millis();
      }
    }
    if ((currentTime - previousRearTime) > debounceTime) {
      if (currentRearState != previousRearState) {
        if (currentRearState == 0) {
          shotComplete++;
          shotSkew = 0;
          shotCompleteTime = millis();
          shotBlowBackData[shotStart] = (shotCompleteTime - shotStartTime);
        }
        previousRearState = currentRearState;
        previousRearTime = millis();
      }
    }
  }
  if (sendResults == true) {
    Serial.println("ShotNumber BlowbackTime CycleTime");
    for (int i = 0; i < shotStart - 1; i++) {
      Serial.println((String)(i + 1) + " " + (String)shotBlowBackData[i + 1] + " " + (String)shotCycleData[i + 1]);
      sendResults = false;
    }
  }
}
