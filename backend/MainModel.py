from utils.ParamList import ParameterList, NumParam, BoolParam, TextParam, ChoiceParam, ConstParam
from backend.serial.SerialPortHandler import SerialPortHandler

class MainModel:

    # Initialization of Model members
    def __init__(self) -> None:
        self.serial = SerialPortHandler()
        pass
