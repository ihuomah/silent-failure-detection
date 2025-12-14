unsigned long lastBeat = 0;
int counter = 0;

void setup() {
  Serial.begin(115200);
  while (!Serial) { ; }
  Serial.println("Heartbeat test started");
}

void loop() {
  unsigned long now = millis();
  if (now - lastBeat >= 10000) { // 10 seconds
    lastBeat = now;
    counter++;
    Serial.print("HEARTBEAT ");
    Serial.println(counter);
  }
}
