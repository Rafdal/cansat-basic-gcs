
class Commands():

    def callback_command(self, xbee, msg):
        msg = msg + "\n"
        xbee.write(msg.encode(encoding = 'ascii', errors = 'strict'))
        xbee.flush()
        print(msg)
    
    def set_time_handler(self, xbee):
        print("Set time") # TODO: missing parameters: utc_time or gps
        command = "CMD,2099,ST, 00:00:00"
        self.callback_command(xbee=xbee.xbee, msg=command)

    def start_telemetry_handler(self, xbee):
        xbee.xbee.reset_output_buffer()
        command = "CMD,2099,CX,ON"
        self.callback_command(xbee=xbee.xbee, msg=command)

    def end_telemetry_handler(self, xbee):
        command = "CMD,2099,CX,OFF"
        self.callback_command(xbee=xbee.xbee, msg=command)

    def cal_altitude_handler(self, xbee):
        command = "CMD,2099,CAL"
        self.callback_command(xbee=xbee.xbee, msg=command)

    def set_pyr_handler(self, xbee):
        command = "CMD,2099,CAL_PITCHROLL"
        self.callback_command(xbee=xbee.xbee, msg=command)

    def enable_sim_mode_handler(self, xbee):
        command = "CMD,2099,SIM,ENABLE"
        self.callback_command(xbee=xbee.xbee, msg=command)

    def activate_sim_mode_handler(self, xbee):
        command = "CMD,2099,SIM,ACTIVATE"
        self.callback_command(xbee=xbee.xbee, msg=command)

    def deactivate_sim_mode_handler(self, xbee):
        command = "CMD,2099,SIM,DISABLE"
        self.callback_command(xbee=xbee.xbee, msg=command)

    def activate_bcn_handler(self, xbee):
        command = "CMD,2099,BCN,ON"
        self.callback_command(xbee=xbee.xbee, msg=command)

    def deactivate_bcn_handler(self, xbee):
        command = "CMD,2099,BCN,OFF"
        self.callback_command(xbee=xbee.xbee, msg=command)

    def start_recording_handler(self, xbee):
        command = "CMD,2099,RECORD_INIT"
        self.callback_command(xbee=xbee.xbee, msg=command)

    def stop_recording_handler(self, xbee):
        command = "CMD,2099,RECORD_STOP"
        self.callback_command(xbee=xbee.xbee, msg=command)


    