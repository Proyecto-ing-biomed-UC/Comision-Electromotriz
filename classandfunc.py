# control discreto PID
class PIDControl:
    def __init__(self, Kp, Ki, Kd, dt=1):
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

    def calcular_control(self, err):
        # controlador
        u = self.prev_u + (self.Kp + self.Ki + self.Kd)*err - (self.Kp + 2*self.Kd)*self.prev_err1 + self.Kd*self.prev_err2
        # actualizacion de parametros
        self.prev_err2 = self.prev_err1
        self.prev_err1 = err
        self.prev_u = u
        return u