import tkinter as tk
import serial
import time
import threading

# Configurar la conexión serial
# puerto: cambia segun el sistema operativo y puerto
# window: COM3, linux: /dev/ttyUSB0, mac: 
arduino_port = 'COM3'
baud_rate = 9600 # velocidad de transmisión en baudios
ser = serial.Serial(arduino_port, baud_rate)
time.sleep(2)  # esperar a que la conexión serial se establezca

# Función para enviar datos al Arduino
def send_data():
    steps = steps_entry.get()
    direction = direction_var.get()
    print(steps, direction)
    ser.write(f"{steps} {direction}\n".encode('utf-8'))

def read_serial(ser):
    while True:
        if ser.in_waiting > 0:
            message = ser.readline().decode('utf-8').rstrip()  # Lee el mensaje
            print(message)  # Muestra el mensaje

thread = threading.Thread(target=read_serial, args=(ser,))
thread.daemon = True  # Permite que el hilo se cierre al cerrar el programa
thread.start()

# Función para actualizar los datos del sensor
#def update_sensor_data():
#    while True:
#        if ser.in_waiting > 0:
#            data = ser.readline().decode('utf-8').strip()
#            if data.startswith("ENC:") in data:
#                encoder_data = data
#                encoder_value = encoder_data.split(":")[1]
#                encoder_label.config(text=f"Encoder: {encoder_value}")
#        time.sleep(0.1)

# Crear la ventana principal
root = tk.Tk()
root.title("Control de Motor Paso a Paso")

# Etiqueta para campo de pasos
steps_label = tk.Label(root, text="Pasos:")
steps_label.grid(row=0, column=0, padx=10, pady=5)

# Campo de entrada para los pasos
steps_entry = tk.Entry(root)
steps_entry.grid(row=0, column=1, padx=10, pady=5)

# Etiqueta para la selección de dirección
direction_label = tk.Label(root, text="Dirección:")
direction_label.grid(row=1, column=0, padx=10, pady=5)

# Variable de control para la dirección (0 para adelante, 1 para atrás)
direction_var = tk.IntVar()
direction_var.set(0)

# Botón de radio para la dirección hacia adelante
forward_radio = tk.Radiobutton(root, text="Atras", variable=direction_var, value=0)
forward_radio.grid(row=1, column=1, padx=10, pady=5)

# Botón de radio para la dirección hacia atrás
backward_radio = tk.Radiobutton(root, text="Adelante", variable=direction_var, value=1)
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

# Iniciar el hilo para actualizar los datos del sensor
#sensor_thread = threading.Thread(target=update_sensor_data)
#sensor_thread.daemon = True
#sensor_thread.start()

# Iniciar el bucle de eventos
root.mainloop()
