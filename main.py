import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QTableWidgetItem
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow


class DBCoffee(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect('coffee.db')
        self.showAll_b.clicked.connect(self.showAllCoffe)

    def showAllCoffe(self):
        cur = self.con.cursor()
        result = cur.execute(
            '''Select name, stepen, type, cost, val from coffe WHERE id BETWEEN 0 AND 1001''').fetchall()
        self.tableWidget.setRowCount(len(result) + 1)
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setItem(0, 0, QTableWidgetItem('Название'))
        self.tableWidget.setItem(0, 1, QTableWidgetItem('Степень обжарки'))
        self.tableWidget.setItem(0, 2, QTableWidgetItem('Молотый/Зерновой'))
        self.tableWidget.setItem(0, 3, QTableWidgetItem('Цена'))
        self.tableWidget.setItem(0, 4, QTableWidgetItem('Объём'))

        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i + 1, j, QTableWidgetItem(str(val).capitalize()))
        self.tableWidget.resizeColumnsToContents()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DBCoffee()
    ex.show()
    sys.exit(app.exec())