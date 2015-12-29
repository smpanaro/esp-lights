// Program steps:
// 1. Turn off (disconnect power)
// 2. Ground GPIO0
// 3. Turn on
// 4. Upload sketch
// 5. Turn off and float GPIO0
// 6. Turn on and run

#include <ESP8266WiFi.h>
#include <ESP8266mDNS.h>
#include <WebSocketsServer.h>

// Constants
char ssid[] = "ssid";
char pass[] = "pass";  
char mdns_name[] = "steves_esp";

WiFiServer server(80);
WebSocketsServer webSocket = WebSocketsServer(81);

// Forward declarations
void connectToWifi();
void advertiseMdns();
void setupWebsockets();
void handleWebSocketEvent(uint8_t num, WStype_t type, uint8_t * payload, size_t length);

void setup() {
  Serial.begin(115200);

  Serial.println();
  Serial.println();

  connectToWifi();
  advertiseMdns();
  setupWebsockets();
}

void loop() {
  webSocket.loop();

  delay(1000);
}

void setupWebsockets() {
  Serial.println("Setting up websockets");
  webSocket.begin();
  webSocket.onEvent(handleWebSocketEvent);
  Serial.println("Set up.");
}

void handleWebSocketEvent(uint8_t num, WStype_t type, uint8_t * payload, size_t length) {

    switch(type) {
        case WStype_DISCONNECTED:
            Serial.println("Disconnected!");
            break;
        case WStype_CONNECTED: {
            IPAddress ip = webSocket.remoteIP(num);
            Serial.println("Connected");

            // send message to client
            webSocket.sendTXT(num, "Connected");
        }
            break;
        case WStype_TEXT:
            Serial.println("Get text");

            // send message to client
            // webSocket.sendTXT(num, "message here");

            // send data to all connected clients
            // webSocket.broadcastTXT("message here");
            break;
        case WStype_BIN:
            Serial.println("get bin");

            // send message to client
            // webSocket.sendBIN(num, payload, lenght);
            break;
    }
}

void connectToWifi() {
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  
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

