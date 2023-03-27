const int buzzer = 9; // buzzer to arduino pin 9

void setup() 
{
    Serial.begin(9600);
    // wait for serial port to connect
    Serial.println("start");
    pinMode(buzzer, OUTPUT); // Set buzzer - pin 9 as an output
    while (!Serial){
    ; //wait for serial port to connect
    }
}

void loop() {
  if (Serial.available() > 0) {
    String inputString = Serial.readStringUntil('\n');
    if (inputString == "run") {
        tone(buzzer, 1000); // Send 1KHz sound signal...
        delay(1000);        // ...for 1 sec
        noTone(buzzer);     // Stop sound...
        delay(1000);        // ...for 1sec
    }
  }
}