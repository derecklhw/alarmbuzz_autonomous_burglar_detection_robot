#include <Servo.h>

Servo servoX; // horizontal servo
Servo servoY; // vertical servo

int posX = 90; // initial position of the horizontal servo
int posY = 0;  // initial position of the vertical servo

void setup()
{
    servoX.attach(9);   // attach the horizontal servo to pin 9
    servoY.attach(10);  // attach the vertical servo to pin 10
}

void loop()
{
    for (posY = 0; posY <= 90; posY += 1)
    {
        servoY.write(posY); // move the vertical servo
        delay(15);          // delay between movements
    }

    for (posX = 90; posX >= 0; posX -= 1)
    {
        servoX.write(posX); // move the horizontal servo
        delay(15);          // delay between movements
    }

    unsigned long start_time = millis(); // get the current time
    while (millis() - start_time < 10000)
    { // run the loop for 10 seconds

        for (posX = 0; posX <= 180; posX += 1)
        {
            servoX.write(posX); // move the horizontal servo
            delay(15);          // delay between movements
        }
        for (posX = 180; posX >= 0; posX -= 1)
        {
            servoX.write(posX); // move the horizontal servo
            delay(15);          // delay between movements
        }
    }

    // stop the servos and wait for 1 second before starting the next loop
    for (posX = posX; posX <= 90; posX += 1)
    {
        servoX.write(posX); // move the horizontal servo
        delay(15);          // delay between movements
    }

    for (posY = 90; posY >= 0; posY -= 1)
    {
        servoY.write(posY); // move the vertical servo
        delay(15);          // delay between movements
    }
    delay(1000);
}
