/*==========================================================================
// Author : Handson Technology
// Project : BTD7960 Motor Control Board driven by Arduino.
// Description : Speed and direction controlled by a potentiometer attached 
// to analog input A0. One side pin of the potentiometer (either one) to 
// ground; the other side pin to +5V
// Source-Code : BTS7960.ino
// Program: Control DC motors using BTS7960 H Bridge Driver.
//==========================================================================
// Connection to the BTS7960 board:
// BTS7960 Pin 1 (RPWM) to Arduino pin 5(PWM)
// BTS7960 Pin 2 (LPWM) to Arduino pin 6(PWM)
// BTS7960 Pin 3 (R_EN), 4 (L_EN), 7 (VCC) to Arduino 5V pin
// BTS7960 Pin 8 (GND) to Arduino GND
// BTS7960 Pin 5 (R_IS) and 6 (L_IS) not connected
*/
int SENSOR_PIN = 0; // center pin of the potentiometer
int RPWM_Output = 5; // Arduino PWM output pin 5; connect to IBT-2 pin 1 (RPWM)
int LPWM_Output = 6; // Arduino PWM output pin 6; connect to IBT-2 pin 2 (LPWM)
int potPin = 1; // Pin donde está conectado el potenciómetro
int potValue = 0;      // Variable para almacenar el valor leído del potenciómetro
int angle = 0;         // Variable para almacenar el ángulo calculado

const int frecuencia = 50; // Frecuencia en Hz
const int periodo = 1000 / frecuencia; // Periodo en milisegundos

int steps = 0;
int direction = 0;


class PIDControl {
  public:
    float Kp;
    float Ki;
    float Kd;
    float dt;
    float prev_err1;
    float prev_err2;
    float prev_u;

    // Constructor
    PIDControl(float kp, float ki, float kd, float samplingPeriod = 1.0) {
      dt = samplingPeriod;
      Kp = kp;
      Ki = ki * dt;
      Kd = kd / dt;
      prev_err1 = 0.0;
      prev_err2 = 0.0;
      prev_u = 0.0;
    }

    // Método para calcular el control
    float calcular_control(float err) {
      float u = prev_u + (Kp + Ki + Kd) * err - (Kp + 2 * Kd) * prev_err1 + Kd * prev_err2;
      prev_err2 = prev_err1;
      prev_err1 = err;
      prev_u = u;
      return u;
    }
};

// Ejemplo de uso en el loop de Arduino
PIDControl pidControl(1.0, 0.1, 0.01, 1.0);


void setup(){
 Serial.begin(9600);               // initialize hardware serial for debugging
 //SoftSerial.begin(9600);           // initialize software serial for UART motor control
 pinMode(RPWM_Output, OUTPUT);
 pinMode(LPWM_Output, OUTPUT);
}
void loop(){
 potValue = analogRead(potPin);  // Leer el valor del potenciómetro (0-1023)
 angle = map(potValue, 0, 10000, 0, 360);  // Mapear el valor a un rango de ángulos (0-180)
 int sensorValue = analogRead(SENSOR_PIN);
 Serial.println(sensorValue);
 // sensor value is in the range 0 to 1023
 // the lower half of it we use for reverse rotation; the upper half for forward rotation
if (Serial.available() > 0) {
    int steps = Serial.parseInt();  // Leer el número de pasos
    int direction = Serial.parseInt();  // Leer la dirección
    //Serial << "Pasos: " << steps << " Dirección: " << direction << "angulo" << angle << endl;
    if (direction == 1){
    analogWrite(LPWM_Output, 0);
    analogWrite(RPWM_Output, steps); //hacia atras reversePWM
    }
    else {
    //modulaPWM(LPWM_Output, 100, periodo);
    analogWrite(LPWM_Output, steps); //hacia adelante forwardPWM
    analogWrite(RPWM_Output, 0);
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
