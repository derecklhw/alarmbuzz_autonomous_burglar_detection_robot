/*
 * Author: Automatic Addison
 * Website: https://automaticaddison.com
 * Description: Controls the speed and direction of two DC motors.
 */

// Motor A connections
const int enA = 9;
const int in1 = 5;
const int in2 = 6;

// Motor B connections
const int enB = 10;
const int in3 = 7;
const int in4 = 8;

// Set the speed (0 = off and 255 = max speed)
const int motorSpeed = 128;

void setup()
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

void loop()
{

    // Go forwards
    go_forward();
    delay(3000);

    // Go backwards
    go_backwards();
    delay(3000);

    // Go right
    go_right();
    delay(3000);

    // Go left
    go_left();
    delay(3000);

    // Stop
    stop_all();
    delay(3000);
}

/*
 *  Forwards, backwards, right, left, stop.
 */
void go_forward()
{
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
    digitalWrite(in3, HIGH);
    digitalWrite(in4, LOW);
}
void go_backwards()
{
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
    digitalWrite(in3, LOW);
    digitalWrite(in4, HIGH);
}
void go_right()
{
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
    digitalWrite(in3, LOW);
    digitalWrite(in4, HIGH);
}
void go_left()
{
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
    digitalWrite(in3, HIGH);
    digitalWrite(in4, LOW);
}
void stop_all()
{
    digitalWrite(in1, LOW);
    digitalWrite(in2, LOW);
    digitalWrite(in3, LOW);
    digitalWrite(in4, LOW);
}