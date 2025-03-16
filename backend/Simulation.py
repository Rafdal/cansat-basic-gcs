import Commands

class Simulation():

    def __init__(self):
        simp_data_file = open("sim/cansat_2025_simp.txt", "r") 
        raw_data_file = simp_data_file.read().split("\n")
        commands = [line for line in raw_data_file if line and line.startswith("CMD")]
        self.commands_list = [line.replace("$,SIMP,", "2099,SIMP, ") for line in commands]
        self.index = 0
        self.initialized = False
        self.commands = Commands()

    def init(self):
        self.initialized = True

    def send_command(self, xbee):
        print(f"Simulation mode sended: {self.commands_list[self.index]}")
        sent = self.commands_list[self.index].split(",")[3]
        self.commands.callback_command(xbee = xbee.xbee, msg = self.commands_list[self.index])
        self.index = self.index + 1
        if (self.index == len(self.commands_list)):
            self.initialized = False
        return sent
             