// Program steps:
// 1. Turn off (disconnect power)
// 2. Ground GPIO0
// 3. Turn on
// 4. Upload sketch
// 5. Turn off and float GPIO0
// 6. Turn on and run

#include <ESP8266WiFi.h>
#include <ESP8266mDNS.h>
#include <WiFiUdp.h>
#include <ws2812_i2s.h>

WiFiUDP udp;

// Network
char ssid[] = "YOUR_SSID_HERE";
char pass[] = "YOUR_PASSWORD_HERE";  
char mdns_name[] = "steves_esp";
char UDP_PORT = 9090;

// Lights
const int NUM_LEDS = 60;
static WS2812 led_strip;
static Pixel_t pixels[NUM_LEDS];

// Protocol
byte LEADER[] = "colors:";
const int LEADER_LEN = 7;
const int PACKET_SIZE = (NUM_LEDS*3) + LEADER_LEN;
byte packet_buffer[PACKET_SIZE];

// Forward declarations
void connectToWifi();
void advertiseMdns();
void setupUdpListening();
int getPacket();
void setupLeds();
void updatePixelArray();

void setup() {
  Serial.begin(115200);

  Serial.println();
  Serial.println();

  connectToWifi();
  advertiseMdns();
  setupUdpListening();
//  setupLeds();
}

void loop() {
  if (getPacket()) {
    Serial.println("New packet: ");
    Serial.println((char*)packet_buffer);
    // updatePixelArray();
  }

//  led_strip.show(pixels); // KEEP DISABLED UNTIL CONFIRM PACKET_BUFFER + PIXELS BUFFER ARE GOOD.
//  delay(10); // Like in the LED example code.
}

void updatePixelArray() {
  for(int i = LEADER_LEN; i < PACKET_SIZE; i += 3) {
    pixels[i].R = packet_buffer[i];
    pixels[i].G = packet_buffer[i+1];
    pixels[i].B = packet_buffer[i+2];
  }
}

void setupLeds() {
  led_strip.init(NUM_LEDS);
  for (int i = 0; i < LEADER_LEN; i++) {
    packet_buffer[i] = LEADER[i];
  }
  for (int i = LEADER_LEN; i < PACKET_SIZE; i++) {
    packet_buffer[i] = 30; // dull white?
  }
}

int packetIsValid(byte* packet) {
  // Packet starts with leader.
  for (int i = 0; i < LEADER_LEN; i++) {
    if (LEADER[i] != packet[i]) { return 0; }
  }
  // A byte is only 8 bits - it must be in the valid color range.
  return 1;
}

int getPacket() {
  byte temp_buffer[PACKET_SIZE];
  int packet_length = udp.parsePacket();

  if (!packet_length) { return 0; }
  if (packet_length != PACKET_SIZE) { return 0; }

  udp.read(temp_buffer, PACKET_SIZE);

  if (packetIsValid(temp_buffer)) {
    byte* dest = packet_buffer;
    byte* src = temp_buffer;
    memcpy(dest, src, PACKET_SIZE);
    return 1;
  }

  return 0;
}

// Setup
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

void setupUdpListening() {
  Serial.println("Starting UDP");
  udp.begin(UDP_PORT);
  Serial.print("Local port: ");
  Serial.println(udp.localPort());
}

