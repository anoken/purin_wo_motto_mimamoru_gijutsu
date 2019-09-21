// Copyright (c) 2019 aNoken 
// https://anoken.jimdo.com/
// https://github.com/anoken/purin_wo_motto_mimamoru_gijutsu
// Arduino IDE compile code

#include <M5Stack.h>
HardwareSerial serial_ext(2);

void setup() {
  M5.begin();
  serial_ext.begin(115200, SERIAL_8N1, 17, 16);
}

void loop() {
  const int thresh = 1000;
  M5.update();
  if ( serial_ext.available() > 0 ) {
    String str = serial_ext.readStringUntil('\n');
    int data = str.toInt();
    Serial.print("data:");
    Serial.println(data);
    if (data > thresh) {
      Serial.print("異常が発生しました");
    }
  }

  vTaskDelay(10 / portTICK_RATE_MS);
}
