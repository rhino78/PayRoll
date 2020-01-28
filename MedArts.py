import DatabaseHelpers
from os import path
import sys
from PyQt5 import Qt, QtSql, QtWidgets, QtCore
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QAction, qApp, QTableWidgetItem, QHBoxLayout, QVBoxLayout

list1 = ['one', 'two', 'three']


class MedArts(Qt.QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = loadUi("MainFrm.ui", self)  # load the ui as html
        quit_action = QAction("Exit", self)
        create_action = QAction("Create New Employee", self)
        payroll_action = QAction("Enter PayRoll", self)

        menubar = self.menuBar()
        quit_action.triggered.connect(qApp.quit)
        create_action.triggered.connect(self.create_new)
        payroll_action.triggered.connect(self.create_payroll)

        # self.saveButton.clicked.connect(self.save_to_db)

        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(create_action)
        fileMenu.addAction(payroll_action)
        fileMenu.addAction(quit_action)

        db = Qt.QSqlDatabase.addDatabase("QSQLITE")
        # need to check for a db, if not, lets create one
        if not path.exists("Employees.db"):
            DatabaseHelpers.init_datbase()




    def save_to_db(self):
        colCount = self.tableWidget.columnCount()
        rowCount = self.tableWidget.rowCount()
        for row in range(rowCount):
            pay = []
            for col in range(colCount):
                item = self.tableWidget.item(row, col)
                if item is not None:
                    pay.append(item.text())
            # loop through all the rows and update / insert into the db
            if len(pay) > 0 and self.in_db(row):
                DatabaseHelpers.update(pay, row)
            elif len(pay) > 0:
                DatabaseHelpers.insert(pay, active_emp_id, row)


    def in_db(self, value):
        return DatabaseHelpers.in_db(value, active_emp_id)

    def eventFilter(self, event):
        if event.type() == QtCore.QEvent.ActivationChange:
            self.init_combo()




    def create_payroll(self):
        self.payroll_form = PayrollForm()
        self.payroll_form.show()

    def create_new(self):
        self.create_form = CreateForm()
        self.create_form.show()


class PayrollForm(Qt.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = loadUi("PayrollFrm.ui", self)  # load the ui as html
        self.closeButton.clicked.connect(self.close)
        self.saveButton.clicked.connect(self.save_to_db)
        self.prevButton.clicked.connect(self.prev)
        self.nextButton.clicked.connect(self.next)
        self.comboBox.currentIndexChanged.connect(self.on_combo_change)
        self.init_combo()

    def prev(self):
        print('previous')
        active_rec =- 1
        print(active_rec)


    def next(self):
        print('next')
        # working ok, but won't increment multiple times
        active_rec =+ 1
        print(active_rec)
        pay = DatabaseHelpers.selectemp(active_emp_id)
        if len(pay) > 0:
            self.date.setText(pay[active_rec][0])
            self.hours.setText(str(pay[active_rec][1]))
            self.gross.setText(str(pay[active_rec][2]))
            self.withholding.setText(str(pay[active_rec][3]))
            self.socialsecurity.setText(str(pay[active_rec][4]))
            self.ira.setText(str(pay[active_rec][5]))
            self.notes.setText(str(pay[active_rec][6]))

    def save_to_db(self):
        DatabaseHelpers.insert_emp(self)

    def init_combo(self):
        self.comboBox.clear()
        emplist = DatabaseHelpers.emp_list()
        for row in emplist:
            self.comboBox.addItem('{0} | {1} | {2} | {3} | {4}'.format(row[0], row[1], row[2], row[3], row[4]))

    def on_combo_change(self, value):
        # we can use the value as an index
        global active_emp_id
        active_emp_id = value
        global active_rec
        active_rec = 0
        self.date.clear()
        self.hours.clear()
        self.gross.clear()
        self.withholding.clear()
        self.socialsecurity.clear()
        self.ira.clear()
        self.notes.clear()

        pay = DatabaseHelpers.selectemp(active_emp_id)
        self.label_8.setText("there are {0} records to display".format(len(pay)))
        # hardcoding to the first row - still need to implement the paging feature
        if len(pay) > 0:
            self.date.setText(pay[active_rec][0])
            self.hours.setText(str(pay[active_rec][1]))
            self.gross.setText(str(pay[active_rec][2]))
            self.withholding.setText(str(pay[active_rec][3]))
            self.socialsecurity.setText(str(pay[active_rec][4]))
            self.ira.setText(str(pay[active_rec][5]))
            self.notes.setText(str(pay[active_rec][6]))


class CreateForm(Qt.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = loadUi("CreateFrm.ui", self)  # load the ui as html
        self.closeButton.clicked.connect(self.close)
        self.saveButton.clicked.connect(self.save_to_db)

    def save_to_db(self):
        DatabaseHelpers.insert_emp(self)


app = Qt.QApplication(sys.argv)
MainFrm = MedArts()
MainFrm.show()

app.exec_()
