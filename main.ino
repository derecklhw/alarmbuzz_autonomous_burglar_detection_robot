#include <Servo.h>

Servo servoX; // horizontal servo
Servo servoY; // vertical servo

const int servoXPin = 3; // attach the horizontal servo to pin 3
const int servoYPin = 2; // attach the vertical servo to pin 2

int posX = 90; // initial position of the horizontal servo
int posY = 60; // initial position of the vertical servo

// Motor A connections
const int enA = 9;
const int in1 = 5;
const int in2 = 6;

// Motor B connections
const int enB = 10;
const int in3 = 7;
const int in4 = 8;

// Set the speed (0 = off and 255 = max speed)
const int motorSpeed = 255;

// Ultrasonic connections
#define Trigger A1
#define Echo A2

// PIR sensor connection
int ledPin = 13;    // choose the pin for the LED
int inputPin = 4;   // choose the input pin (for PIR sensor)
int pirState = LOW; // we start, assuming no motion detected
int val = 0;        // variable for reading the pin status

// Buzzer connection
const int buzzer = 11;

// Function prototypes
boolean start_flag = false;
boolean stop_flag = false;

void setup()
{
    Serial.begin(9600);

    setupMotorPins();
    setupUltrasonicPins();
    setupPirSensorPins();
    setupServoPins();
    pinMode(buzzer, OUTPUT);

    // Wait for serial port to connect
    while (!Serial)
    {
        ;
    }
}

void loop()
{
    if (checkSerialCommand())
    {
        return;
    }

    if (start_flag && !stop_flag)
    {
        manageMotionDetection();
        avoidObstacle();
    }
}

/*
 * Check Serial Command
 */
boolean checkSerialCommand()
{
    if (Serial.available() > 0)
    {
        String serialInput = Serial.readStringUntil('\n');
        serialInput.trim();
        // "stop" command
        if (serialInput == "stop")
        {
            start_flag = false;
            stop_flag = true;
            sweepEnd();
            stopAll();
            return true;
        }
        // "start" command
        else if (serialInput == "start")
        {
            start_flag = true;
            stop_flag = false;
            randomSeed(analogRead(3));
            goForward();
            return true;
        }
        // "human" command
        else if (serialInput == "intruder")
        {
            sweepEnd();
            buzzerTone();
            return true;
        }
        // "owner" command
        else if (serialInput == "owner")
        {
            sweepEnd();
            return true;
        }
    }
    return false;
}

/*
 * Manage Motion Detection
 */
void manageMotionDetection()
{
    val = digitalRead(inputPin); // read input value
    if (val == HIGH && pirState == LOW)
    {
        digitalWrite(ledPin, HIGH); // turn LED ON
        pirState = HIGH;
        performSweep();
    }
    else if (val == LOW && pirState == HIGH)
    {
        digitalWrite(ledPin, LOW); // turn LED OFF
        pirState = LOW;
        goForward();
    }
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
 * Obstacle detected, avoid it
 */
void avoidObstacle()
{
    int distance = doPing();

    // If obstacle <= 10 inches away
    if (distance >= 0 && distance <= 10)
    {
        // Serial.println("Obstacle detected ahead");
        goBackwards(); // Move in reverse
        delay(1000);

        // Go left or right to avoid the obstacle*/
        // Generates 0 or 1, randomly
        if (random(2) == 0)
        {
            goRight(); // Turn right
        }
        else
        {
            goLeft(); // Turn left
        }
        delay(1500);
        goForward(); // Move forward
    }
    delay(50); // Wait 50 milliseconds before pinging again
}

/*
 * Perform Sweep action
 */
void performSweep()
{
    stopAll();
    delay(200);
    sweepStart();
    Serial.println("motion");
    sweepRunning();
    sweepEnd();
}

/*
 * Sweep Start movement
 */
void sweepStart()
{
    for (posY = posY; posY <= 60; posY += 1)
    {
        servoY.write(posY); // move the vertical servo
        delay(50);
    }

    for (posX = posX; posX >= 0; posX -= 1)
    {
        servoX.write(posX); // move the horizontal servo
        delay(50);
    }
}

/*
 * Sweep Running movment
 */
void sweepRunning()
{
    for (posX = posX; posX <= 180; posX += 1)
    {
        servoX.write(posX); // move the horizontal servo
        delay(75);

        if (checkSerialCommand())
        {
            return;
        }
    }
    for (posX = posX; posX >= 0; posX -= 1)
    {
        servoX.write(posX); // move the horizontal servo
        delay(75);

        if (checkSerialCommand())
        {
            return;
        }
    }
}

/*
 * Sweep End Movement
 */
void sweepEnd()
{
    // Ensure posX returns to 90 degrees
    if (posX > 90)
    {
        for (; posX >= 90; posX -= 1)
        {
            servoX.write(posX); // move the horizontal servo
            delay(50);
        }
    }
    else if (posX < 90)
    {
        for (; posX <= 90; posX += 1)
        {
            servoX.write(posX); // move the horizontal servo
            delay(50);
        }
    }

    // Then move posY back to 0
    for (posY = posY; posY >= 60; posY -= 1)
    {
        servoY.write(posY); // move the vertical servo
        delay(50);
    }
}

/*
 * Buzzer emit sounds
 */
void buzzerTone()
{
    tone(buzzer, 1000); // Send 1KHz sound signal...
    delay(1000);
    noTone(buzzer); // Stop sound...
    delay(1000);
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
 * Setup Servo Pins
 */
void setupServoPins()
{
    servoX.attach(servoXPin);
    servoY.attach(servoYPin);

    servoY.write(posY);
    servoX.write(posX);
}
