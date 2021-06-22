#!/usr/bin/env python

import sys
import os
import json
from datetime import datetime
from PyQt5.QtWidgets import (QWidget, QApplication, QListWidget, QVBoxLayout,
                             QPushButton)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import resources


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(600, 500)
        self.g_layout = QVBoxLayout(self)
        self.list = QListWidget(self)
        self.list.setWordWrap(True)
        self.g_layout.addWidget(self.list)
        self.setWindowTitle('JSON viewer')
        self.setWindowIcon(QIcon(':/resource/viewer.png'))
        self.refresh_button = QPushButton(self)
        self.refresh_button.setText('refresh')
        self.refresh_button.pressed.connect(self.browse)
        self.refresh_button.setMaximumWidth(170)
        self.g_layout.addWidget(self.refresh_button,
                                alignment=Qt.AlignCenter)

    def browse(self):
        self.list.clear()
        if not os.path.exists('saves/data.csv'):
            self.list.addItem('Отсутсвует сохранение')
        else:
            with open('saves/data.json', 'r', encoding='utf-8') as file:
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
