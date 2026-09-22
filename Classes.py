class PID:
    def __init__(self, Kp, Ki, Kd, output_limits = (None, None)):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.setpoint = 0
        self.error_sum = 0
        self.prev_error = 0
        self.output_min, self.output_max = output_limits