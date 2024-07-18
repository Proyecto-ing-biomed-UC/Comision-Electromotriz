# Control Automático Ciervo
El archivo mov_simple.ino es el código básico que cambia periódicamente de dirección.

Diego: Cree un archivo nuevo mov_simple.ino que logra implementar un lazo abierto enviando codigos desde python con el archivo senal_control.py. Tambien añadi codigo para leer un encoder (todo esto quedo comentado ya que aun no añadimos sensores).

Ignacio: Archivo steps.py: entrega a velocidades.ino un valor de velocidad (1, 2 o 3). Archivo velocidades.ino: recibe el comando de velocidad y lo entrega al arduino.

Ignacio: Archivo dir_vel_tiempo.py: envía un comando del formato F1T1, donde F o B indica la dirección, el primer número la velocidad, T indica que sigue el tiempo y el último número indica la duración del pulso. Archivo dir_vel_t.ino recibe el comando de dir_vel_tiempo.py y lo envía al arduino.
