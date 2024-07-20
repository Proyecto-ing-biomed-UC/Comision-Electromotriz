#class PIDControl {
#  public:
#    float Kp;
#    float Ki;
#    float Kd;
#    float dt;
#    float prev_err1;
#    float prev_err2;
#    float prev_u;
#
#    // Constructor
#    PIDControl(float kp, float ki, float kd, float samplingPeriod = 1.0) {
#      dt = samplingPeriod;
#      Kp = kp;
#      Ki = ki * dt;
#      Kd = kd / dt;
#      prev_err1 = 0.0;
#      prev_err2 = 0.0;
#      prev_u = 0.0;
#    }
#
#    // Método para calcular el control
#    float calcular_control(float err) {
#      float u = prev_u + (Kp + Ki + Kd) * err - (Kp + 2 * Kd) * prev_err1 + Kd * prev_err2;
#      prev_err2 = prev_err1;
#      prev_err1 = err;
#      prev_u = u;
#      return u;
#    }
#};
// Ejemplo de uso en el loop de Arduino
//PIDControl pidControl(1.0, 0.1, 0.01, 1.0);


#thread = threading.Thread(target=read_serial, args=(ser,))
#thread.daemon = True  # Permite que el hilo se cierre al cerrar el programa
#thread.start()


from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QRadioButton, QPushButton, QVBoxLayout, QHBoxLayout, QButtonGroup
from PyQt5.QtCore import Qt
#app = QApplication(sys.argv)
        #ex = MotorControl(ser)
        #ex.show()
        #sys.exit(app.exec_())

class MotorControl(QWidget):
    def __init__(self, serial):
        super().__init__()
        self.ser = serial
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Control de Motor')

        # Campo de velocidad
        vel_label = QLabel('Velocidad:')
        self.vel_entry = QLineEdit()

        # Layout para la velocidad
        vel_layout = QHBoxLayout()
        vel_layout.addWidget(vel_label)
        vel_layout.addWidget(self.vel_entry)

        # Selección de dirección
        dir_label = QLabel('Dirección:')

        self.dir_group = QButtonGroup(self)
        forward_radio = QRadioButton('Atras')
        forward_radio.setChecked(True)
        backward_radio = QRadioButton('Adelante')
        self.dir_group.addButton(forward_radio, 0)
        self.dir_group.addButton(backward_radio, 1)

        # Layout para la dirección
        dir_layout = QHBoxLayout()
        dir_layout.addWidget(dir_label)
        dir_layout.addWidget(forward_radio)
        dir_layout.addWidget(backward_radio)

        # Botón para enviar datos
        send_button = QPushButton('Enviar')
        send_button.clicked.connect(self.send_data)

        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.addLayout(vel_layout)
        main_layout.addLayout(dir_layout)
        main_layout.addWidget(send_button)

        self.setLayout(main_layout)

    def send_data(self):
        velocidad = self.vel_entry.text()
        direccion = self.dir_group.checkedId()
        #print(f'Velocidad: {velocidad}, Dirección: {"Atras" if direccion == 0 else "Adelante"}')
        self.ser.write(f"<{velocidad},{direccion}>".encode('utf-8'))

    def closeEvent(self, event):
        event.accept()
        self.ser.close()