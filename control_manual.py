import tkinter as tk # interfaz de usuario
import serial # comunicacion con arduino
import time
import threading # multitask
from classandfunc import *
import numpy as np

# Configurar la conexión serial
# puerto: cambia segun el sistema operativo y puerto
# window: COM3, linux: /dev/ttyUSB0, mac: 
arduino_port = 'COM3'
baud_rate = 9600 # velocidad de transmisión en baudios
ser = serial.Serial(arduino_port, baud_rate)
#vel_entry = None
#dir_entry = None
time.sleep(2)  # esperar a que la conexión serial se establezca

# Función para enviar datos al Arduino
def send_data():
    global vel_entry, dir_entry
    velocidad = vel_entry.get()
    direccion = dir_entry.get()
    ser.write(f"<{velocidad},{direccion}>".encode('utf-8'))

# ventana principal
root = tk.Tk()
root.title("Control de Motor")
# campo de velocidad
vel_label = tk.Label(root, text="Velocidad:")
vel_label.grid(row=0, column=0, padx=10, pady=5)
# Campo de entrada para la velocidad
vel_entry = tk.Entry(root)
vel_entry.grid(row=0, column=1, padx=10, pady=5)

# Etiqueta para la selección de dirección
dir_label = tk.Label(root, text="Dirección:")
dir_label.grid(row=1, column=0, padx=10, pady=5)

# Variable de control para la dirección (0 para adelante, 1 para atrás)
dir_entry = tk.IntVar()
dir_entry.set(0)

# Botón de radio para la dirección hacia adelante
forward_radio = tk.Radiobutton(root, text="Atras", variable=dir_entry, value=0)
forward_radio.grid(row=1, column=1, padx=10, pady=5)

# Botón de radio para la dirección hacia atrás
backward_radio = tk.Radiobutton(root, text="Adelante", variable=dir_entry, value=1)
backward_radio.grid(row=1, column=2, padx=10, pady=5)

# Botón para enviar los datos al Arduino
send_button = tk.Button(root, text="Enviar", command=send_data)
send_button.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

# Etiqueta para mostrar los datos del encoder
#encoder_label = tk.Label(root, text="Encoder: 0")
#encoder_label.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

def close_serial():
    ser.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", close_serial)

# Iniciar el bucle de eventos
root.mainloop()