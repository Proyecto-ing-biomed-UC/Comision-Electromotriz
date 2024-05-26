import serial
import time

# Configurar la conexión serial
arduino_port = 'COM4'
baud_rate = 9600  # Velocidad de transmisión en baudios
ser = serial.Serial(arduino_port, baud_rate)
time.sleep(2)  # Esperar a que la conexión serial se establezca

# Función para enviar comandos al Arduino
def send_command(command):
    ser.write((command + '\n').encode('utf-8'))
    print("Comando enviado:", command)

# Ejemplo de uso: enviar comandos al Arduino
try:
    while True:
        command = input("Ingrese un comando (e.g., F1T10, B2D2000): ")
        if len(command) > 3 and command[0] in ['F', 'B'] and command[1] in ['1', '2', '3'] and command[2] in ['T', 'D']:
            send_command(command)
        else:
            print("Comando no válido. Ingrese un comando válido como F1T10 o B2D2000.")
except KeyboardInterrupt:
    print("\nPrograma interrumpido.")
finally:
    ser.close()  # Cerrar la conexión serial al finalizar

