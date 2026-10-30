#include <Arduino.h>

void setup() {                                    // runs once at power-on

    Serial.begin(115200);                         //open USB serial at 115200 baud
    Serial.println("This is the source code!");

}

void loop() {                                     // runs forever, again and again

}