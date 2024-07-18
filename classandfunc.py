# control discreto PID
class PIDControl:
    def __init__(self, Kpa, Kia, Kda, dt=1):
        self.dt = dt # periodo de muestreo
        # constantes controlador de angulo discreto
        self.Kp = Kpa
        self.Ki = Kia*dt
        self.Kd = Kda/dt
        # errores previos
        self.prev_err1 = 0
        self.prev_err2 = 0
        # entrada previa discretizacion via retencion de orden 0
        self.prev_u = 0

    def calcular_control(self, err):
        # controlador
        u = self.prev_u_a + (self.Kp + self.Ki + self.Kd)*err - (self.Kp + 2*self.Kd)*self.prev_err1_a + self.Kd*self.prev_err2_a
        # actualizacion de parametros
        self.prev_err2_a = self.prev_err1_a
        self.prev_err1_a = err
        self.prev_u_a = u
        return u