import sys
import os
import json
from datetime import datetime
from PyQt5.QtWidgets import (QWidget, QApplication, QListWidget, QGridLayout)
from PyQt5.QtGui import QIcon
import resources


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(600, 500)
        self.g_layout = QGridLayout(self)
        self.list = QListWidget(self)
        self.g_layout.addWidget(self.list)
        self.setWindowTitle('JSON viewer')
        self.setWindowIcon(QIcon(':/resource/viewer.png'))

    def browse(self):
        self.list.clear()
        if not os.path.exists('saves/data.csv'):
            self.list.addItem('Отсутсвует сохранение')
        else:
            with open('saves/data.json', 'r') as file:
                data = json.load(file)
                self.lst = []
                for num, row in enumerate(data, 1):
                    row = ('{}. {:%d.%m.%Y, в %H:%M} была выполнена '
                           'операция {} с итоговым ответом {}\n').format(
                               num,
                               datetime.fromisoformat(row["datetime"]),
                               row["operation"],
                               row["result"])
                    self.list.addItem(row)
                    self.lst.append(row)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    w = Window()
    w.show()
    w.browse()
    sys.exit(app.exec_())
