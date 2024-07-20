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
tipo_control = 1 # 0 manual, 1 automatico

# logica de control
def controlador(referencia, estado):
    error = referencia - estado
    if error >= 0:
        direccion = 0 # hacia atras
    else:
        direccion = 1 # hacia delante
    error = np.abs(error)
    senal_control = controlador_angulo.calcular_control(error)
    send_data_control(senal_control, direccion)

# enviar datos al Arduino
def send_data_control(velocidad, direccion):
    #print("Velocidad de control:", velocidad, "Dirección:", direccion)
    ser.write(f"<{velocidad},{direccion}>".encode('utf-8'))
    

if __name__ == '__main__':
    archivo_csv = 'dataset.csv'
    data = lectura_referencia(archivo_csv)
    data = data[0].tolist()
    #print(data)
    if tipo_control == 0:
        # tener ojo con la acumulacion de mensaje del arduino
        control_manual(ser)
    elif tipo_control == 1:
        # inicializar controlador
        Kp = 1; Ki = 0; Kd = 0
        controlador_angulo = PIDControl(Kp, Ki, Kd, dt=0.01)
        # loop lectura estado y control
        tiempo_referencia = 0
        while True:
            if ser.in_waiting > 0:
                estado = ser.readline().decode('utf-8').rstrip()
                # se envian otros mensajes en el debug
                print(estado)
                referencia = data[tiempo_referencia]
                if estado.isdigit():
                    print(estado)
                    controlador(100, int(estado))
                tiempo_referencia += 1