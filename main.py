import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QTableWidgetItem, QPushButton, QSpinBox
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow


class addEditCoffeeFormClass(QMainWindow):
    def __init__(self, main=None, edit=False):
        super().__init__(main)
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.con = sqlite3.connect('coffee.db')
        self.add.clicked.connect(self.add_m)
        self.update_.clicked.connect(self.update_m)
        if edit:
            self.choseID()
    def add_m(self):
        error_find = False
        name = self.name.text()
        step = self.step.text()
        mol_zern = self.mol_zern.text()
        descr = self.descr.toPlainText()
        val = self.val.text()
        cost = self.cost.text()
        self.errors.setText('')
        if name == '':
            error_find = True
            self.errors.setText(self.errors.toPlainText() + '\nError: Название - пустая строка')
        if not step.isdigit():
            error_find = True
            self.errors.setText(self.errors.toPlainText() + '\nError: Степень обжарки не числовое значение')
        if not cost.isdigit():
            error_find = True
            self.errors.setText(self.errors.toPlainText() + '\nError: Цена не числовое значение')
        if not val.isdigit():
            error_find = True
            self.errors.setText(self.errors.toPlainText() + '\nError: Объём не числовое значение')
        if cost == '':
            error_find = True
            self.errors.setText(self.errors.toPlainText() + '\nError: Цена - пустая строка')
        if val == '':
            error_find = True
            self.errors.setText(self.errors.toPlainText() + '\nError: Объём - пустая строка')
        if error_find:
            return -1
        cur = self.con.cursor()
        cur.execute('INSERT INTO coffe(name, stepen, type, descrip, cost, val) VALUES(?, ?, ?, ?, ?, ?)',
                    (name, step, mol_zern, descr, val, cost))
        self.con.commit()
        # добавляет в базу данных новый кофе с автоинкрементным ID
        self.close()

    def update_m(self):
        error_find = False
        name = self.name.text()
        step = self.step.text()
        mol_zern = self.mol_zern.text()
        descr = self.descr.toPlainText()
        val = self.val.text()
        cost = self.cost.text()
        self.errors.setText('')
        if name == '':
            error_find = True
            self.errors.setText(self.errors.toPlainText() + '\nError: Название - пустая строка')
        if not step.isdigit():
            error_find = True
            self.errors.setText(self.errors.toPlainText() + '\nError: Степень обжарки не числовое значение')
        if not cost.isdigit():
            error_find = True
            self.errors.setText(self.errors.toPlainText() + '\nError: Цена не числовое значение')
        if not val.isdigit():
            error_find = True
            self.errors.setText(self.errors.toPlainText() + '\nError: Объём не числовое значение')
        if cost == '':
            error_find = True
            self.errors.setText(self.errors.toPlainText() + '\nError: Цена - пустая строка')
        if val == '':
            error_find = True
            self.errors.setText(self.errors.toPlainText() + '\nError: Объём - пустая строка')
        if error_find:
            return -1
        cur = self.con.cursor()
        cur.execute('''UPDATE coffe
                SET name = ?
                WHERE id = ?''', (name, int(self.id_l.text())))
        cur.execute('''UPDATE coffe
                        SET stepen = ?
                        WHERE id = ?''', (step, int(self.id_l.text())))
        cur.execute('''UPDATE coffe
                SET type = ?
                WHERE id = ?''', (mol_zern, int(self.id_l.text())))
        cur.execute('''UPDATE coffe
                        SET descrip = ?
                        WHERE id = ?''', (descr, int(self.id_l.text())))
        cur.execute('''UPDATE coffe
                        SET cost = ?
                        WHERE id = ?''', (cost, int(self.id_l.text())))
        cur.execute('''UPDATE coffe
                        SET val = ?
                        WHERE id = ?''', (val, int(self.id_l.text())))
        self.con.commit()
        self.close()

    def choseID(self):
        cur = self.con.cursor()
        maxx = sorted(cur.execute(
            '''Select id from coffe WHERE id BETWEEN 0 AND 1001''').fetchall(), key=lambda u: u[0])[-1][-1]
        win = ChooseID(self, maxx)
        win.show()
        self.add.setEnabled(False)
        self.update_.setEnabled(True)

    def editFormSet(self, id):
        cur = self.con.cursor()
        res = cur.execute(
            '''Select * from coffe WHERE id = ?''', (id,)).fetchall()[0]
        self.id_l.setText(str(id))
        self.name.setText(res[1])
        self.step.setText(str(res[2]))
        self.mol_zern.setText(res[3])
        self.descr.setText(res[4])
        self.val.setText(str(res[5]))
        self.cost.setText(str(res[6]))


class DBCoffee(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect('coffee.db')
        self.showAll_b.clicked.connect(self.showAllCoffe)
        self.add_b.clicked.connect(self.addCofee)
        self.edit_b.clicked.connect(self.editCofee)

    def editCofee(self):
        win = addEditCoffeeFormClass(self, True)
        win.show()

    def addCofee(self):
        win = addEditCoffeeFormClass(self)
        win.show()

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
        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i + 1, j, QTableWidgetItem(str(val).capitalize()))
        self.tableWidget.resizeColumnsToContents()



class ChooseID(QMainWindow):
    def __init__(self, main=None, maxx=1):
        super().__init__(main)
        self.id_ = 1
        self.main = main
        self.initUI(maxx)

    def initUI(self, maxx):
        self.setGeometry(300, 300, 415, 400)  # окно
        self.setWindowTitle('Форма выбора')

        self.new_game_b = QPushButton('Выбрать', self)  # кнопка заказа
        self.new_game_b.resize(self.new_game_b.sizeHint())
        self.new_game_b.move(150, 165)
        self.new_game_b.clicked.connect(self.take_order)

        self.id = QSpinBox(self)
        self.id.resize(self.new_game_b.sizeHint())
        self.id.move(150, 200)
        self.id.setMaximum(maxx)
        self.id.setMinimum(1)

    def take_order(self):
        self.main.editFormSet(self.id.value())
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DBCoffee()
    ex.show()
    sys.exit(app.exec())