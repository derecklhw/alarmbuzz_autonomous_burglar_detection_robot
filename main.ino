void setup() 
{
    Serial.begin(9600);
    // wait for serial port to connect
    while (!Serial){
   
  }
}

void loop() {
  if (Serial.available() > 0) {
    String inputString = Serial.readStringUntil('\n');
    if (inputString == "run") {
   
    }
  }
}
