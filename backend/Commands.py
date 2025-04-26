
class Commands():

    def callback_command(self, xbee, msg):
        # msg = msg + "\n"
        # xbee.write(msg.encode(encoding = 'ascii', errors = 'strict'))
        # xbee.flush()
        print(msg)
    
    # ST
    def set_time_handler(self, xbee):
        # TODO: missing parameters utc_time or gps and the time
        command = "CMD,3165,ST,00:00:00"
        self.callback_command(xbee=xbee, msg=command)

    # CX - ON
    def start_telemetry_handler(self, xbee):
        command = "CMD,3165,CX,ON"
        self.callback_command(xbee=xbee, msg=command)

    # CX - OFF
    def end_telemetry_handler(self, xbee):
        command = "CMD,3165,CX,OFF"
        self.callback_command(xbee=xbee, msg=command)

    # CAL
    def cal_altitude_handler(self, xbee):
        command = "CMD,3165,CAL"
        self.callback_command(xbee=xbee, msg=command)

    # CAL_PR
    def set_pr_handler(self, xbee):
        command = "CMD,3165,CAL_PR"
        self.callback_command(xbee=xbee, msg=command)

    # SIM - ENABLE
    def enable_sim_mode_handler(self, xbee):
        command = "CMD,3165,SIM,ENABLE"
        self.callback_command(xbee=xbee, msg=command)

    # SIM - ACTIVATE
    def activate_sim_mode_handler(self, xbee):
        command = "CMD,3165,SIM,ACTIVATE"
        self.callback_command(xbee=xbee, msg=command)

    # SIM - DISABLE
    def deactivate_sim_mode_handler(self, xbee):
        command = "CMD,3165,SIM,DISABLE"
        self.callback_command(xbee=xbee, msg=command)

    # MEC - ACTIVATE n
    def activate_mec(self, xbee, number):
        command = f"CMD,3165,MEC,{number},ON"
        self.callback_command(xbee=xbee, msg=command)

    # MEC - DEACTIVATE n
    def deactivate_mec(self, xbee, number):
        command = f"CMD,3165,MEC,{number},OFF"
        self.callback_command(xbee=xbee, msg=command)


    