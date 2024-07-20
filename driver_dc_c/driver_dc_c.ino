// BTS7960 puente H, Placa de control de motor controlada por Arduino.
// control de velocidad y direccion
// IBT-2 controlador de motor basado en el chip H-bridge BTS7960

int RPWM_Output_PIN = 5; // hacia atras
int LPWM_Output_PIN = 6; // hacia delante
int SENSOR_PIN = 1; // sensor de angulo
int potvalue = 0; // lectura del potenciometro
int angle = 0; // angulo calculado

//const int frecuencia = 50; // Frecuencia en Hz
//const int periodo = 1000 / frecuencia; // Periodo en milisegundos

int speed = 0;
int direction = 0;

void setup(){
 Serial.begin(9600); // Inicializar el serial del hardware para depuración
 pinMode(RPWM_Output_PIN, OUTPUT);
 pinMode(LPWM_Output_PIN, OUTPUT);
}
void loop(){
 potvalue = analogRead(SENSOR_PIN);  // Leer el valor del potenciómetro
 angle = map(potvalue, 0, 1000, 0, 360);  // Mapear el valor a un rango de ángulos
 Serial.println(angle);
 //float error = sensorValue - ref
 //float control = pidControl.calcular_control(error);
 if (Serial.available() > 0) {
    String mensaje = Serial.readStringUntil('>');
    if (mensaje.startsWith("<")) {
      mensaje.remove(0, 1); // Elimina el delimitador de inicio '<'
      int comaIndex = mensaje.indexOf(',');
      if (comaIndex != -1) {
        int speed = mensaje.substring(0, comaIndex).toInt();
        int direction = mensaje.substring(comaIndex + 1).toInt();
    //int speed = Serial.parseInt(); // velocidad
    //int direction = Serial.parseInt(); // direccion
    //Serial.print("Velocidad recibida: ");
    //Serial.println(speed);
    //Serial.print("Direccion recibida: ");
    //Serial.println(direction);
    //Serial.println(speed);
    //Serial.println(direction);
    if (direction == 0){
    analogWrite(LPWM_Output_PIN, 0);
    analogWrite(RPWM_Output_PIN, speed); //hacia atras
    }
    else {
    //modulaPWM(LPWM_Output, 100, periodo);
    analogWrite(LPWM_Output_PIN, speed); //hacia delante
    analogWrite(RPWM_Output_PIN, 0);
    }
    }
    }
 }
}

void modulaPWM(int pin, int dutyCycle, int periodo) {
  int tiempoAlto = (dutyCycle * periodo) / 100; // Tiempo en estado alto
  int tiempoBajo = periodo - tiempoAlto; // Tiempo en estado bajo

  analogWrite(pin, 100);
  delayMicroseconds(tiempoAlto * 1000); // Mantiene en estado alto

  analogWrite(pin, 0);
  delayMicroseconds(tiempoBajo * 1000); // Mantiene en estado bajo
}
