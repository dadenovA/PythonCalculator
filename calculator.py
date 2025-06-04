import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget,
                             QVBoxLayout, QGridLayout, QPushButton,
                             QLineEdit, QLabel, QSizePolicy)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon, QColor


class CalculatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculator")
        # resolution
        self.setGeometry(700, 250, 520, 680)
        self.setStyleSheet("background-color: #2d2d30;")

        # central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # layouts
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setSpacing(15)
        self.main_layout.setContentsMargins(25, 25, 25, 25)
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(12)

        # display
        self.result_display = QLineEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setAlignment(Qt.AlignRight)
        self.result_display.setFixedHeight(80)
        self.result_display.setStyleSheet("""
            font-size: 32px; 
            padding: 15px; 
            background-color: #1e1e1e;
            color: #ffffff;
            border: 1px solid #3f3f46;
            border-radius: 8px;
            margin-bottom: 8px;
        """)
        # current calculation disoplay
        self.expression_display = QLabel("")
        self.expression_display.setAlignment(Qt.AlignRight)
        self.expression_display.setStyleSheet("""
            font-size: 18px; 
            color: #b4b4b4;
            padding: 5px;
            margin-bottom: 20px;
        """)

        self.main_layout.addWidget(self.result_display)
        self.main_layout.addWidget(self.expression_display)

        # CSS for buttons
        self.number_style = """
            QPushButton {
                background-color: #3e3e42;
                border: 1px solid #505054;
                border-radius: 8px;
                font-size: 22px;
                font-weight: bold;
                color: #ffffff;
                padding: 15px;
            }
            QPushButton:hover {
                background-color: #505054;
            }
            QPushButton:pressed {
                background-color: #68686c;
            }
        """

        self.operator_style = """
            QPushButton {
                background-color: #007acc;
                border: 1px solid #005f9e;
                border-radius: 8px;
                font-size: 22px;
                font-weight: bold;
                color: #ffffff;
                padding: 15px;
            }
            QPushButton:hover {
                background-color: #1c97ea;
            }
            QPushButton:pressed {
                background-color: #0063a8;
            }
        """

        self.equal_style = """
            QPushButton {
                background-color: #6a9955;
                border: 1px solid #588048;
                border-radius: 8px;
                font-size: 22px;
                font-weight: bold;
                color: #ffffff;
                padding: 15px;
            }
            QPushButton:hover {
                background-color: #7cb668;
            }
            QPushButton:pressed {
                background-color: #588048;
            }
        """

        self.clear_style = """
            QPushButton {
                background-color: #d16969;
                border: 1px solid #b05454;
                border-radius: 8px;
                font-size: 20px;
                font-weight: bold;
                color: #ffffff;
                padding: 15px;
            }
            QPushButton:hover {
                background-color: #e07979;
            }
            QPushButton:pressed {
                background-color: #b05454;
            }
        """

        self.function_style = """
            QPushButton {
                background-color: #5a4c7b;
                border: 1px solid #4a3f66;
                border-radius: 8px;
                font-size: 20px;
                font-weight: bold;
                color: #ffffff;
                padding: 15px;
            }
            QPushButton:hover {
                background-color: #6a5c8b;
            }
            QPushButton:pressed {
                background-color: #4a3f66;
            }
        """

        # first 4 rows
        buttons = [
            ('7', 0, 0, self.number_style), ('8', 0, 1, self.number_style), ('9', 0, 2, self.number_style),
            ('÷', 0, 3, self.operator_style),
            ('4', 1, 0, self.number_style), ('5', 1, 1, self.number_style), ('6', 1, 2, self.number_style),
            ('×', 1, 3, self.operator_style),
            ('1', 2, 0, self.number_style), ('2', 2, 1, self.number_style), ('3', 2, 2, self.number_style),
            ('-', 2, 3, self.operator_style),  # Changed from '−' to '-'
            ('0', 3, 0, self.number_style), ('.', 3, 1, self.number_style), ('=', 3, 2, self.equal_style),
            ('+', 3, 3, self.operator_style),
        ]

        # fifth row
        function_buttons = [
            ('C', 4, 0, self.clear_style), ('(', 4, 1, self.function_style), (')', 4, 2, self.function_style),
            ('⌫', 4, 3, self.function_style),
            ('x²', 5, 0, self.function_style), ('√x', 5, 1, self.function_style), ('%', 5, 2, self.function_style),
            ('±', 5, 3, self.function_style)
        ]

        all_buttons = buttons + function_buttons
        for button_text, row, col, style in all_buttons:
            button = QPushButton(button_text)
            button.setMinimumSize(100, 80)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            button.setStyleSheet(style)
            button.clicked.connect(self.button_clicked)
            self.grid_layout.addWidget(button, row, col)
        self.main_layout.addLayout(self.grid_layout)
        self.current_input = ""
        self.last_result = ""
        self.last_was_operator = False
        self.last_was_equal = False

    def button_clicked(self):
        button = self.sender()
        button_text = button.text()
        if button_text == "C":
            self.clear_display()
        elif button_text == "⌫":
            self.current_input = self.current_input[:-1]
            self.update_display()
        elif button_text == "=":
            self.calculate_result()
        elif button_text == "±":
            try:
                # search for the last number
                if self.current_input and self.current_input[-1].isdigit():
                    # finding start of the last nubmer
                    i = len(self.current_input) - 1
                    while i >= 0 and (self.current_input[i].isdigit() or self.current_input[i] == '.'):
                        i -= 1
                    i += 1
                    expr_start = self.current_input[:i]
                    number = self.current_input[i:]
                    if float(number) > 0:
                        self.current_input = f"{expr_start}(-{number})"
                    else:
                        self.current_input = f"{expr_start}{abs(float(number))}"
                else:
                    if self.last_was_equal and self.current_input:
                        self.current_input = str(-float(self.current_input))

                self.update_display()
            except:
                self.result_display.setText("Error")

        elif button_text == "x²":
            if self.current_input:
                try:
                    if self.last_was_equal:
                        val = float(self.current_input)
                        self.current_input = str(val ** 2)
                    else:
                        self.current_input += "**2"
                    self.update_display()
                except:
                    self.result_display.setText("Error")

        elif button_text == "√x":
            try:
                if self.last_was_equal:
                    val = float(self.current_input)
                    if val >= 0:
                        self.current_input = str(val ** 0.5)
                    else:
                        self.result_display.setText("Error")
                        return
                else:
                    self.current_input = f"({self.current_input})**0.5"
                self.update_display()
            except:
                self.result_display.setText("Error")

        elif button_text == "%":
            try:
                if self.current_input:
                    if self.last_was_equal:
                        val = float(self.current_input)
                        self.current_input = str(val / 100)
                    else:
                        i = len(self.current_input) - 1
                        while i >= 0 and (self.current_input[i].isdigit() or self.current_input[i] == '.'):
                            i -= 1
                        i += 1
                        expr_start = self.current_input[:i]
                        number = self.current_input[i:]

                        if number:
                            percentage = float(number) / 100
                            self.current_input = f"{expr_start}{percentage}"
                    self.update_display()
            except:
                self.result_display.setText("Error")

        elif button_text in "0123456789.()":
            # Start new after '='
            if self.last_was_equal and button_text in "0123456789.":
                self.current_input = button_text
            else:
                self.current_input += button_text
            self.last_was_equal = False
            self.last_was_operator = False
            self.update_display()

        elif button_text in "+-×÷":  # Operators
            # visual to actual buttons
            op_map = {"×": "*", "÷": "/", "-": "-", "+": "+"}
            if not self.last_was_operator:
                self.current_input += op_map[button_text]
                self.last_was_operator = True
                self.last_was_equal = False
                self.update_display()
            else:
                self.current_input = self.current_input[:-1] + op_map[button_text]
                self.update_display()

    def calculate_result(self):
        if self.current_input:
            try:
                expression = self.current_input.replace("×", "*").replace("÷", "/")

                self.expression_display.setText(self.current_input + " =")

                result = eval(expression)

                if isinstance(result, float):
                    if result.is_integer():
                        formatted_result = str(int(result))
                    else:
                        formatted_result = str(result)
                else:
                    formatted_result = str(result)

                self.result_display.setText(formatted_result)
                self.current_input = formatted_result
                self.last_was_equal = True
                self.last_was_operator = False

            except Exception as e:
                self.result_display.setText("Error")
                self.expression_display.setText("Invalid expression")
                self.current_input = ""

    def update_display(self):
        if self.current_input:
            display_text = self.current_input
            display_text = display_text.replace("*", "×").replace("/", "÷")
            self.result_display.setText(display_text)
        else:
            self.result_display.setText("0")
            self.expression_display.setText("")

    def clear_display(self):
        self.current_input = ""
        self.last_was_equal = False
        self.last_was_operator = False
        self.result_display.setText("0")
        self.expression_display.setText("")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    font = QFont("Segoe UI", 11)
    app.setFont(font)

    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    calculator = CalculatorApp()
    calculator.show()
    sys.exit(app.exec_())