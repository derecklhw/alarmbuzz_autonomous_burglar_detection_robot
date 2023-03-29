#include <Servo.h>

Servo servoX; // horizontal servo
Servo servoY; // vertical servo

const int servoXPin = 3; // attach the horizontal servo to pin 3
const int servoYPin = 2; // attach the vertical servo to pin 2

int posX = 90; // initial position of the horizontal servo
int posY = 0;  // initial position of the vertical servo

// Motor A connections
const int enA = 9;
const int in1 = 5;
const int in2 = 6;

// Motor B connections
const int enB = 10;
const int in3 = 7;
const int in4 = 8;

// Set the speed (0 = off and 255 = max speed)
// If your wheels are not moving, check your connections,
// or increase the speed.
const int motorSpeed = 255;

// Ultrasonic connections
#define Trigger A1
#define Echo A2

// PIR sensor connection
int ledPin = 13;    // choose the pin for the LED
int inputPin = 4;   // choose the input pin (for PIR sensor)
int pirState = LOW; // we start, assuming no motion detected
int val = 0;        // variable for reading the pin status

const int buzzer = 11; // buzzer to arduino pin 11

boolean start_flag = false;

void setup() 
{
    Serial.begin(9600);

    setupMotorPins();
    setupUltrasonicPins();
    setupPirSensorPins();

    servoX.attach(servoXPin);   
    servoY.attach(servoYPin);

    servoY.write(posY); 
    servoX.write(posX);

    pinMode(buzzer, OUTPUT);

    // Wait for serial port to connect
    while (!Serial) {
        ;
    }
}

void loop() {
    if (Serial.available() > 0 ) {
        // Read incoming data
        String input = Serial.readStringUntil('\n');

        // Perform action based on the input
        if (input == "start") {
            start_flag = true;
            randomSeed(analogRead(3));
            delay(200); // Pause 200 milliseconds
            goForward(); // Go forward
        } else if (input == "stop") {
            // Stop execution of code
            start_flag = false;
            delay(200); // Pause 200 milliseconds
            stopAll(); // Stop all
        }
    }

    if (start_flag) {
        val = digitalRead(inputPin); // read input value
        if (val == HIGH)
        {                             // check if the input is HIGH
            digitalWrite(ledPin, HIGH); // turn LED ON
            if (pirState == LOW)
            {
            // we have just turned on
            // We only want to print on the output change, not state
            pirState = HIGH;
            stopAll();
            delay(200);

            sweepStart();
            Serial.println("motion");
            sweepRunning();
            sweepEnd();
            }
        }
        else
        {
            digitalWrite(ledPin, LOW); // turn LED OFF
            if (pirState == HIGH)
            {
            // we have just turned of
            // Serial.println("Motion ended!");
            // We only want to print on the output change, not state
            pirState = LOW;
            goForward();
            }
        }       
        avoidObstacle();
    }
}

/*
* Setup Motor Pins
*/
void setupMotorPins()
{
    // Motor control pins are outputs
    pinMode(enA, OUTPUT);
    pinMode(enB, OUTPUT);
    pinMode(in1, OUTPUT);
    pinMode(in2, OUTPUT);
    pinMode(in3, OUTPUT);
    pinMode(in4, OUTPUT);

    // Turn off motors - Initial state
    digitalWrite(in1, LOW);
    digitalWrite(in2, LOW);
    digitalWrite(in3, LOW);
    digitalWrite(in4, LOW);

    // Set the motor speed
    analogWrite(enA, motorSpeed);
    analogWrite(enB, motorSpeed);
}

/* 
* Setup Ultrasonic Pins
*/
void setupUltrasonicPins()
{
    // Define each pin as an input or output for ultrasonic.
    pinMode(Echo, INPUT);
    pinMode(Trigger, OUTPUT);
}

/*
* Setup Pir Sensor Pins 
*/
void setupPirSensorPins()
{
    // Define each pin as an input or output for pir sensor
    pinMode(ledPin, OUTPUT);  // declare LED as output
    pinMode(inputPin, INPUT); // declare sensor as input
}

/*
 * Returns the distance to the obstacle as an integer
 */
