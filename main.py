import sys
from ui import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableView
from PyQt5 import QtSql
from PyQt5 import QtCore
from PyQt5 import QtGui

class form(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('fieldlist.db')
        self.model = QtSql.QSqlTableModel()
        self.model.setTable('field')
        self.model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
        self.model.select()
        self.model.setHeaderData(0, QtCore.Qt.Horizontal,"AssessmentID")
        self.model.setHeaderData(1, QtCore.Qt.Horizontal,"Module Name")
        self.model.setHeaderData(2, QtCore.Qt.Horizontal, "Staff ID")
        self.model.setHeaderData(3, QtCore.Qt.Horizontal,"Module Code")
        self.model.setHeaderData(4, QtCore.Qt.Horizontal, "Submission Date")
        self.model.setHeaderData(5, QtCore.Qt.Horizontal,"Weighting")
        self.model.setHeaderData(6, QtCore.Qt.Horizontal,"Component")
        self.ui.tableWidget.setModel(self.model)
        self.ui.pushButton.clicked.connect(self.addToDb)
        self.ui.query.textChanged.connect(self.search)
        self.show()
        self.ui.pushButton_2.clicked.connect(self.updaterow)
        self.ui.pushButton_3.clicked.connect(self.delrow)
        self.i = self.model.rowCount()
        self.ui.lcdNumber.display(self.i)
        print(self.ui.tableWidget.currentIndex().row())

    def search(self):
        items = self.ui.tableWidget.findItems(
            self.ui.query.text(), QtCore.Qt.MatchExactly)
        if items:
            results = '\n'.join(
                'row %d column %d' % (item.row() + 1, item.column() + 1)
                for item in items)
        else:
            results = 'Found Nothing'
        QtGui.QMessageBox.information(self, 'Search Results', results)

    def addToDb(self):
        print(self.i)
        self.model.insertRows(self.i,1)
        self.model.setData(self.model.index(self.i,1),self.ui.lineEdit.text())
        self.model.setData(self.model.index(self.i, 2), self.ui.lineEdit_2.text())
        self.model.setData(self.model.index(self.i,3), self.ui.lineEdit_3.text())
        self.model.setData(self.model.index(self.i,4), self.ui.dateEdit.text())
        self.model.setData(self.model.index(self.i,5), self.ui.lineEdit_4.text())
        self.model.setData(self.model.index(self.i,6), self.ui.lineEdit_5.text())
        self.model.submitAll()
        self.i += 1
        self.ui.lcdNumber.display(self.i)

    def delrow(self):
        if self.ui.tableWidget.currentIndex().row() > -1:
            self.model.removeRow(self.ui.tableWidget.currentIndex().row())
            self.i -= 1
            self.model.select()
            self.ui.lcdNumber.display(self.i)
        else:
            QMessageBox.question(self,'Message', "Please select a row would you like to delete", QMessageBox.Ok)
            self.show()

    def updaterow(self):
        if self.ui.tableWidget.currentIndex().row() > -1:
            record = self.model.record(self.ui.tableWidget.currentIndex().row())
            record.setValue("Module Name",self.ui.lineEdit.text())
            record.setValue("Staff ID",self.ui.lineEdit_2.text())
            record.setValue("Module Code", self.ui.lineEdit_3.text())
            record.setValue("Submission Date", self.ui.dateEdit.text())
            record.setValue("Weighting", self.ui.lineEdit_4.text())
            record.setValue("Component", self.ui.lineEdit_5.text())
            self.model.setRecord(self.ui.tableWidget.currentIndex().row(), record)
        else:
            QMessageBox.question(self,'Message', "Please select a row would you like to update", QMessageBox.Ok)
            self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    frm = form()
    sys.exit(app.exec_())
