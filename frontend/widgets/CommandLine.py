from backend.Commands import Commands
from PyQt5.QtWidgets import QLineEdit, QPushButton, QHBoxLayout, QLabel

class CommandLine:

    def __init__(self, center_widget, xbee):

        title_style = '''QLabel{font-size:24px; margin:5px; font-weight:600;}'''
        self.commands = Commands()

        self.command_line_layout = QHBoxLayout()

        # Command line
        custom_command_title = QLabel('Send Command', center_widget)
        custom_command_title.setStyleSheet(title_style)
        self.command_line = QLineEdit(center_widget)
        self.command_line.setStyleSheet('''QLineEdit{font-size:24px; padding:5px; font-weight:350;}''')
        send_command_btn = QPushButton("SEND" , center_widget)
        send_command_btn.setStyleSheet('''QPushButton{font-size:22px; margin:5px; padding:5px; height:30px;}''')
        send_command_btn.clicked.connect(lambda: self.command_line_handler(xbee, msg=self.command_line.text()))

        self.command_line_layout.addWidget(custom_command_title)
        self.command_line_layout.addWidget(self.command_line)
        self.command_line_layout.addWidget(send_command_btn)

    def command_line_handler(self, xbee, msg):
        self.commands.callback_command(xbee=xbee, msg=msg)
        self.command_line.clear()