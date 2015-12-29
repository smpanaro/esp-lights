// Program steps:
// 1. Turn off (disconnect power)
// 2. Ground GPIO0
// 3. Turn on
// 4. Upload sketch
// 5. Turn off and float GPIO0
// 6. Turn on and run

#include <ESP8266WiFi.h>
#include <ESP8266mDNS.h>

char ssid[] = "ssid";
char pass[] = "pass";  
char mdns_name[] = "steves_esp";

void connectToWifi();
void advertiseMdns();

void setup() {
  Serial.begin(115200);

  Serial.println();
  Serial.println();

  connectToWifi();
  advertiseMdns();
}

void loop() {

  delay(1000);
}

void connectToWifi() {
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, pass);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");

  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void advertiseMdns() {
  if (!MDNS.begin(mdns_name, WiFi.localIP(), 120)) {
    Serial.println("Error setting up mdns");
  }
  Serial.println("Set up mdns: ");
  Serial.println(mdns_name);
}

