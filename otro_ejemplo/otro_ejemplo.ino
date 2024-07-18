const int pwmPin = 9; // Pin de salida PWM
const int frecuencia = 50; // Frecuencia en Hz
const int periodo = 1000 / frecuencia; // Periodo en milisegundos

void setup() {
  pinMode(pwmPin, OUTPUT);
}

void loop() {
  for (int dutyCycle = 0; dutyCycle <= 100; dutyCycle++) {
    modulaPWM(pwmPin, dutyCycle, periodo);
    delay(10); // Retardo para visualizar el cambio en el duty cycle
  }
  for (int dutyCycle = 100; dutyCycle >= 0; dutyCycle--) {
    modulaPWM(pwmPin, dutyCycle, periodo);
    delay(10); // Retardo para visualizar el cambio en el duty cycle
  }
}

void modulaPWM(int pin, int dutyCycle, int periodo) {
  int tiempoAlto = (dutyCycle * periodo) / 100; // Tiempo en estado alto
  int tiempoBajo = periodo - tiempoAlto; // Tiempo en estado bajo

  digitalWrite(pin, HIGH);
  delayMicroseconds(tiempoAlto * 1000); // Mantiene en estado alto

  digitalWrite(pin, LOW);
  delayMicroseconds(tiempoBajo * 1000); // Mantiene en estado bajo
}
