const int ldrPin = A0;  // Pin connected to the LDR module's S pin
int ldrValue = 0;       // Variable to store the LDR value
int score = 0;
unsigned long lastHitTime = 0;  // To store the time when the laser was last detected
unsigned long disableTime = 1000;  // Disable target for 1 second (1000 milliseconds)

void setup() {
  Serial.begin(9600);  // Start Serial communication for debugging
}

void loop() {
  ldrValue = analogRead(ldrPin);  // Read the analog value from the LDR
  

  // Check if the LDR value indicates that the laser is on it
  if (ldrValue < 100) {  // Adjust threshold based on your laser's intensity
    if (millis() - lastHitTime >= disableTime) {
          score++; // Add to score
          Serial.println("Laser Detected!");  // Laser is detected (light is high)
          Serial.print("Score: ");
          Serial.println(score);
          lastHitTime = millis();
      } 

    } 
  delay(100);  // Delay to avoid overwhelming the Serial Monitor
}

