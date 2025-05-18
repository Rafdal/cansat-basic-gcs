from PyQt5.QtCore import pyqtSignal, QObject

class Commands(QObject):
    cx_on = False
    send_command = pyqtSignal(str)  # Signal to send command to XBee
    
    # ST
    def set_time_handler(self):
        # TODO: missing parameters utc_time or gps and the time
        command = "CMD,3165,ST,00:00:00"
        self.send_command.emit(command)

    # CX - ON
    def start_telemetry_handler(self):
        command = "CMD,3165,CX,ON"
        self.send_command.emit(command)

    # CX - OFF
    def end_telemetry_handler(self):
        command = "CMD,3165,CX,OFF"
        self.send_command.emit(command)

    # FIXME: A VECES CUANDO LE MANDO OFF, NO SE APAGA :(
    def toggle_telemetry_handler(self) -> bool:
        """ CX - TOGGLE
        This function toggles the telemetry mode between ON and OFF.
        It emits a command to the XBee device to change the telemetry mode.
        
        Returns:
            active (bool): The new telemetry mode (True for ON, False for OFF).
        """
        self.cx_on = not self.cx_on
        mode_str = "ON" if self.cx_on else "OFF"
        command = f"CMD,3165,CX,{mode_str}"
        self.send_command.emit(command)
        print(f"\tSending COMMAND: \'{command}\'")  
        return self.cx_on

    # CAL
    def cal_altitude_handler(self):
        command = "CMD,3165,CAL"
        self.send_command.emit(command)

    # CAL_PR
    def set_pr_handler(self):
        command = "CMD,3165,CAL_PR"
        self.send_command.emit(command)

    # SIM - ENABLE
    def enable_sim_mode_handler(self):
        command = "CMD,3165,SIM,ENABLE"
        self.send_command.emit(command)

    # SIM - ACTIVATE
    def activate_sim_mode_handler(self):
        command = "CMD,3165,SIM,ACTIVATE"
        self.send_command.emit(command)

    # SIM - DISABLE
    def deactivate_sim_mode_handler(self):
        command = "CMD,3165,SIM,DISABLE"
        self.send_command.emit(command)

    # MEC - ACTIVATE n
    def activate_mec(self, number):
        command = f"CMD,3165,MEC,{number},ON"
        self.send_command.emit(command)

    # MEC - DEACTIVATE n
    def deactivate_mec(self, number):
        command = f"CMD,3165,MEC,{number},OFF"
        self.send_command.emit(command)


    