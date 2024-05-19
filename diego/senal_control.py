import serial
import time

# Configurar la conexión serial
# puerto: cambia segun el sistema operativo y puerto
# window: COM3, linux: /dev/ttyUSB0, mac: 
arduino_port = 'COM3'
baud_rate = 9600 # velocidad de transmisión en baudios
ser = serial.Serial(arduino_port, baud_rate)
time.sleep(2)  # Esperar a que la conexión serial se establezca

# Función para enviar comandos al Arduino
def send_command(command):
    ser.write(command.encode('utf-8'))
    print("Comando enviado:", command)

# Ejemplo de uso: enviar comandos al Arduino
try:
    while True:
        command = input()
        steps = command[0]
        direction = command[1]
        send_command(steps, direction)
except KeyboardInterrupt:
    print("\nPrograma interrumpido.")
finally:
    ser.close()  # Cerrar la conexión serial al finalizar