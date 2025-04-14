const int ldrPin1 = A0;  // Pin connected to the LDR module's S pin
const int ldrPin2 = A1;  // Pin connected to the LDR module's S pin
const int pin5 = 5;     
const int pin6 = 6;   
const int pin10 = 10;
const int pin11 = 11;
int ldrValue1 = 0;       // Variable to store the LDR value
int ldrValue2 = 0;       // Variable to store the LDR value
int score = 0;
unsigned long lastHitTime1 = 0;  // To store the time when the laser was last detected
unsigned long lastHitTime2 = 0;  // To store the time when the laser was last detected
unsigned long disableTime = 3000;  // Disable target for 1 second (1000 milliseconds)

void setup() {
  Serial.begin(9600);  // Start Serial communication for debugging
  pinMode(pin5, OUTPUT);
  pinMode(pin6, OUTPUT);
  pinMode(pin10, OUTPUT);
  pinMode(pin11, OUTPUT);
  digitalWrite(pin5, LOW);
  digitalWrite(pin6, LOW);
  digitalWrite(pin10, LOW);
  digitalWrite(pin11, LOW);
}

void loop() {
  ldrValue1 = analogRead(ldrPin1);  // Read the analog value from the LDR
  Serial.println(ldrValue1);


  // Check if the LDR value indicates that the laser is on it
  if (ldrValue1 < 200) {  // Adjust threshold based on your laser's intensity

    if (millis() - lastHitTime1 >= disableTime) {
          score++; // Add to score
          Serial.println("Laser Detected!");  // Laser is detected (light is high)
          Serial.print("Score: ");
          Serial.println(score);
          lastHitTime1 = millis();
      } 

    } 

    if (millis() - lastHitTime1 >= disableTime) {
      digitalWrite(pin10, HIGH);
      digitalWrite(pin11, LOW);     

    } else {
 
      digitalWrite(pin10, LOW);
      digitalWrite(pin11, HIGH);
    }

  // 2nd sensor
  ldrValue2 = analogRead(ldrPin2);  // Read the analog value from the LDR
  Serial.println(ldrValue2);

  if (ldrValue2 < 200) {  // Adjust threshold based on your laser's intensity
    if (millis() - lastHitTime2 >= disableTime) {
      score++;  // Add to score
      Serial.println("Laser Detected!");  // Laser is detected (light is high)
      Serial.print("Score: ");
      Serial.println(score);
      lastHitTime2 = millis();
    }
  }

  // Handle the LED states based on the time since the last laser hit
  if (millis() - lastHitTime2 >= disableTime) {    
    digitalWrite(pin5, HIGH); // Turn on the first LED
    digitalWrite(pin6, LOW);  // Turn off the second LED
    
  } else {
    digitalWrite(pin5, LOW);  // Turn off the first LED
    digitalWrite(pin6, HIGH); // Turn on the second LED
  }

  delay(100);  // Delay to avoid overwhelming the Serial Monitor
}
  
