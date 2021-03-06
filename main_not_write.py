#!/usr/bin/env python

import sys
from decimal import Decimal
import math
from datetime import datetime
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import gui_calculator
import resources
from data_manager import DataManager


def service_info(enable=0):
    def wrapper(method):
        def wrapper2(self, *args, **kwargs):
            result = method(self, *args, **kwargs)
            if enable == 1:
                print(
                    f'данные с экрана: {self.lcdNumber.value()}'
                    f'{self.operand = }'
                    f'{self.operand_pass = }'
                    f'{self.oper = }'
                    f'{self.point_eq = }'
                    f'{self.p_point = }'
                    f'{self.amount_operand = }'
                    f'{self.memory_cell = }'
                    f'{self.num_eq.isEnabled() = }',
                    '\t',
                    sep='\n'
                )
            return result
        return wrapper2
    return wrapper


class Exx(QtWidgets.QMainWindow, gui_calculator.Ui_MainWindow, DataManager):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        DataManager.__init__(self)
        self.init_var()

        # ячейка памяти
        self.memory_cell = 0

        # отображение чисел после нажатия кнопки
        self.num_0.pressed.connect(lambda: self.input_operand('0'))
        self.num_1.pressed.connect(lambda: self.input_operand('1'))
        self.num_2.pressed.connect(lambda: self.input_operand('2'))
        self.num_3.pressed.connect(lambda: self.input_operand('3'))
        self.num_4.pressed.connect(lambda: self.input_operand('4'))
        self.num_5.pressed.connect(lambda: self.input_operand('5'))
        self.num_6.pressed.connect(lambda: self.input_operand('6'))
        self.num_7.pressed.connect(lambda: self.input_operand('7'))
        self.num_8.pressed.connect(lambda: self.input_operand('8'))
        self.num_9.pressed.connect(lambda: self.input_operand('9'))

        # операции
        self.num_plus.pressed.connect(lambda: self.operation('+'))
        self.num_minus.pressed.connect(lambda: self.operation('-'))
        self.num_division.pressed.connect(lambda: self.operation('/'))
        self.num_mult.pressed.connect(lambda: self.operation('*'))
        self.num_point.pressed.connect(self.point)
        self.num_plus_minus.pressed.connect(self.sign_change)
        self.num_c.pressed.connect(self.clear_all)
        self.num_ce.pressed.connect(self.clear_entry)
        self.num_backspace.pressed.connect(self.backspace)
        self.num_eq.pressed.connect(self.eq)
        self.num_eq.setEnabled(False)
        self.num_mc.pressed.connect(self.memory_clear)
        self.num_mr.pressed.connect(self.memory_read)
        self.num_m_minus.pressed.connect(
            lambda: self.memory_add_sub('memory-')
        )
        self.num_m_plus.pressed.connect(
            lambda: self.memory_add_sub('memory+')
        )
        self.num_procent.pressed.connect(
            lambda: self.extended_operations('procent')
        )
        self.num_sqrt.pressed.connect(
            lambda: self.extended_operations('sqrt_num')
        )
        self.setWindowIcon(QIcon(':/resource/calculator.ico'))

    def keyPressEvent(self, event):
        k = event.key()
        if Qt.Key_1 <= k <= Qt.Key_9:
            self.input_operand(event.text())
        elif k == Qt.Key_0:
            self.input_operand('0')
        elif k == Qt.Key_Asterisk:
            self.operation('*')
        elif k == Qt.Key_Plus:
            self.operation('+')
        elif k == Qt.Key_Minus:
            self.operation('-')
        elif k == Qt.Key_Slash:
            self.operation('/')
        elif k == Qt.Key_Enter:
            if self.num_eq.isEnabled() is True:
                self.eq()
        elif k == Qt.Key_Percent:
            pass
        elif k == Qt.Key_Backspace:
            self.backspace()
        elif k == Qt.Key_Period or Qt.Key_Comma:
            self.point()
        super().keyPressEvent(event)

    def init_var(self):

        # хранит хранит 2 операнда и знак операции
        self.oper = []

        # флаг ввода данных на экран
        self.operand_pass = False

        # флаг десятичной точки
        self.p_point = False

        # флаг соверщения операции '='
        self.point_eq = False

        self.init_operand(0)

    def init_operand(self, val):

        # операнд, записанный по разрядам
        self.operand = ['0']

        self.amount_operand = '0'
        self.lcdNumber.display(val)

    @service_info()
    def input_operand(self, num):

        # ввод нового выражения после self.eq
        if self.point_eq is True:
            self.operand.clear()
            self.oper.clear()
            self.point_eq = False
            self.history.clear()
            self.num_eq.setEnabled(False)

        # предотвращение ввода одних нулей
        if self.operand == ['0'] and num != '.':
            self.operand.pop()

        self.operand.append(num)

        # отображение 12-ти значного числа, десятичного разделителя,
        # знака +/-
        if self.p_point is True or '-' in self.operand:
            self.operand = self.operand[:13]
        else:
            self.operand = self.operand[:12]

        # ввод числа
        self.amount_operand = ''.join(self.operand)
        self.lcdNumber.display(self.amount_operand)
        self.operand_pass = True

    @service_info()
    def operation(self, value):
        self.num_eq.setEnabled(True)
        self.operation_val = value
        self.remove_point()
        if self.operand_pass is True and (
            self.oper != [] and self.point_eq is False
        ):
            self.eq()
        self.operand_pass = False
        self.oper = [self.amount_operand, self.operation_val]
        if self.oper[1] != self.operation_val:
            self.oper[1] = self.operation_val
        self.operand.clear()
        self.point_eq = False
        self.history_operations()
        self.p_point = False

    @service_info()
    def eq(self):

        # унарная операция
        if self.point_eq is True:
            self.oper[0] = self.amount_operand
            self.calculation()

        # бинарная операция
        else:
            self.remove_point()
            self.oper.append(self.amount_operand)
            self.calculation()
            self.point_eq = True
            self.p_point = False

    @service_info()
    def calculation(self):
        error = False
        if self.oper[1] == '+':
            self.amount_operand = str(
                self.float_to_int(
                    Decimal(self.oper[0])
                    + Decimal(self.oper[2])
                )
            )
        elif self.oper[1] == '-':
            self.amount_operand = str(
                self.float_to_int(
                    Decimal(self.oper[0])
                    - Decimal(self.oper[2])
                )
            )
        elif self.oper[1] == '*':
            self.amount_operand = str(
                self.float_to_int(
                    Decimal(self.oper[0])
                    * Decimal(self.oper[2])
                )
            )
        elif self.oper[1] == '/':
            try:
                self.amount_operand = str(
                    self.float_to_int(
                        Decimal(self.oper[0])
                        / Decimal(self.oper[2])
                    )
                )
            except ZeroDivisionError:
                self.init_operand('Error')
                self.history.clear()
                self.num_eq.setEnabled(False)
                error = True
        if not error:
            self.operand.clear()
            self.amount_operand = self.exp_num_reduction(self.amount_operand)
            self.lcdNumber.display(self.amount_operand)
            self.history_operations()

    def history_operations(self):
        a = '{:,.12g}'.format(float(self.oper[0])).replace(',', ' ')
        b = str(self.oper[1])
        if len(self.oper) == 3:
            c = '{:,.12g}'.format(float(self.oper[2])).replace(',', ' ')
            d = ' ='
            self.history.setText(' '.join([a, b, c, d]))
        else:
            self.history.setText(' '.join([a, b]))

    @service_info()
    def memory_read(self):
        self.operand.clear()
        for num in list(str(self.float_to_int(self.memory_cell))):
            self.input_operand(num)
        self.operand.clear()

    def memory_clear(self):
        self.memory_cell = 0
        self.label.clear()

    def memory_add_sub(self, argument):
        if argument == 'memory+':
            self.memory_cell += self.lcdNumber.value()
        elif argument == 'memory-':
            self.memory_cell -= self.lcdNumber.value()
        self.memory_cell = self.float_to_int(
            '{:.12g}'.format(self.memory_cell)
        )
        self.operand.clear()
        if self.memory_cell != 0:
            self.label.setText('M')
        else:
            self.label.clear()

    @service_info()
    def point(self):
        ''' десятичный разделитель '''
        if self.p_point is False and len(self.operand) < 12:
            if self.point_eq is True:
                self.input_operand('0')
            self.input_operand('.')
            self.p_point = True

    @service_info()
    def sign_change(self):
        '''изменение знака у числа'''
        if self.operand != ['0'] and len(self.operand) > 0:
            if '-' not in self.operand:
                self.operand.insert(0, '-')
            else:
                self.operand.remove('-')
        self.amount_operand = str(-self.float_to_int(self.amount_operand))
        self.lcdNumber.display(self.amount_operand)

    @service_info()
    def extended_operations(self, operation):
        error = False
        if operation == 'procent' and len(self.oper) > 0:
            self.amount_operand = str(
                self.float_to_int(
                    float(self.oper[0])
                    / 100
                    * float(self.amount_operand)
                )
            )
        elif operation == 'sqrt_num':
            try:
                self.amount_operand = str(
                    self.float_to_int(
                        math.sqrt(
                            self.lcdNumber.value())
                    )
                )
            except ValueError:
                error = True
                self.init_operand('Error')
        if operation == 'procent' or (
            operation == 'sqrt_num' and error is False
        ):
            self.amount_operand = self.exp_num_reduction(self.amount_operand)
            self.lcdNumber.display(self.amount_operand)
            self.operand.clear()

    def remove_point(self):
        '''удаление десятичного разделителя у целого числа'''
        if self.amount_operand[-1] == '.':
            self.amount_operand = self.amount_operand[:-1:]

    def exp_num_reduction(self, num):
        '''сокращение экспоненциальной формы числа для его
        полного отображения на дисплее'''
        if len(num) > 13:
            return '{:.8g}'.format(self.float_to_int(num))
        return num

    def float_to_int(self, result):
        '''проверка полученного числа на целочисленность'''
        if float(result).is_integer() is True:
            return int(float(result))
        return float(result)

    @service_info()
    def backspace(self):
        if len(self.operand) != 0 and self.point_eq is False:
            element = self.operand.pop(-1)
            if element == '.':
                self.p_point = False
            self.amount_operand = ''.join(self.operand)
            self.lcdNumber.display(self.amount_operand)
            if len(self.operand) == 0 or (
                len(self.operand) == 1 and self.operand[0] == '-'
            ):
                self.init_operand(0)

    def clear_entry(self):
        self.init_operand(0)

    @service_info()
    def clear_all(self):
        self.history.clear()
        self.init_var()
        self.num_eq.setEnabled(False)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Exx()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
