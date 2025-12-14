#include <WiFiS3.h>
#include <WiFiUdp.h>


const char* ssid = "YOUR_WIFI_SSID";
const char* pass = "YOUR_WIFI_PASSWORD";


WiFiUDP Udp;

IPAddress listenerIP(192, 168, 0, 100);  // Update listenerIP to match the IPv4 address of the backend listener

unsigned int listenerPort = 5005;       // Listener service port


unsigned long lastBeat = 0;
int counter = 0;

void setup() {
  Serial.begin(115200);

  
  while (!Serial) {}

  Serial.println("=== WiFi Heartbeat Sender Starting ===");

 
  Serial.print("Connecting to WiFi SSID: ");
  Serial.println(ssid);

  WiFi.begin(ssid, pass);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi connected successfully.");

 
  Serial.print("Arduino IP address: ");
  Serial.println(WiFi.localIP());

  Serial.print("Sending heartbeats to listener IP: ");
  Serial.println(listenerIP);

  Serial.print("Sending heartbeats to listener port: ");
  Serial.println(listenerPort);

 
  Udp.begin(0);  

  Serial.println("UDP socket initialised.");
  Serial.println("====================================");
}

void loop() {
  unsigned long now = millis();

  if (now - lastBeat >= 10000) {   // 10-second heartbeat interval
    lastBeat = now;
    counter++;

    String msg = "HB," + String(counter) + "," + String(millis());

    Udp.beginPacket(listenerIP, listenerPort);
    Udp.print(msg);
    Udp.endPacket();

  
    Serial.print("Sent heartbeat: ");
    Serial.println(msg);
  }
}