int doPing()
{
    int distance = 0;
    int average = 0;

    // Grab four measurements of distance and calculate
    // the average.
    for (int i = 0; i < 4; i++)
    {

        // Make the Trigger LOW (0 volts)
        // for 2 microseconds
        digitalWrite(Trigger, LOW);
        delayMicroseconds(2);

        // Emit high frequency 40kHz sound pulse
        // (i.e. pull the Trigger)
        // by making Trigger HIGH (5 volts)
        // for 10 microseconds
        digitalWrite(Trigger, HIGH);
        delayMicroseconds(10);
        digitalWrite(Trigger, LOW);

        // Detect a pulse on the Echo pin 8.
        // pulseIn() measures the time in
        // microseconds until the sound pulse
        // returns back to the sensor.
        distance = pulseIn(Echo, HIGH);

        // Speed of sound is:
        // 13511.811023622 inches per second
        // 13511.811023622/10^6 inches per microsecond
        // 0.013511811 inches per microsecond
        // Taking the reciprocal, we have:
        // 74.00932414 microseconds per inch
        // Below, we convert microseconds to inches by
        // dividing by 74 and then dividing by 2
        // to account for the roundtrip time.
        distance = distance / 74 / 2;

        // Compute running sum
        average += distance;

        // Wait 10 milliseconds between pings
        delay(10);
    }

    // Return the average of the four distance
    // measurements
    return (average / 4);
}

/*
 *  Forwards, backwards, right, left, stop.
 */
void goForward()
{
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
    digitalWrite(in3, HIGH);
    digitalWrite(in4, LOW);
}
void goBackwards()
{
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
    digitalWrite(in3, LOW);
    digitalWrite(in4, HIGH);
}
void goRight()
{
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
    digitalWrite(in3, LOW);
    digitalWrite(in4, HIGH);
}
void goLeft()
{
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
    digitalWrite(in3, HIGH);
    digitalWrite(in4, LOW);
}
void stopAll()
{
    digitalWrite(in1, LOW);
    digitalWrite(in2, LOW);
    digitalWrite(in3, LOW);
    digitalWrite(in4, LOW);
}

/*
 * Obstacle detected, avoid it
*/
void avoidObstacle()
{
    int distance = doPing();

    // If obstacle <= 16 inches away
    if (distance >= 0 && distance <= 10)
    {
        // Serial.println("Obstacle detected ahead");
        goBackwards(); // Move in reverse
        delay(1000);

        /* Go left or right to avoid the obstacle*/
        if (random(2) == 0)
        {               // Generates 0 or 1, randomly
            goRight(); // Turn right
        }
        else
        {
            goLeft(); // Turn left
        }
        delay(1500);
        goForward(); // Move forward
        // Serial.println("Obstacle detected completed");  
    }
    delay(50); // Wait 50 milliseconds before pinging again
}

/*
 * Sweep Start movement
*/
void sweepStart()
{
    for (posY = posY; posY <= 45; posY += 1)
    {
        servoY.write(posY); // move the vertical servo
        delay(50);          // delay between movements
    }

    for (posX = posX; posX >= 0; posX -= 1)
    {
        servoX.write(posX); // move the horizontal servo
        delay(50);          // delay between movements
    }
}

/* 
* Sweep Running movment 
*/
void sweepRunning()
{
    unsigned long start_time = millis(); // get the current time
    while (millis() - start_time < 10000)
    { // run the loop for 10 seconds

        for (posX = posX; posX <= 180; posX += 1)
        {
            servoX.write(posX); // move the horizontal servo
            delay(50);          // delay between movements

            if (Serial.available() > 0 && Serial.readString() == "human")
            {   
                sweepEnd();
                buzzerTone();
                return;
            }
        }
        for (posX = posX; posX >= 0; posX -= 1)
        {
            servoX.write(posX); // move the horizontal servo
            delay(50);          // delay between movements

            if (Serial.available() > 0 && Serial.readString() == "human")
            {
                sweepEnd();
                buzzerTone();
                return;
            }
        }
    }
}


/*
 * Sweep End Movement
*/
void sweepEnd()
{
    // stop the servos and wait for 1 second before starting the next loop
    for (posX = posX; posX <= 90; posX += 1)
    {
        servoX.write(posX); // move the horizontal servo
        delay(50);          // delay between movements
    }

    for (posY = posY; posY >= 0; posY -= 1)
    {
        servoY.write(posY); // move the vertical servo
        delay(50);          // delay between movements
    }
}

/*
* Buzzer emit sounds 
*/
void buzzerTone()
{
    tone(buzzer, 1000); // Send 1KHz sound signal...
    delay(1000);        // ...for 1 sec
    noTone(buzzer);     // Stop sound...
    delay(1000);        // ...for 1sec
}