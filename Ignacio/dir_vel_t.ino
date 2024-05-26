const int stepPin = 7; 
const int dirPin = 2; 
const int enPin = 8;

int pd = 500;       // Pulse Delay period
int pt = 800;       // Pulse Delay period

int speeds[3][2] = {
  {1000, 400},  // Speed 1: {pd, pt}
  {1500, 600},  // Speed 2: {pd, pt}
  {2000, 800}   // Speed 3: {pd, pt}
};

int currentSpeed = 0;
bool directionForward = true; // true for forward, false for backward

void setup() {
  pinMode(stepPin, OUTPUT); 
  pinMode(dirPin, OUTPUT);
  pinMode(enPin, OUTPUT);
  digitalWrite(enPin, LOW);
  Serial.begin(9600);  
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    if (command.length() >= 4) {
      char dir = command[0];
      char speedChar = command[1];
      char type = command[2];
      String valueStr = command.substring(3);
      int value = valueStr.toInt();
      
      if ((dir == 'F' || dir == 'B') && (speedChar >= '1' && speedChar <= '3')) {
        currentSpeed = speedChar - '1'; // Convert char to index (0, 1, or 2)
        directionForward = (dir == 'F');

        pd = speeds[currentSpeed][0];
        pt = speeds[currentSpeed][1];

        Serial.print("Command received: ");
        Serial.println(command);
        Serial.print("Speed Setting: ");
        Serial.print(currentSpeed + 1); // Print current speed setting (1, 2, or 3)
        Serial.print(" - Direction: ");
        Serial.print(directionForward ? "Forward" : "Backward"); 
        Serial.print(" - Delay: ");
        Serial.print(pd); 
        Serial.print(", Steps: ");
        Serial.print(pt); 
        Serial.println();

        digitalWrite(dirPin, directionForward ? HIGH : LOW); // Set direction
        digitalWrite(enPin, LOW); // Enable the motor

        if (type == 'T') {
          // Move for the specified time in seconds
          long duration = value * 1000L; // Convert seconds to milliseconds
          unsigned long startTime = millis();
          while (millis() - startTime < duration) {
            digitalWrite(stepPin, HIGH); 
            delayMicroseconds(pd); 
            digitalWrite(stepPin, LOW); 
            delayMicroseconds(pd); 
          }
        } else if (type == 'D') {
          // Move for the specified number of steps
          for (int x = 0; x < value; x++) {
            digitalWrite(stepPin, HIGH); 
            delayMicroseconds(pd); 
            digitalWrite(stepPin, LOW); 
            delayMicroseconds(pd); 
          }
        }
        
        digitalWrite(enPin, HIGH); // Disable the motor to reduce noise when not in use
      }
    }
  }
}


