// Define los pines donde están conectados los 8 cables del encoder
const int pin1 = 23; // G23
const int pin2 = 22; // G22
const int pin3 = 21; // G21
const int pin4 = 19; // G19
const int pin5 = 18; // G18
const int pin6 = 17; // G17
const int pin7 = 16; // G16
const int pin8 = 15; // G15

void setup() {
  // Configura los pines como entradas
  pinMode(pin1, INPUT);
  pinMode(pin2, INPUT);
  pinMode(pin3, INPUT);
  pinMode(pin4, INPUT);
  pinMode(pin5, INPUT);
  pinMode(pin6, INPUT);
  pinMode(pin7, INPUT);
  pinMode(pin8, INPUT);
  
  // Inicia la comunicación serial para ver los resultados
  Serial.begin(9600);
}

void loop() {
  // Lee el estado de cada pin
  int bit1 = digitalRead(pin1);
  int bit2 = digitalRead(pin2);
  int bit3 = digitalRead(pin3);
  int bit4 = digitalRead(pin4);
  int bit5 = digitalRead(pin5);
  int bit6 = digitalRead(pin6);
  int bit7 = digitalRead(pin7);
  int bit8 = digitalRead(pin8);

  // Combina los bits en un solo valor de 8 bits
  int position = (bit1 << 7) | (bit2 << 6) | (bit3 << 5) | (bit4 << 4) | (bit5 << 3) | (bit6 << 2) | (bit7 << 1) | bit8;

  // Muestra la posición del encoder en formato binario y decimal
  Serial.print("Posición (binario): ");
  Serial.print(bit1);
  Serial.print(bit2);
  Serial.print(bit3);
  Serial.print(bit4);
  Serial.print(bit5);
  Serial.print(bit6);
  Serial.print(bit7);
  Serial.print(bit8);
  
  Serial.print(" | Posición (decimal): ");
  Serial.println(position);

  delay(500); // Retardo para la siguiente lectura
}

