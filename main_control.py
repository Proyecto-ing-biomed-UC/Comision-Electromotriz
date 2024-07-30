#import tkinter as tk # interfaz de usuario
import serial # comunicacion con arduino
import time
import threading # multitask
from classandfunc import *
import numpy as np
import sys

# Configurar la conexión serial
# puerto: cambia segun el sistema operativo y puerto
# window: COM3, linux: /dev/ttyUSB0, mac: 
arduino_port = 'COM3'
baud_rate = 9600 # velocidad de transmisión en baudios
ser = serial.Serial(arduino_port, baud_rate)
time.sleep(2)  # esperar a que la conexión serial se establezca
tipo_control = 0 # 0 manual, 1 automatico
dt = 0.01

if __name__ == '__main__':
    archivo_csv = 'dataset.csv'
    data = lectura_referencia(archivo_csv)
    data = data[0].tolist()
    velocidad = np.gradient(data, dt)
    #print(data)
    if tipo_control == 0:
        # tener ojo con la acumulacion de mensaje del arduino
        control_manual(ser)
    elif tipo_control == 1:
        # inicializar controlador
        Kp = 1; Ki = 0; Kd = 0
        controlador_vel_pos = PIDControl(Kp, Ki, Kd, ser, dt=dt)
        # loop lectura estado y control
        tiempo_referencia = 0
        while True:
            if ser.in_waiting > 0:
                estado = ser.readline().decode('utf-8').rstrip()
                # se envian otros mensajes en el debug
                #print(estado)
                referencia = [data[tiempo_referencia], velocidad[tiempo_referencia]]
                referencia = [100, 0]
                if estado.isdigit():
                    print(estado)
                    controlador_vel_pos.calcular_control(referencia, int(estado))
                tiempo_referencia += 1