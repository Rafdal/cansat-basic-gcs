from backend.Commands import Commands
import numpy as np

# 2024 legacy code 
class SimulationMode():

    def __init__(self):
        simp_data_file = open("sim/cansat_2025_simp.txt", "r") 
        raw_data_file = simp_data_file.read().split("\n")
        commands = [line for line in raw_data_file if line and line.startswith("CMD")]
        self.commands_list = [line.replace("$,SIMP,", "3165,SIMP, ") for line in commands]
        self.index = 0
        self.initialized = False
        self.commands = Commands()

    def enable(self):
        self.initialized = True

    def send_command(self, xbee = None):
        print(f"Simulation mode sended: {self.commands_list[self.index]}")
        sent = self.commands_list[self.index].split(",")[3]
        
        if (xbee is None or isinstance(xbee, str)):
            return np.float64(93948)    # WORKAROUND (crasheaba)
        
        self.commands.callback_command(xbee = xbee.xbee, msg = self.commands_list[self.index])
        self.index = self.index + 1
        if (self.index == len(self.commands_list)):
            self.initialized = False
        return sent
             