#include <ESP8266WiFi.h>

#ifndef STASSID
#define STASSID "Android_One"
#define STAPSK "hostelnet"
#endif

const char* ssid = STASSID;
const char* password = STAPSK;

void setup() {
  Serial.begin(115200);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }

  Serial.println(WiFi.localIP());
}

void loop() {
}