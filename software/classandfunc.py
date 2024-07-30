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
        self.ser = serie
        self.verifica = False

        # filtro promedio
        self.estado = None
        self.estado_ant1 = 0
        self.estado_ant2 = 0
        self.estado_ant3 = 0
        self.estado_ant4 = 0
        self.conteo = 0

    def calcular_control(self, referencia, estado):
        if self.verifica != False:
            estado_velocidad = (self.estado_ant1 - estado)/self.dt
            # calculo error y logica de control
            error_vel = referencia[1] - estado_velocidad
            error_pos = referencia[0] - estado
            if error_pos >= 0:
                direccion = 1 # hacia atras
            else:
                direccion = 0 # hacia delante
            #print("error_pos", error_pos)
            err = error_pos
            # controlador
            u = self.prev_u + (self.Kp + self.Ki + self.Kd)*err - (self.Kp + 2*self.Kd)*self.prev_err1 + self.Kd*self.prev_err2
            #u = self.prev_u + (self.Kp + self.Ki + self.Kd)*err
            # actualizacion de parametros
            #print("u", u)
            #if u >= 0:
            #    direccion = 0
            #else:
            #    direccion = 1
                
            u = np.abs(u)
            if u > 255:
                u = 255
            elif u < 0:
                u = 0
            
            self.prev_err2 = self.prev_err1
            self.prev_err1 = err
            self.prev_u = u
            self.send_data_control(int(u), direccion)
        self.verifica = True
        self.conteo += 1
        self.estado_ant4 = self.estado_ant3
        self.estado_ant3 = self.estado_ant2
        self.estado_ant2 = self.estado_ant1
        self.estado_ant1 = estado
        return
    # enviar datos al Arduino
    def send_data_control(self, velocidad, direccion):
        print("Velocidad de control:", velocidad, "Dirección:", direccion)
        self.ser.write(f"<{velocidad},{direccion}>".encode('utf-8'))

def filtro_estado(controlador_vel_pos, estado):
    estados = controlador_vel_pos.conteo
    if estados == 0:
        div = 1
        estado = estado/div
    elif estados == 1:
        div = 2
        print("estado filtro:", estado, controlador_vel_pos.estado_ant1)
        estado = (estado + controlador_vel_pos.estado_ant1)/div
    elif estados == 2:
        div = 3
        estado = (estado + controlador_vel_pos.estado_ant1 + controlador_vel_pos.estado_ant2)/div
    elif estados == 3:
        div = 4
        estado = (estado + controlador_vel_pos.estado_ant1 + controlador_vel_pos.estado_ant2 + controlador_vel_pos.estado_ant3)/div
    elif estados >= 4:
        div = 5
        estado = (estado + controlador_vel_pos.estado_ant1 + controlador_vel_pos.estado_ant2 + controlador_vel_pos.estado_ant3 + controlador_vel_pos.estado_ant4)/div
    #print("estado filtro:", estado)
    return estado
        
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
    forward_radio = tk.Radiobutton(root, text="Estirar", variable=dir_entry, value=0)
    forward_radio.grid(row=1, column=1, padx=10, pady=5)

    # Botón de radio para la dirección hacia atrás
    backward_radio = tk.Radiobutton(root, text="Flectar", variable=dir_entry, value=1)
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
    print(velocidad, direccion)
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

    