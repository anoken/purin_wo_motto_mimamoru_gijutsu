// Copyright (c) 2019 aNoken
// Arduino IDE compile code
//arduino-esp ver 1.04
//m5stickc libs in adrduino ver 0.1.1

#include <M5StickC.h>
#include <WiFi.h>
#include <ssl_client.h>
#include <WiFiClientSecure.h>
const char* ssid = "your_ssid";
const char* passwd = "your_passwd";

const char* host = "notify-api.line.me";
const char* token = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX";

HardwareSerial serial_ext(2);
TFT_eSprite *Spr;
uint32_t front_col = TFT_YELLOW;
uint32_t back_col = TFT_BLACK;

int dat[160];
int dat2[160];
String moji;
String moji2;

int dist = 0;
int dist_thresh = 50;
bool sendphoto_flg = 0;
typedef struct {
  uint32_t length;
  uint8_t *buf;
} jpeg_data_t;

jpeg_data_t jpeg_data;
static const int RX_BUF_SIZE = 30000;
static const uint8_t packet_img[4] = { 0xFF, 0xF1, 0xF2, 0xA1};
static const uint8_t packet_dist[4] = { 0xFF, 0xF3, 0xF4, 0xA1};
static const uint8_t packet_thresh[4] = { 0xFF, 0xF5, 0xF6, 0xA1};

void sendLinePhoto(uint8_t* image_data, size_t image_sz, String mess);
void sendLineMessage(String message);
void setup_wifi();

void setup() {
  M5.begin();
  M5.Lcd.setRotation(1);
  //LCD Splite Initialize
  Spr = new TFT_eSprite(&M5.Lcd);
  Spr->setColorDepth(8);
  Spr->createSprite(320, 240);
  Spr->setBitmapColor(front_col, back_col);
  Spr->fillSprite(front_col);
  Spr->pushSprite(0, 0);

  Spr->setTextColor(TFT_WHITE); // White text, no background

  setup_wifi();

  jpeg_data.buf = (uint8_t *) malloc(sizeof(uint8_t) * RX_BUF_SIZE);
  jpeg_data.length = 0;
  if (jpeg_data.buf == NULL) {
    Serial.println("malloc jpeg buffer 1 error");
  }

  serial_ext.begin(115200, SERIAL_8N1, 32, 33);
  for (int x = 0; x < 160; x++)dat[x] = 0;
  for (int x = 0; x < 160; x++)dat2[x] = 0;

}


void loop() {
  M5.update();

  if ( M5.BtnA.wasPressed() ) {
    Serial.println("BtnA.wasPressed() == TRUE");
  }
  if ( M5.BtnB.wasPressed() ) {
    sendphoto_flg = !sendphoto_flg;
    Serial.println(sendphoto_flg);
  }

  if (serial_ext.available()) {
    uint8_t rx_buffer[10];
    int rx_size = serial_ext.readBytes(rx_buffer, 10);
    if (rx_size == 10) {   //packet receive of packet_begin
      if ((rx_buffer[0] == packet_img[0]) && (rx_buffer[1] == packet_img[1]) && (rx_buffer[2] == packet_img[2]) && (rx_buffer[3] == packet_img[3])) {
        //image size receive of packet_begin
        jpeg_data.length = (uint32_t)(rx_buffer[4] << 16) | (rx_buffer[5] << 8) | rx_buffer[6];
        int rx_size = serial_ext.readBytes(jpeg_data.buf, jpeg_data.length);
        String messe = "\r\n おうちに訪問者です";
        if (!sendphoto_flg) sendLineMessage(messe);
        else              sendLinePhoto(jpeg_data.buf, jpeg_data.length, messe);

      }
      else if ((rx_buffer[0] == packet_dist[0]) && (rx_buffer[1] == packet_dist[1]) && (rx_buffer[2] == packet_dist[2]) && (rx_buffer[3] == packet_dist[3])) {
        dist = (uint32_t)(rx_buffer[4] << 8) | rx_buffer[5];
        for (int x = 0; x < 159; x++)dat[x] = dat[x + 1];
        dat[159] = dist;

        dist_thresh = (uint32_t) (rx_buffer[6] << 8) | rx_buffer[7];
        for (int x = 0; x < 160 ; x++)dat2[x] = dist_thresh;
      }

      else {
        uint8_t rx_buffer[10];
        int rx_size = serial_ext.readBytes(rx_buffer, 1);
      }
    }
  }

  Spr->fillSprite(back_col);  

  //Graph Fearture
  double ratio = 80 * 0.65 / dist_thresh;
  for (int x = 0; x < 160 - 1; x++)Spr->drawLine( x, 65 - dat[x] * ratio, x + 1, 65 - dat[x + 1] * ratio,  TFT_YELLOW);
  for (int x = 0; x < 160 - 1; x++)Spr->drawLine( x, 65 - dat2[x] * ratio, x + 1, 65 - dat2[x + 1] *ratio,  TFT_RED);
  moji = String(dist) + String("/") + String(dist_thresh) + String("    ");
  moji2 = "Message Only";
  if (sendphoto_flg) moji2 = "Photo Send";
  Spr->drawString(moji, 5, 0, 2);
  Spr->drawString(moji2, 70, 65, 2);
  Spr->pushSprite(0, 0);

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


//Line send Photo
void sendLinePhoto(uint8_t* image_data, size_t image_sz, String message) {
  WiFiClientSecure client;
  if (!client.connect(host, 443))   return;
  int httpCode = 404;
  size_t image_size = image_sz;
  String boundary = "----purin_alert--";
  String body = "--" + boundary + "\r\n";
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

//Line send Massage Only
void sendLineMessage(String message) {
  WiFiClientSecure client;

  if (!client.connect(host, 443)) {
    Serial.println("Connection failed");
    return;
  }
  String query = String("message=") + message;
  String request = String("") +
                   "POST /api/notify HTTP/1.1\r\n" +
                   "Host: " + host + "\r\n" +
                   "Authorization: Bearer " + token + "\r\n" +
                   "Content-Length: " + String(query.length()) +  "\r\n" +
                   "Content-Type: application/x-www-form-urlencoded\r\n\r\n" +
                   query + "\r\n";
  client.print(request);

  while (client.connected()) {
    String line = client.readStringUntil('\n');
    Serial.println(line);
    if (line == "\r") {
      break;
    }
  }

  String line = client.readStringUntil('\n');
  Serial.println(line);
}
