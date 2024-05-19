from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget, QPushButton

import sys
import math
import cmath
import gettext
import locale
import os

gettext.bindtextdomain("messages", "locales")
gettext.textdomain("messages")

# Get the current directory of your Python script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define the relative path to the "locales" directory
locales_dir = os.path.join(current_dir, "locales")

# Update the localedir parameter with the relative path to the "locales" directory
lc = locale.getlocale()[0]  # Extract the language code from the tuple
if lc == 'English_United Kingdom':
    lc = 'en'
lang = gettext.translation("messages", localedir=locales_dir, fallback=True, languages=[lc])
lang.install()

_ = lang.gettext
#_ = gettext.gettext


def extract_square_root(get_text, set_text, get_precision):
    def inner_function():
        try:
            precision_input = get_precision()

            if precision_input == "":
                precision = 5
            elif precision_input.isdigit() and int(precision_input) < 26:
                precision = int(precision_input)
            else:
                set_text(_("Ошибка: Точность должна быть положительным числом и не больше 25!"))
                return

            number = float(get_text())

            if number == 0:
                result = 0
            elif number < 0:
                complex_root = cmath.sqrt(number)
                result = complex_root
            else:
                result = math.sqrt(number)
# Аналитическое вычисление корня
                xn = number
                while True:
                    xn1 = 0.5 * (xn + number/xn)
                    if abs(xn - xn1) < 10 ** (-precision):
                        break
                    xn = xn1
                analytical_root = xn

            if isinstance(result, complex):
                set_text(f"{result.real:.{precision}f} + {result.imag:.{precision}f}i")
            else:
                set_text(f"{result:.{precision}f}")
                set_text(_("Арифметический корень: ") + f"{result:.{precision}f}" + '\n' + _("Аналитический корень: ") + f"{analytical_root:.{precision}f}")

        except ValueError:
            set_text(_("Ошибка: Неверный ввод. Пожалуйста, введите число."))
    return inner_function



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(_("Калькулятор квадратного корня"))
        self.setFixedSize(500,300)

        layout = QVBoxLayout()

        precision_label = QLabel(_("Точность:"))
        self.precision_input = QLineEdit()
        layout.addWidget(precision_label)
        layout.addWidget(self.precision_input)

        number_label = QLabel(_("Число:"))
        self.input = QLineEdit()
        layout.addWidget(number_label)
        layout.addWidget(self.input)

        self.label = QLabel()
        button = QPushButton(_("Вычислить"))
        layout.addWidget(button)
        layout.addWidget(self.label)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        button.clicked.connect(extract_square_root(self.input.text, self.label.setText, self.precision_input.text))

        support_label = QLabel()
        support_label.setText(_("<b>Техническая поддержка:")+"</b><br>andrej55556@mail.ru")
        layout.addWidget(support_label)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()