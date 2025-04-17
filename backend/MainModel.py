from utils.ParamList import ParameterList, NumParam, BoolParam, TextParam, ChoiceParam, ConstParam
from backend.serial.SerialPortHandler import SerialPortHandler
from PyQt5.QtCore import QTimer

class MainModel:

    # Initialization of Model members
    def __init__(self) -> None:
        self.serial = SerialPortHandler()
        self.timer = QTimer()
        self.timer_callback = None
        self.timer.timeout.connect(self._on_timer_timeout)

    # Method to start the periodic timer
    def start_timer(self, interval_ms: int) -> None:
        """
        Starts the timer with the specified interval in milliseconds.
        The timer will trigger the callback periodically.
        """
        self.timer.start(interval_ms)

    # Method to stop the timer
    def stop_timer(self) -> None:
        """Stops the timer."""
        self.timer.stop()

    # Method to attach a callback function to the timer
    def attach_timer_callback(self, callback) -> None:
        """
        Attaches a callback function to be executed on timer timeout.
        :param callback: A callable function to be executed periodically.
        """
        self.timer_callback = callback

    # Internal method triggered on timer timeout
    def _on_timer_timeout(self) -> None:
        """Internal method called when the timer times out."""
        if self.timer_callback:
            self.timer_callback()