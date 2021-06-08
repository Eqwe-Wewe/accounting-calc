import sys
import os
from datetime import datetime
import csv
from PyQt5.QtWidgets import (QWidget, QGridLayout, QApplication, QTableWidget,
                             QTableWidgetItem, QHeaderView, QLabel)
from PyQt5.QtGui import QIcon
import resources


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(600, 500)
        self.g_layout = QGridLayout(self)
        self.table = QTableWidget(self)
        self.g_layout.addWidget(self.table)
        self.setWindowTitle('CSV viewer')
        self.setWindowIcon(QIcon(':/resource/viewer.png'))
        self.open_file()
        if self.file:
            # self.table.setSortingEnabled(True)
            self.table.horizontalHeader().setSectionResizeMode(
                QHeaderView.Stretch)
            self.table.horizontalHeader().setDefaultSectionSize(120)
            self.table.horizontalHeader().setSectionResizeMode(
                2, QHeaderView.Fixed)

    def open_file(self):
        if not os.path.exists('saves/data.csv'):
            # raise FileNotFoundError('Отсутствуют сохранения')
            self.label = QLabel(self)
            self.label.setText('Отсутствуют сохранения')
            self.g_layout.addWidget(self.label)
            self.file = False
        else:
            self.file = True
            with open('saves/data.csv') as file:
                reader = csv.reader(file, delimiter=';')
                for num, row in enumerate(reader, -1):
                    self.table.insertRow(num)
                    if num == -1:
                        self.table.setColumnCount(len(row))
                        self.table.setHorizontalHeaderLabels(row)
                    else:
                        for col in row:
                            self.table.setItem(
                                num, 0, QTableWidgetItem(row[0]))
                            self.table.setItem(
                                num, 1, QTableWidgetItem(row[1]))
                            self.table.setItem(
                                num, 2, QTableWidgetItem(
                                    '{:%H:%M:%S, %d.%m.%Y}'.format(
                                        datetime.fromisoformat(row[2]))))


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = Window()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
