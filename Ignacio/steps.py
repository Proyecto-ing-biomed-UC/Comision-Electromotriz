import serial
import time

# Configurar la conexión serial
arduino_port = 'COM4'
baud_rate = 9600  # Velocidad de transmisión en baudios
ser = serial.Serial(arduino_port, baud_rate)
time.sleep(2)  # Esperar a que la conexión serial se establezca

# Función para enviar comandos al Arduino
def send_command(command):
    ser.write(command.encode('utf-8'))
    print("Comando enviado:", command)

# Ejemplo de uso: enviar comandos al Arduino
try:
    while True:
        command = input("Ingrese un comando (1, 2, 3 para cambiar la velocidad): ")
        if command in ['1', '2', '3']:
            send_command(command)
        else:
            print("Comando no válido. Ingrese 1, 2 o 3.")
except KeyboardInterrupt:
    print("\nPrograma interrumpido.")
finally:
    ser.close()  # Cerrar la conexión serial al finalizar

