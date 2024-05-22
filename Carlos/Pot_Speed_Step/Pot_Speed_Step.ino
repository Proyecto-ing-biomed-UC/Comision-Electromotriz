const int stepPin = 7; 
const int dirPin = 2; 
const int enPin = 8;
const int buttonPin = 10;
int spt = A0;     // Potentiometer
int spd = A2;     // Potentiometer
int pd = 500;       // Pulse Delay period
int pt = 800;       // Pulse Delay period


void setup() {
  pinMode(buttonPin, INPUT);
  pinMode(stepPin,OUTPUT); 
  pinMode(dirPin,OUTPUT);
  pinMode(enPin,OUTPUT);
  digitalWrite(enPin,LOW);
  Serial.begin(9600);  
}

void loop() {
  int buttonState = digitalRead(buttonPin);
  pt = map((analogRead(spd)),0,1023,2000,50);
  pd = map((analogRead(spt)),0,1023,2000,50);
  Serial.print("Delay:");
  Serial.print(pd); 
  Serial.print(","); 

  Serial.print("Steps:");
  Serial.print(pt); 
  Serial.print("\n");

    digitalWrite(dirPin,HIGH); // Enables the motor to move in a particular direction
    for(int x = 0; x < pt; x++) {
      digitalWrite(stepPin,HIGH); 
      delayMicroseconds(pd); 
      digitalWrite(stepPin,LOW); 
      delayMicroseconds(pd); 
    }    
    digitalWrite(dirPin,LOW); // Enables the motor to move in a particular direction
    for(int x = 0; x < pt; x++) {
      digitalWrite(stepPin,HIGH); 
      delayMicroseconds(pd); 
      digitalWrite(stepPin,LOW); 
      delayMicroseconds(pd); 
    }}