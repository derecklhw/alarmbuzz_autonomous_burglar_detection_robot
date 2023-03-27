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
const int motorSpeed = 140;

#define Trigger A1
#define Echo A2

boolean start_flag = false;

void setup() 
{
    Serial.begin(9600);

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

    // Define each pin as an input or output.
    pinMode(Echo, INPUT);
    pinMode(Trigger, OUTPUT);

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
            go_forward(); // Go forward
        } else if (input == "stop") {
            // Stop execution of code
            start_flag = false;
            delay(200); // Pause 200 milliseconds
            stop_all(); // Stop all
        }
    }

    // Obstacle detection code
    if (start_flag) {
        int distance = doPing();

        // If obstacle <= 16 inches away
        if (distance >= 0 && distance <= 16)
        {

            // Serial.println("Obstacle detected ahead");
            go_backwards(); // Move in reverse
            delay(2000);

            /* Go left or right to avoid the obstacle*/
            if (random(2) == 0)
            {               // Generates 0 or 1, randomly
                go_right(); // Turn right
            }
            else
            {
                go_left(); // Turn left
            }
            delay(3000);
            go_forward(); // Move forward
        }
        delay(50); // Wait 50 milliseconds before pinging again
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