#!/usr/bin/env python

import sys
import os
from datetime import datetime
import csv
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QApplication, QTableWidget,
                             QTableWidgetItem, QHeaderView, QLabel,
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
        self.v_layout = QVBoxLayout(self)
        self.table = QTableWidget(self)
        self.v_layout.addWidget(self.table)
        self.setWindowTitle('CSV viewer')
        self.setWindowIcon(QIcon(':/resource/viewer.png'))
        self.open_file()
        self.refresh_button = QPushButton(self)
        self.refresh_button.setText('refresh')
        self.refresh_button.pressed.connect(self.refresh)
        self.refresh_button.setMaximumWidth(170)
        self.v_layout.addWidget(
            self.refresh_button,
            alignment=Qt.AlignCenter
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setDefaultSectionSize(120)
        self.table.horizontalHeader().setSectionResizeMode(
            2,
            QHeaderView.Fixed
        )

    def open_file(self):
        if not os.path.exists('saves/data.csv'):
            self.label = QLabel(self)
            self.label.setText('Отсутствуют сохранения')
            self.g_layout.addWidget(self.label)
        else:
            with open('saves/data.csv', encoding='utf-8') as file:
                reader = csv.reader(file, delimiter=';')
                for num, row in enumerate(reader, -1):
                    self.table.insertRow(num)
                    if num == -1:
                        self.table.setColumnCount(len(row))
                        self.table.setHorizontalHeaderLabels(row)
                    else:
                        for col in row:
                            self.table.setItem(
                                num,
                                0,
                                QTableWidgetItem(row[0])
                            )
                            self.table.setItem(
                                num,
                                1,
                                QTableWidgetItem(row[1])
                            )
                            self.table.setItem(
                                num,
                                2,
                                QTableWidgetItem(
                                    '{:%H:%M:%S, %d.%m.%Y}'.format(
                                        datetime.fromisoformat(row[2])
                                    )
                                )
                            )

    def refresh(self):
        for row in range(self.table.rowCount()):
            self.table.removeRow(0)
        self.open_file()


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = Window()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
