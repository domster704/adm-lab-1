# Практичнская работа №1: Исупов Григорий, Рид Екатерина; БПМ-22-4

import math
import sys
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtGui import QIcon


def transformArrayWithHex(array, alphabet):
    new_array = []
    current_hex_number = ''
    for index in range(len(array)):
        if array[index] in alphabet or array[index] == '.':
            current_hex_number += array[index]
        elif current_hex_number != '':
            new_array.append(current_hex_number)
            new_array.append(array[index])
            current_hex_number = ''
        else:
            new_array.append(array[index])

    if current_hex_number != '':
        new_array.append(current_hex_number)
    return new_array


class Converter(object):
    def __init__(self, base):
        self.currentBase = base
        self.alphabet = "0123456789ABCDEF"
        self.romanAlphabet = "IVXLCDMGH"
        self.isRoman = False

    def setBase(self, base):
        self.currentBase = base

    def convert_base(self, num, to_base, init_base):
        n = int(num, init_base) if isinstance(num, str) else num
        sign_coefficient = '' if n >= 0 else '-'
        n = abs(n)
        result = ""
        while n > 0:
            n, m = divmod(n, to_base)
            result += self.alphabet[m]
        return sign_coefficient + result[::-1]

    def _contains_only_alphabet_symbol(self, string):
        return any(char in self.alphabet for char in string)

    def _contains_only_roman_symbol(self, string):
        return any(char in self.romanAlphabet for char in string)

    def convert_array_of_num_to_some_base(self, array, base):
        new_array = []
        if self.isRoman:
            self.isRoman = False
            self.currentBase = 10
            local_array = []
            for el in transformArrayWithHex(array, self.romanAlphabet):
                if self._contains_only_roman_symbol(el):
                    local_array.append(str(self.convert_from_roman_to_10base(el)))
                else:
                    local_array.append(el)
            array = local_array

        if base == 'roman':
            base = 10
            self.isRoman = True

        for el in transformArrayWithHex(array, self.alphabet):
            if self._contains_only_alphabet_symbol(el):
                new_array.append(self.convert_base(el, base, self.currentBase))
            else:
                new_array.append(el)

        if self.isRoman:
            local_array = []
            for el in new_array:
                if self._contains_only_alphabet_symbol(el):
                    print(el)
                    local_array.append(self.convert_to_roman(int(el)))
            new_array = local_array[::-1]
        return new_array

    def convert_to_roman(self, number):
        romans_dict = {
            1: "I",
            5: "V",
            10: "X",
            50: "L",
            100: "C",
            500: "D",
            1000: "M",
            5000: "G",
            10000: "H"
        }
        div = 1
        while number >= div:
            div *= 10

        div /= 10

        res = ""
        while number:
            last_num = int(number / div)
            if last_num <= 3:
                res += (romans_dict[div] * last_num)
            elif last_num == 4:
                res += (romans_dict[div] +
                        romans_dict[div * 5])
            elif 5 <= last_num <= 8:
                res += (romans_dict[div * 5] +
                        (romans_dict[div] * (last_num - 5)))
            elif last_num == 9:
                res += (romans_dict[div] +
                        romans_dict[div * 10])

            number = math.floor(number % div)
            div /= 10
        return res

    def convert_from_roman_to_10base(self, string):
        def value(r):
            d = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000, "G": 5000, "H": 10000}
            if r in d:
                return d[r]
            return -1

        res = 0
        i = 0

        while i < len(string):
            s1 = value(string[i])
            if i + 1 < len(string):
                s2 = value(string[i + 1])
                if s1 >= s2:
                    res = res + s1
                    i = i + 1
                else:
                    res = res + s2 - s1
                    i = i + 2
            else:
                res = res + s1
                i = i + 1

        return res


class CalculatorUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(CalculatorUI, self).__init__()
        uic.loadUi('Calc_v5.ui', self)
        self.solution = []
        self.converter = Converter(10)

    def btnPressedEC(self, button_id):
        global per_log
        try:
            # number Pi 'π'
            if button_id == 26:
                self.lineEdit.setText(self.lineEdit.text() + "π")
                self.solution.append(str(math.pi))
            # factorial
            if button_id == 29:
                self.lineEdit.setText(self.lineEdit.text() + "!")
                self.solution = [str(math.factorial(int("".join(self.solution))))]
            # working with sin()
            if button_id == 30:
                self.lineEdit.setText(self.lineEdit.text() + "sin(")
                self.solution.append("math.sin(")
            # working with cos()
            if button_id == 25:
                self.lineEdit.setText(self.lineEdit.text() + "cos(")
                self.solution.append("math.cos(")
            # working with e
            if button_id == 27:
                self.lineEdit.setText(self.lineEdit.text() + "e")
                self.solution.append("math.e")
            # working with log₁₀
            if button_id == 28:
                self.lineEdit.setText(self.lineEdit.text() + "log")
                per_log = 1
                self.solution.append('math.log(')
        except Exception as e:
            self.statusBar.showMessage(str(e))
            self.lineEdit.setText("")
            self.solution = [""]
        print(self.solution)

    def btnPressedDC(self, button_id):
        global per, start, per_log, p, pop
        try:
            # working with digits
            if button_id in digitsIDs:
                if per_log == 1:
                    self.lineEdit.setText(self.lineEdit.text() + low_index[str(button_id)])
                    per_log = 2
                    p = button_id
                elif per_log == 2:
                    exec(f'self.lineEdit.setText(self.lineEdit.text() + self.pushButton_{button_id}.text())')
                    pop += str(button_id)
                else:
                    if set(self.lineEdit.text()) == {"0"}:
                        exec(f'self.lineEdit.setText(self.pushButton_{button_id}.text())')
                    else:
                        exec(f'self.lineEdit.setText(self.lineEdit.text() + self.pushButton_{button_id}.text())')
                    exec(f'self.solution.append(self.pushButton_{button_id}.text())')
                    # this part for working with '√'
                    if button_id == 13 and per == 1:
                        print(per)
                        start = 1
                    elif start == 1 and button_id == 14:
                        start = 0
                        per = 0
                        self.solution.append("**0.5")
                    elif per == 1 and start == 0:
                        per = 0
                        self.solution.append("**0.5")
            # working with math actions
            elif button_id in b:
                if per_log == 2:
                    self.solution.append(f'{int(pop)}, {p})')
                    per_log, pop = 0, ""
                if self.lineEdit.text()[-1] not in "+-":
                    exec(f'self.lineEdit.setText(self.lineEdit.text() + self.pushButton_{button_id}.text())')
                if button_id == 12:
                    self.solution.append("*")
                elif button_id == 16:
                    self.solution.append("/")
                else:
                    exec(f'self.solution.append(self.pushButton_{button_id}.text())')
            # working with dot('.')
            elif button_id == 23:
                self.lineEdit.setText(self.lineEdit.text() + ".")
                self.solution.append(".")
            # clear lineEdit
            elif button_id == 17:
                self.solution = [""]
            # calculating
            elif button_id == 11:
                if per_log == 2:
                    self.solution.append(f'{int(pop)}, {p})')
                    per_log, pop = 0, ""
                if self.lineEdit.text() == "":
                    pass
                else:
                    self.numSystemLabel.setText("10")
                    self.numSystemSlider.setValue(10)

                    result = str(eval("".join(self.solution)))
                    self.lineEdit.setText(result)
                    self.solution = [result]

            # deleting last element
            elif button_id == 15:
                self.lineEdit.setText(self.lineEdit.text()[0:-1])
                self.solution = self.solution[0:-1]
            # working with '√'; require changes, please, checked "working with digits"
            elif button_id == 22:
                self.lineEdit.setText(self.lineEdit.text() + "√")
                per = 1
            # working with 'x²'
            elif button_id == 19:
                self.lineEdit.setText(self.lineEdit.text() + "²")
                self.solution.append("**2")
        except Exception as e:
            self.statusBar.showMessage(str(e))
            self.lineEdit.setText("")
            self.solution = [""]
        print(self.solution)

    def btnPressedNumSystem(self, button_text):
        self.lineEdit.setText(self.lineEdit.text() + button_text)
        self.solution.append(button_text)
        print(self.solution)

    def initUI(self):
        self.setFixedSize(352, 535)
        self.setWindowTitle("Calculator")
        self.setWindowOpacity(0.98)
        self.setWindowIcon(QIcon('calc_ico.png'))
        self.action.triggered.connect(self.EC)
        self.action_2.triggered.connect(self.DC)
        self.numberSystem_action.triggered.connect(self.NumberSystemResizeWindow)
        self.NumberSystemResizeWindow()

        self.numSystemSlider.valueChanged.connect(self.changeNumSystemLabel)

        self.romanButton.clicked.connect(self.romanButtonListener)

        self.show()

    def EC(self):
        self.setFixedSize(455, 535)
        self.lineEdit.setGeometry(QtCore.QRect(0, 0, 1000, 61))

    def DC(self):
        self.setFixedSize(351, 535)
        self.lineEdit.setGeometry(QtCore.QRect(0, 0, 1000, 61))

    def NumberSystemResizeWindow(self):
        self.setFixedSize(647, 535)
        self.lineEdit.setGeometry(QtCore.QRect(0, 0, 1000, 61))

    def changeNumSystemLabel(self):
        base = self.sender().value()
        self.numSystemLabel.setText(str(base))
        self.solution = self.converter.convert_array_of_num_to_some_base(self.solution, base)

        self.converter.setBase(base)
        self.lineEdit.setText("".join(self.solution))

    def romanButtonListener(self):
        self.solution = self.converter.convert_array_of_num_to_some_base(self.solution, 'roman')
        self.lineEdit.setText("".join(self.solution))


if __name__ == "__main__":
    digitsIDs = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 13, 14)
    b = (10, 21, 12, 16, 20, 18)
    numberSystemIDS = ()
    per, start, per_log, p, pop = 0, 0, 0, 0, ""
    low_index = {
        "0": "₀",
        "1": "₁",
        "2": "₂",
        "3": "₃",
        "4": "₄",
        "5": "₅",
        "6": "₆",
        "7": "₇",
        "8": "₈",
        "9": "₉",
    }

    app = QtWidgets.QApplication(sys.argv)
    root = CalculatorUI()
    root.initUI()

    mainButtonsLayout = root.gridLayout_mainButtons
    engineerButtonsLayout = root.gridLayout_engineerButtons
    wordButtonsLayout = root.gridLayout_wordButtons

    for i in range(0, 24):
        exec(f'root.pushButton_{i}.clicked.connect(lambda checked, text=i: root.btnPressedDC(text))')

    for i in range(25, 31):
        exec(f'root.pushButton_{i}.clicked.connect(lambda checked, text=i: root.btnPressedEC(text))')

    for i in range(wordButtonsLayout.count()):
        button = wordButtonsLayout.itemAt(i).widget()
        button.clicked.connect(lambda checked, text=button.text(): root.btnPressedNumSystem(text))

    app.exec_()
    
