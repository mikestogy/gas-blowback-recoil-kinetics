bool experimentReceived = false;

void setup() {
  Serial.begin(115200);
  Serial.println("Serial Ready");

  while (!experimentReceived){
    if(Serial.available() > 0){
      String msg = Serial.readString();
      Serial.println("Experiment Received");
    }
  }

}

void loop() {
  // put your main code here, to run repeatedly:

}
