import sys
from data_manager import DataBaseQuery
from config import config
from PyQt5.QtWidgets import (QWidget, QApplication, QListWidget, QSpinBox,
                             QGridLayout, QLabel, QPushButton)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import resources


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(600, 500)
        self.g_layout = QGridLayout(self)
        self.label = QLabel(self)
        self.label.setLayoutDirection(Qt.LeftToRight)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText('of')
        self.spin = QSpinBox(self)
        self.spin.setMinimum(1)
        self.g_layout.addWidget(self.label, 1, 1, 1, 1)
        self.button = QPushButton(self)
        self.button.setText('show')
        self.button.pressed.connect(self.request)
        self.g_layout.addWidget(self.button, 1, 4, 1, 1)
        self.g_layout.addWidget(self.spin, 1, 0, 1, 1)
        self.list = QListWidget(self)
        self.list.setWordWrap(True)
        self.g_layout.addWidget(self.list, 0, 0, 1, 5)
        self.spin2 = QSpinBox(self)
        self.spin2.setMinimum(1)
        self.g_layout.addWidget(self.spin2, 1, 2, 1, 1)
        self.label_2 = QLabel(self)
        self.label_2.setAlignment(Qt.AlignCenter)
        self.label_2.setText('total')
        self.g_layout.addWidget(self.label_2, 1, 3, 1, 1)
        self.setWindowTitle('Request from the database')
        self.setWindowIcon(QIcon(':/resource/viewer.png'))
        self.init_request()

    def keyPressEvent(self, event):
        k = event.key()
        if k == Qt.Key_Enter or Qt.Key_Return:
            self.request()
        super().keyPressEvent(event)

    def init_request(self):
        '''задает диапазон значений для просмотра'''
        try:
            with DataBaseQuery(config) as cursor:
                operation = """SELECT count(*) FROM calculator"""
                cursor.execute(operation)
        except AttributeError as err:
            print(f'mysql_viewer Error: {err}')
        else:
            file = cursor.fetchone()
            self.max_len(*file)

    def request(self):
        from_val = self.spin.value() - 1
        to_val = self.spin2.value() - (self.spin.value() - 1)
        if self.spin.value() > self.spin2.value():
            self.list.clear()
            self.list.addItem(
                'The value of "from" is greater than the value of "to".')
        else:
            try:
                with DataBaseQuery(config) as cursor:
                    operation = f"""SELECT * FROM calculator ORDER BY id LIMIT
                                {from_val},{to_val}; SELECT count(*)
                                FROM calculator"""
                    files = [result.fetchall() for result in cursor.execute(
                        operation, multi=True)]
            except AttributeError as err:
                print(f'mysql_viewer Error: {err}')
            else:
                self.file = files[0]
                self.max_len(files[1][0][0])
                self.browse()

    def max_len(self, val):
        self.max_length = val
        self.spin.setMaximum(self.max_length)
        self.spin2.setMaximum(self.max_length)
        self.label_2.setText(f'total {self.max_length}')

    def browse(self):
        self.list.clear()
        for i in range(self.spin2.value() - self.spin.value() + 1):
            i = (f"Операция [{self.file[i][1]}] под № {self.file[i][0]}",
                 f" c результатом {self.file[i][2]} была выполнена ",
                 f"{self.file[i][3]:%d.%m.%Y в %H:%M:%S} \n")
            self.list.addItem(i)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    w = Window()
    w.show()
    sys.exit(app.exec_())
