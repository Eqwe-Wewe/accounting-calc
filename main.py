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
                print(f'данные с экрана: {self.lcdNumber.value()}',
                      f'{self.operand = }',
                      f'{self.operand_pass = }',
                      f'{self.oper = }',
                      f'{self.plus_minus = }',
                      f'{self.point_eq = }',
                      f'{self.p_point = }',
                      f'{self.amount_operand = }',
                      f'{self.memory_cell = }',
                      f'{self.num_eq.isEnabled() = }',
                      '\t',
                      sep='\n')
            return result
        return wrapper2
    return wrapper


class Exx(QtWidgets.QMainWindow, gui_calculator.Ui_MainWindow, DataManager):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        DataManager.__init__(self)
        self.init_var()

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
        self.num_plus_minus.pressed.connect(self.plus_to_minus)
        self.num_c.pressed.connect(self.cancel)
        self.num_ce.pressed.connect(self.cancel_ce)
        self.num_eq.pressed.connect(self.eq)
        self.num_eq.setEnabled(False)
        self.num_mc.pressed.connect(lambda: self.memory('clear'))
        self.num_mr.pressed.connect(lambda: self.memory('read'))
        self.num_m_minus.pressed.connect(lambda: self.memory('memory-'))
        self.num_m_plus.pressed.connect(lambda: self.memory('memory+'))
        self.num_procent.pressed.connect(
            lambda: self.extended_operations(
                'procent'))
        self.num_sqrt.pressed.connect(
            lambda: self.extended_operations(
                'sqrt_num'))
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
            self.cancel_ce()
        elif k == Qt.Key_Period or Qt.Key_Comma:
            self.point()
        super().keyPressEvent(event)

    def init_var(self):
        # операнд, записанный по разрядам
        self.operand = []

        # хранит хранит 2 операнда и знак операции
        self.oper = []

        # ячейка памяти
        self.memory_cell = 0

        # флаг-допуск ввода данных на экран
        self.operand_pass = False

        # флаг десятичной точки
        self.p_point = False

        # если False - знак плюс перед операндом
        self.plus_minus = False

        # флаг соверщения операции '='
        self.point_eq = False

        # целое значение операнда
        self.init_operand()

        #  доп. инфо по операциям на экране
        self.label.setText('')
        self.label_memory.setText('')

    def init_operand(self):
        self.operand = ['0']
        self.amount_operand = '0'
        self.lcdNumber.display(0)

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

        # отображение 12 значного числа, десятичного разделителя,
        # знака +/-
        if '.' in self.operand:
            self.operand = self.operand[:13]
        else:
            self.operand = self.operand[:12]

        # ввод числа
        self.amount_operand = ''.join(self.operand)
        self.lcdNumber.display(self.amount_operand)
        self.operand_pass = True
        self.label.clear()

    @service_info()
    def operation(self, value):
        self.num_eq.setEnabled(True)
        self.operation_val = value
        self.remove_sep()
        if self.operand_pass is True and (self.oper != []
                                          and self.point_eq is not True):
            self.eq()
        self.operand_pass = False
        self.oper = [self.amount_operand, self.operation_val]
        if self.oper[1] != self.operation_val:
            self.oper[1] = self.operation_val
        self.operand.clear()
        self.point_operation = True
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
            self.remove_sep()
            self.oper.append(self.amount_operand)
            self.calculation()
            self.point_eq = True
            self.point_operation = False
            self.p_point = False
            self.label.clear()

    @service_info()
    def calculation(self):
        if self.oper[1] == '+':
            self.result = str(self.float_to_int(
                Decimal(self.oper[0])
                + Decimal(self.oper[2])))
        elif self.oper[1] == '-':
            self.result = str(self.float_to_int(
                Decimal(self.oper[0])
                - Decimal(self.oper[2])))
        elif self.oper[1] == '*':
            self.result = str(self.float_to_int(
                Decimal(self.oper[0])
                * Decimal(self.oper[2])))
        try:
            if self.oper[1] == '/':
                self.result = str(self.float_to_int(
                    Decimal(self.oper[0])
                    / Decimal(self.oper[2])))
        except ZeroDivisionError:
            self.lcdNumber.display('error')
            self.history.clear()
            self.oper.clear()
            self.operand.clear()
            self.num_eq.setEnabled(False)
        else:
            self.result = '{:.12g}'.format(float(self.result))
            # ------------------------write-----------------------------
            self.insert_data.append([' '.join(self.oper),
                                     self.result,
                                     datetime.now().isoformat()])
            # ----------------------------------------------------------
            self.amount_operand = self.result
            self.lcdNumber.display(self.result)
            self.history_operations()

    def history_operations(self):
        a = '{:,.15g}'.format(self.float_to_int(self.oper[0])).replace(
            ',', ' ')
        b = str(self.oper[1])
        if len(self.oper) == 3:
            c = '{:,.15g}'.format(self.float_to_int(self.oper[2])).replace(
                ',', ' ')
            d = ' ='
            self.history.setText(' '.join([a, b, c, d]))
        else:
            self.history.setText(' '.join([a, b]))

    @service_info()
    def memory(self, argument):
        ''' операции с ячейкой памяти '''
        if argument == 'read':
            for num in list(str(self.float_to_int(self.memory_cell))):
                self.input_operand(num)
            self.operand_pass = True
            self.point_operation = False
            self.operand.clear()
        elif argument == 'memory+':
            self.memory_cell += self.lcdNumber.value()
            self.memory_cell = float('{:.12g}'.format(self.memory_cell))
        elif argument == 'memory-':
            self.memory_cell -= self.lcdNumber.value()
            self.memory_cell = float('{:.12g}'.format(self.memory_cell))
        elif argument == 'clear':
            self.memory_cell = 0
        self.label.setText(argument)

    @service_info()
    def point(self):
        ''' десятичный разделитель '''
        if self.p_point is False and len(self.operand) < 13:
            if self.point_eq is True or self.operand == []:
                self.input_operand('0')
            self.input_operand('.')
            self.p_point = True

    @service_info()
    def plus_to_minus(self):
        '''изменение знака у числа'''
        if '-' not in self.operand:
            self.operand.insert(0, '-')
        else:
            self.operand.remove('-')
        self.amount_operand = ''.join(self.operand)
        self.lcdNumber.display(self.amount_operand)

    @service_info()
    def extended_operations(self, operation):
        if operation == 'procent' and len(self.oper) > 0:
            self.num_conversion = ' '.join([str(self.lcdNumber.value()),
                                            '% из', self.oper[0]])
            self.amount_operand = (self.float_to_int(self.oper[0])
                                   / 100
                                   * float(self.amount_operand))
            self.label.setText('procent')
        elif operation == 'sqrt_num':
            self.num_conversion = ' '.join(['квадратный корень из',
                                            str(self.float_to_int(
                                                self.lcdNumber.value()))])
            self.sqrt_of_num = self.float_to_int(math.sqrt(
                self.lcdNumber.value()))
            self.amount_operand = str(self.sqrt_of_num)
            self.label.setText('sqrt')
        if ((len(self.oper) > 0 and operation == 'procent')
                or operation == 'sqrt_num'):
            self.amount_operand = '{:.12g}'.format(float(self.amount_operand))
            self.lcdNumber.display(self.amount_operand)
            self.operand.clear()
            # -------------------------write----------------------------
            self.insert_data.append([self.num_conversion,
                                     self.amount_operand,
                                     datetime.now().isoformat()])
            # ----------------------------------------------------------

    def remove_sep(self):
        '''удаление десятичного разделителя у целого числа'''
        if self.amount_operand[-1] == '.':
            self.amount_operand = self.amount_operand[:-1:]

    def float_to_int(self, result):
        '''проверка полученного числа на целочисленность'''
        if float(result).is_integer() is True:
            return int(float(result))
        return float(result)

    @service_info()
    def cancel_ce(self):
        if len(self.operand) != 0:
            element = self.operand.pop(-1)
            if element == '.':
                self.p_point = False
            self.amount_operand = ''.join(self.operand)
            self.lcdNumber.display(self.amount_operand)
            if len(self.operand) == 0 or (len(self.operand) == 1
                                          and self.operand[0] == '-'):
                self.init_operand()

        # очистка после self.eq()
        if self.point_eq is True:
            self.cancel()

    @service_info()
    def cancel(self):
        self.history.clear()
        self.init_var()
        self.num_eq.setEnabled(False)

    @service_info(0)
    def closeEvent(self, event):
        if self.insert_data != []:
            DataManager.write_data(self.insert_data)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Exx()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
