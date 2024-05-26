const int stepPin = 7; 
const int dirPin = 2; 
const int enPin = 8;
const int buttonPin = 10;

int pd = 500;       // Pulse Delay period
int pt = 800;       // Pulse Delay period

int speeds[3][2] = {
  {1000, 400},  // Speed 1: {pd, pt}
  {1500, 600},  // Speed 2: {pd, pt}
  {2000, 800}   // Speed 3: {pd, pt}
};

int currentSpeed = 0;

void setup() {
  pinMode(stepPin, OUTPUT); 
  pinMode(dirPin, OUTPUT);
  pinMode(enPin, OUTPUT);
  digitalWrite(enPin, LOW);
  Serial.begin(9600);  
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    if (command >= '1' && command <= '3') {
      currentSpeed = command - '1'; // Convert char to index (0, 1, or 2)
    }
  }

  pd = speeds[currentSpeed][0];
  pt = speeds[currentSpeed][1];

  Serial.print("Speed Setting: ");
  Serial.print(currentSpeed + 1); // Print current speed setting (1, 2, or 3)
  Serial.print(" - Delay: ");
  Serial.print(pd); 
  Serial.print(", Steps: ");
  Serial.print(pt); 
  Serial.print("\n");

  digitalWrite(dirPin, HIGH); // Enables the motor to move in a particular direction
  for (int x = 0; x < pt; x++) {
    digitalWrite(stepPin, HIGH); 
    delayMicroseconds(pd); 
    digitalWrite(stepPin, LOW); 
    delayMicroseconds(pd); 
  }    
  digitalWrite(dirPin, LOW); // Enables the motor to move in the opposite direction
  for (int x = 0; x < pt; x++) {
    digitalWrite(stepPin, HIGH); 
    delayMicroseconds(pd); 
    digitalWrite(stepPin, LOW); 
    delayMicroseconds(pd); 
  }
}
