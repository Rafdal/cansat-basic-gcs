from PyQt5.QtCore import pyqtSignal, QObject

class Commands(QObject):
    cx_on = False
    send_command = pyqtSignal(str)  # Signal to send command to XBee
    print_debug = pyqtSignal(str)  # Signal to print debug messages
    
    # ST
    def set_time_handler(self):
        # TODO: missing parameters utc_time or gps and the time
        command = "CMD,3165,ST,00:00:00"
        self.send_command.emit(command)

    # CX - ON
    def start_telemetry_handler(self):
        command = "CMD,3165,CX,ON"
        self.send_command.emit(command)
        self.print_debug.emit(f"\tSending COMMAND: \'{command}\'")

    # CX - OFF
    def end_telemetry_handler(self):
        command = "CMD,3165,CX,OFF"
        self.send_command.emit(command)
        self.print_debug.emit(f"\tSending COMMAND: \'{command}\'")

    # CAL
    def cal_altitude_handler(self):
        command = "CMD,3165,CAL"
        self.send_command.emit(command)
        self.print_debug.emit(f"\tSending COMMAND: \'{command}\'")

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


    