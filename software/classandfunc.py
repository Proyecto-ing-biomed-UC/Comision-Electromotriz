import serial
import tkinter as tk # interfaz de usuario
from functools import partial
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# control discreto PID
class PIDControl:
    def __init__(self, Kp, Ki, Kd, serie, dt=1):
        self.dt = dt # periodo de muestreo
        # constantes controlador de angulo discreto
        self.Kp = Kp
        self.Ki = Ki*dt
        self.Kd = Kd/dt
        # errores previos
        self.prev_err1 = 0
        self.prev_err2 = 0
        # entrada previa discretizacion via retencion de orden 0
        self.prev_u = 0

        # 
        self.estado_ant = None
        self.ser = serie
        self.verifica = False

    def calcular_control(self, referencia, estado):
        if self.verifica != False:
            estado_velocidad = (self.estado_ant - estado)/self.dt
            # calculo error y logica de control
            error_vel = referencia[1] - estado_velocidad
            error_pos = referencia[0] - estado
            if error_pos >= 0:
                direccion = 0 # hacia atras
            else:
                direccion = 1 # hacia delante
            err = np.abs(error_pos)
            # controlador
            u = self.prev_u + (self.Kp + self.Ki + self.Kd)*err - (self.Kp + 2*self.Kd)*self.prev_err1 + self.Kd*self.prev_err2
            # actualizacion de parametros
            if u > 0:
                direccion = 0
            else:
                direccion = 1
                
            u = np.abs(u)
            
            self.prev_err2 = self.prev_err1
            self.prev_err1 = err
            self.prev_u = u
            self.send_data_control(u, direccion)
        self.estado_ant = estado
        self.verifica = True

        return
    # enviar datos al Arduino
    def send_data_control(self, velocidad, direccion):
        print("Velocidad de control:", velocidad, "Dirección:", direccion)
        self.ser.write(f"<{velocidad},{direccion}>".encode('utf-8'))

def control_manual(ser):
    global vel_entry, dir_entry
    # ventana principal
    root = tk.Tk()
    root.title("Control de Motor")
    # etiqueta campo de velocidad
    vel_label = tk.Label(root, text="Velocidad:")
    vel_label.grid(row=0, column=0, padx=10, pady=5)
    # Campo de entrada para la velocidad
    vel_entry = tk.Entry(root)
    vel_entry.grid(row=0, column=1, padx=10, pady=5)

    # Etiqueta para la selección de dirección
    dir_label = tk.Label(root, text="Dirección:")
    dir_label.grid(row=1, column=0, padx=10, pady=5)

    # Variable de control para la dirección (0 atras, 1 adelante)
    dir_entry = tk.IntVar()
    dir_entry.set(0)

    # Botón de radio para la dirección hacia adelante
    forward_radio = tk.Radiobutton(root, text="Atras", variable=dir_entry, value=0)
    forward_radio.grid(row=1, column=1, padx=10, pady=5)

    # Botón de radio para la dirección hacia atrás
    backward_radio = tk.Radiobutton(root, text="Adelante", variable=dir_entry, value=1)
    backward_radio.grid(row=1, column=2, padx=10, pady=5)

    # Botón para enviar los datos al Arduino
    send_button = tk.Button(root, text="Enviar", command=partial(send_data, ser))
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


# enviar datos al Arduino
def send_data(ser):
    global vel_entry, dir_entry
    velocidad = vel_entry.get()
    direccion = dir_entry.get()
    ser.write(f"<{velocidad},{direccion}>".encode('utf-8'))

def lectura_referencia(nombre_archivo):
    datos = pd.read_csv(nombre_archivo, header=None)
    return datos


if __name__ == '__main__':
    dt = 0.01
    data = lectura_referencia('dataset.csv')
    angulos = data[0].tolist()
    vel_angular = np.gradient(angulos, dt)
    tiempo = np.arange(len(angulos))*dt
    # Graficar ángulos y velocidad angular
    plt.figure(figsize=(12, 6))

    # Gráfico de ángulos
    plt.subplot(2, 1, 1)
    plt.plot(tiempo, angulos, label='Ángulo')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Ángulo (rad)')
    plt.title('Ángulos en función del tiempo')
    plt.legend()
    plt.grid(True)

    # Gráfico de velocidad angular
    plt.subplot(2, 1, 2)
    plt.plot(tiempo[:-1], vel_angular[:-1], label='Velocidad Angular', color='orange')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Velocidad Angular (rad/s)')
    plt.title('Velocidad Angular en función del tiempo')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()

    