// Copyright (c) 2019 aNoken
// https://twitter.com/anoken2017
// Arduino IDE compile code

#include <M5StickC.h>
#include <WiFi.h>
#include "Ambient.h" // Ambient Header
//RTC Define
RTC_TimeTypeDef RTC_TimeStruct;
RTC_DateTypeDef RTC_DateStruct;

//Wi-Fi Define
const char* ssid       = "your_ssid";
const char* password   = "your_passwd";
const char* ntpServer =  "ntp.nict.jp";

//LCD Display Define
TFT_eSprite *Spr;
uint32_t front_col = TFT_BLACK;
uint32_t back_col = TFT_YELLOW;

//Fuinction Define
void wifi_connect();
String ZeroPad(int num);
uint16_t getColor(uint8_t red, uint8_t green, uint8_t blue);

//Set Target_time
int Target_Hours = 17;
int Target_Minutes = 0;

HardwareSerial serial_ext(2);
int data = -1;


WiFiClient client;
Ambient ambient; // Ambient
unsigned int channelId = 00000 ; // Ambient
const char* writeKey = "000000000000000"; // 

void setup() {
  M5.begin();
  M5.Lcd.setRotation(3);
  pinMode(32, OUTPUT);
  pinMode(33, OUTPUT);
  pinMode(M5_BUTTON_HOME, INPUT_PULLUP);
  pinMode(M5_BUTTON_RST, INPUT_PULLUP);
  M5.Axp.ScreenBreath(10);

  //Wi-Fi Connect
  wifi_connect();

  //NTP TimeScale
  configTime(9 * 3600, 0, ntpServer);

  //GET NOW TIME
  struct tm timeInfo;
  if (getLocalTime(&timeInfo)) {
    Serial.println("ntpServer:");
    Serial.println(ntpServer);

    // Initialize RTC time
    RTC_TimeTypeDef TimeStruct;
    TimeStruct.Hours   = timeInfo.tm_hour;
    TimeStruct.Minutes = timeInfo.tm_min;
    TimeStruct.Seconds = timeInfo.tm_sec;
    M5.Rtc.SetTime(&TimeStruct);

    // Initialize RTC Date
    RTC_DateTypeDef DateStruct;
    DateStruct.WeekDay = timeInfo.tm_wday;
    DateStruct.Month = timeInfo.tm_mon + 1;
    DateStruct.Date = timeInfo.tm_mday;
    DateStruct.Year = timeInfo.tm_year + 1900;
    M5.Rtc.SetData(&DateStruct);
  }

  //LCD Splite Initialize
  Spr = new TFT_eSprite(&M5.Lcd);
  Spr->setColorDepth(8);
  Spr->createSprite(320, 240);
  Spr->setBitmapColor(front_col, back_col);

  serial_ext.begin(115200, SERIAL_8N1, 32, 33);

  ambient.begin(channelId, writeKey, &client);

}

void loop() {
  M5.update();
  if ( serial_ext.available() > 0 ) {
    String str = serial_ext.readStringUntil('\n');
    data = str.toInt();
    Serial.print("data:");
    Serial.println(data);

    //Send to Ambient
    ambient.set(1, data);
    ambient.send();
  }



  //Get RTC
  M5.Rtc.GetTime(&RTC_TimeStruct);
  M5.Rtc.GetData(&RTC_DateStruct);

  int Target_Seconds = 30;
  bool state = 0;

  if ((Target_Hours == RTC_TimeStruct.Hours) && (Target_Minutes == RTC_TimeStruct.Minutes) && (Target_Seconds > RTC_TimeStruct.Seconds)) {
    state = 1;
  }
  if (state)  {
    Spr->fillSprite(getColor(255, 0, 0));
    Spr->setTextColor(getColor(0, 0, 0), getColor(255, 0, 0));
  }
  else {
    Spr->fillSprite(getColor(255, 255, 0));
    Spr->setTextColor( getColor(0, 0, 0), getColor(255, 255, 0));
  }

  //Now Time Display
  Spr->setTextSize(1);
  //String date_str = String("") + String(ZeroPad(RTC_DateStruct.Year)) + String("/") + String(ZeroPad(RTC_DateStruct.Month)) + String("/") + String(ZeroPad(RTC_DateStruct.Date));
  //Spr->drawString(date_str, 10, 15, 4);
  String time_str = String("") + String(ZeroPad(RTC_TimeStruct.Hours)) + String(":") + String(ZeroPad(RTC_TimeStruct.Minutes)) + String(":") + String(ZeroPad(RTC_TimeStruct.Seconds));
  Spr->drawString(time_str, 10, 15, 4);

  String act_str = String("ACT:") + String(data);
  Spr->drawString(act_str, 10, 45, 4);


  Spr->pushSprite(0, 0);

  //LED Flashes regularly
  static unsigned long old_time = millis();
  unsigned long time = millis();
  unsigned long interval = 1000;
  if (state) {

    //LED Light Flash By Grove Port
    unsigned long dtime = time - old_time;
    if (RTC_TimeStruct.Seconds > 15) {
      interval = 500;
    }
    if (RTC_TimeStruct.Seconds > 20) {
      interval = 200;
    }
    if (RTC_TimeStruct.Seconds > 25) {
      interval = 100;
    }
    if (dtime < interval / 2) {
      digitalWrite(32, HIGH);
      digitalWrite(33, HIGH);
    }
    else if (dtime >= interval / 2) {
      digitalWrite(32, LOW);
      digitalWrite(33, LOW);
    }
    if (dtime > interval) {
      old_time = time;
    }

  }
  else {
    //LED Light OFF By Grove Port
    digitalWrite(32, LOW);
    digitalWrite(33, LOW);
  }
  vTaskDelay(10 / portTICK_RATE_MS);

}

//Get 24Bit Color -> 16Bit Color
uint16_t getColor(uint8_t red, uint8_t green, uint8_t blue) {
  return ((red >> 3) << 11) | ((green >> 2) << 5) | (blue >> 3);
}

//Wi-Fi Connect
void wifi_connect() {

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)  delay(500);
  Serial.println(WiFi.localIP());
}

//String ZeroPad
String ZeroPad(int num) {
  char buf[8];
  sprintf(buf, "%02d", num);
  String bud_str = buf;
  return bud_str;
}
