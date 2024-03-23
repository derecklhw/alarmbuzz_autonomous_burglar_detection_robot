#include <Servo.h>

Servo servoX; // horizontal servo
Servo servoY; // vertical servo

int posX = 90; // initial position of the horizontal servo
int posY = 0;  // initial position of the vertical servo

void setup()
{
    servoX.attach(3);   // attach the horizontal servo to pin 9
    servoY.attach(2);  // attach the vertical servo to pin 10
}

void loop()
{
    servo_start();

    servo_sweep();

    servo_end();
    delay(1000);
}

void servo_start()
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

void servo_sweep()
{
    unsigned long start_time = millis(); // get the current time
    while (millis() - start_time < 10000)
    { // run the loop for 10 seconds

        for (posX = posX; posX <= 180; posX += 1)
        {
            servoX.write(posX); // move the horizontal servo
            delay(50);          // delay between movements
        }
        for (posX = posX; posX >= 0; posX -= 1)
        {
            servoX.write(posX); // move the horizontal servo
            delay(50);          // delay between movements
        }
    }
}

void servo_end()
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