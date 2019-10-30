// Copyright (c) 2019 aNoken 
// https://anoken.jimdo.com/
// https://github.com/anoken/purin_wo_motto_mimamoru_gijutsu
// Arduino IDE compile code

#include <M5StickC.h>
#include <WiFi.h>
#include <ssl_client.h>
#include <WiFiClientSecure.h>
const char* ssid = "your_ssid";
const char* passwd = "your_passwd";

const char* host = "notify-api.line.me";
const char* token = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX";

HardwareSerial serial_ext(2);

typedef struct {
  uint32_t length;
  uint8_t *buf;
} jpeg_data_t;

jpeg_data_t jpeg_data;
static const int RX_BUF_SIZE = 30000;
static const uint8_t packet_begin[3] = { 0xFF, 0xD8, 0xEA };

//https://github.com/anoken/purin_wo_mimamoru_gijutsu/blob/master/2_6_M5Camera_Send_LineNotify/2_6_M5Camera_Send_LineNotify.ino
void sendLineNotify(uint8_t* image_data, size_t image_sz);
void setup_wifi() ;
void setup() {
  M5.begin();
  M5.Lcd.setRotation(3);
  M5.Lcd.setCursor(0, 30, 4);
  M5.Lcd.println("m5stick_uart_wifi_converter");

  setup_wifi();

  jpeg_data.buf = (uint8_t *) malloc(sizeof(uint8_t) * RX_BUF_SIZE);
  jpeg_data.length = 0;
  if (jpeg_data.buf == NULL) {
    Serial.println("malloc jpeg buffer 1 error");
  }

  serial_ext.begin(115200, SERIAL_8N1, 32, 33);
}

void loop() {
  M5.update();

  if (serial_ext.available()) {
    uint8_t rx_buffer[10];
    int rx_size = serial_ext.readBytes(rx_buffer, 10);
    if (rx_size == 10) {   //packet receive of packet_begin
      if ((rx_buffer[0] == packet_begin[0]) && (rx_buffer[1] == packet_begin[1]) && (rx_buffer[2] == packet_begin[2])) {
        //image size receive of packet_begin
        jpeg_data.length = (uint32_t)(rx_buffer[4] << 16) | (rx_buffer[5] << 8) | rx_buffer[6];
        int rx_size = serial_ext.readBytes(jpeg_data.buf, jpeg_data.length);

        //image processing, for example, line notify send image
        sendLineNotify(jpeg_data.buf, jpeg_data.length);
        //image processing end
      }
    }
  }
  vTaskDelay(10 / portTICK_RATE_MS);
}

void setup_wifi() {
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, passwd);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}


//Line通知
void sendLineNotify(uint8_t* image_data, size_t image_sz) {

  WiFiClientSecure client;
  if (!client.connect(host, 443))   return;
  int httpCode = 404;
  size_t image_size = image_sz;
  String boundary = "----purin_alert--";
  String body = "--" + boundary + "\r\n";
  String message = "m5stickVで撮影！！！";
  body += "Content-Disposition: form-data; name=\"message\"\r\n\r\n" + message + " \r\n";
  if (image_data != NULL && image_sz > 0 ) {
    image_size = image_sz;
    body += "--" + boundary + "\r\n";
    body += "Content-Disposition: form-data; name=\"imageFile\"; filename=\"image.jpg\"\r\n";
    body += "Content-Type: image/jpeg\r\n\r\n";
  }
  String body_end = "--" + boundary + "--\r\n";
  size_t body_length = body.length() + image_size + body_end.length();
  String header = "POST /api/notify HTTP/1.1\r\n";
  header += "Host: notify-api.line.me\r\n";
  header += "Authorization: Bearer " + String(token) + "\r\n";
  header += "User-Agent: " + String("M5Stack") + "\r\n";
  header += "Connection: close\r\n";
  header += "Cache-Control: no-cache\r\n";
  header += "Content-Length: " + String(body_length) + "\r\n";
  header += "Content-Type: multipart/form-data; boundary=" + boundary + "\r\n\r\n";
  client.print( header + body);
  Serial.print(header + body);

  bool Success_h = false;
  uint8_t line_try = 3;
  while (!Success_h && line_try-- > 0) {
    if (image_size > 0) {
      size_t BUF_SIZE = 1024;
      if ( image_data != NULL) {
        uint8_t *p = image_data;
        size_t sz = image_size;
        while ( p != NULL && sz) {
          if ( sz >= BUF_SIZE) {
            client.write( p, BUF_SIZE);
            p += BUF_SIZE; sz -= BUF_SIZE;
          } else {
            client.write( p, sz);
            p += sz; sz = 0;
          }
        }
      }
      client.print("\r\n" + body_end);
      Serial.print("\r\n" + body_end);

      while ( client.connected() && !client.available()) delay(10);
      if ( client.connected() && client.available() ) {
        String resp = client.readStringUntil('\n');
        httpCode    = resp.substring(resp.indexOf(" ") + 1, resp.indexOf(" ", resp.indexOf(" ") + 1)).toInt();
        Success_h   = (httpCode == 200);
        Serial.println(resp);
      }
      delay(10);
    }
  }
  client.stop();
}
