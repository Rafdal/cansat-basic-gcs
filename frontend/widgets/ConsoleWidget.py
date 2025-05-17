from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QScrollArea, QHBoxLayout, QTextEdit, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QTextCursor, QColor
from frontend.widgets.BasicWidgets import TextInput, Button

class ConsoleWidget(QWidget):
    def __init__(self, textSelectable=True, wordWrap=True, defaultText="Console output will appear here...", fixedWidth=None, maxBlockCount=1000):
        super(ConsoleWidget, self).__init__()
        
        self.defaultText = defaultText

        # Size policy to make the widget expand as much as possible
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        if fixedWidth:
            self.setFixedWidth(fixedWidth)
        
        # Create the QLabel that will display the console output
        self.consoleOutput = QTextEdit()
        self.consoleOutput.setReadOnly(True)
        self.consoleOutput.setWordWrapMode(wordWrap)
        self.consoleOutput.setFont(QFont("Monospace", 10))
        self.consoleOutput.setText(defaultText + '\n')
        self.consoleOutput.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        # Make the text area expand to fill available space
        self.consoleOutput.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.consoleOutput.setMinimumHeight(200)  # Set a reasonable minimum height
        
        if textSelectable:
            self.consoleOutput.setTextInteractionFlags(Qt.TextSelectableByMouse)
        
        self.consoleOutput.document().setMaximumBlockCount(maxBlockCount)
        
        self.lineCount = QLabel("Lines: 0")
        
        # Create a QVBoxLayout for this widget and add the QScrollArea to it
        vlayout = QVBoxLayout(self)
        topHLayout = QHBoxLayout()
        topHLayout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        topHLayout.addWidget(self.lineCount)
        topHLayout.addStretch(1)
        topHLayout.addWidget(Button("Clear", on_click=lambda: self.clearConsole()))
        vlayout.addLayout(topHLayout)
        vlayout.addWidget(self.consoleOutput)
        
        # Set the layout for this widget
        self.setLayout(vlayout)
        
        # Additional styling or functionality can be added here as needed

    def clear(self):
        self.clearConsole()

    def clearConsole(self):
        self.consoleOutput.clear()
        self.setText(self.defaultText)

    def setText(self, text):
        self.consoleOutput.setTextColor(QColor(0, 0, 0))
        self.consoleOutput.setText(text)
        newlines = text.count('\n')+1
        self.lineCount.setText(f"Lines: {newlines}")

    def appendText(self, text, color=QColor(0, 0, 0)):
        # Method to append text to the console, improving performance for large updates
        self.consoleOutput.moveCursor(QTextCursor.End)
        self.consoleOutput.setTextColor(color)
        self.consoleOutput.insertPlainText(text)
        # Update line count
        newlines = self.consoleOutput.toPlainText().count('\n') + 1
        self.lineCount.setText(f"Lines: {newlines}")