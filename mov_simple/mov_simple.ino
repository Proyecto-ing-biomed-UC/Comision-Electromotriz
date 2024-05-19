// Declara y asigna constantes para los pines que se usarán en el circuito
const int stepPin = 5; // pulsos que determinan el movimiento del motor, cada pulso en este pin hace que el motor avance un paso.
const int dirPin = 2; // dirección de rotación
const int enPin = 8; // habilitar o deshabilitar el driver del motor paso a paso
const int buttonPin = 10; // detectar estado de boton
// const int encoderPinA = 2; // encoder A
// const int encoderPinB = 3; // encoder B
// volatile long encoderPos = 0; // posicion encoder

// inicio del programa (configurar pines y ajustes)
void setup() {
  pinMode(buttonPin, INPUT);
  // pinMode(encoderPinA, INPUT);
  // pinMode(encoderPinB, INPUT);
  // attachInterrupt(digitalPinToInterrupt(encoderPinA), updateEncoder, CHANGE);
  pinMode(stepPin,OUTPUT); 
  pinMode(dirPin,OUTPUT);
  pinMode(enPin,OUTPUT);
  digitalWrite(enPin,LOW); // se establece en estado bajo (cuando el pin está bajo, el driver del motor se activa y está listo para recibir comandos)
  Serial.begin(9600);
}

// bucle de ejecucion infinito
void loop() {
  int buttonState = digitalRead(buttonPin); // boton del hombre muerto
  // Serial.print("ENC:");
  // Serial.print(encoderPos);
  if (buttonState == LOW) {
    if (Serial.available() > 0) {
    int steps = Serial.parseInt();  // Leer el número de pasos
    int direction = Serial.parseInt();  // Leer la dirección
    moveMotor(steps, direction);
  }
  }
}

// Función para mover el motor
void moveMotor(int steps, int direction) {
  digitalWrite(dirPin, direction);  // Establecer la dirección
  digitalWrite(enPin, HIGH);  // Habilitar el driver del motor
  for (int x = 0; x < steps; x++) {
    digitalWrite(stepPin, HIGH);  // Enviar pulso HIGH
    delayMicroseconds(500);       // Esperar 500 microsegundos
    digitalWrite(stepPin, LOW);   // Enviar pulso LOW
    delayMicroseconds(500);       // Esperar 500 microsegundos
  }
  digitalWrite(enPin, LOW);  // Deshabilitar el driver del motor después de mover el número deseado de pasos
}

void updateEncoder() {
  int stateA = digitalRead(encoderPinA);
  int stateB = digitalRead(encoderPinB);
  if (stateA == stateB) {
    encoderPos++;
  } else {
    encoderPos--;
  }
}
