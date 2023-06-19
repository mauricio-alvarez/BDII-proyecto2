from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import pyqtSlot
import sys

class Ui_Load(QtWidgets.QMainWindow):
  def setupUi(self, MainWindow):
    MainWindow.setObjectName("MainWindow")
    MainWindow.resize(484, 269)
    self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
    self.centralwidget.setObjectName("centralwidget")
    self.files_path = QtWidgets.QLineEdit(parent=self.centralwidget)
    self.files_path.setEnabled(False)
    self.files_path.setGeometry(QtCore.QRect(50, 90, 341, 31))
    self.files_path.setReadOnly(True)
    self.files_path.setObjectName("files_path")
    self.cancel_button = QtWidgets.QPushButton(parent=self.centralwidget)
    self.cancel_button.setGeometry(QtCore.QRect(100, 180, 121, 31))
    self.cancel_button.setObjectName("cancel_button")
    self.files_button = QtWidgets.QPushButton(parent=self.centralwidget)
    self.files_button.setGeometry(QtCore.QRect(400, 100, 25, 19))
    self.files_button.setObjectName("files_button")
    self.files_button.clicked.connect(self.open_dialog)
    self.load_button = QtWidgets.QPushButton(parent=self.centralwidget)
    self.load_button.setGeometry(QtCore.QRect(250, 180, 121, 31))
    self.load_button.setObjectName("load_button")
    MainWindow.setCentralWidget(self.centralwidget)
    self.retranslateUi(MainWindow)
    QtCore.QMetaObject.connectSlotsByName(MainWindow)

  def retranslateUi(self, MainWindow):
    _translate = QtCore.QCoreApplication.translate
    MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
    self.files_path.setPlaceholderText(_translate("MainWindow", "Select Folder or File"))
    self.cancel_button.setText(_translate("MainWindow", "Cancel"))
    self.files_button.setText(_translate("MainWindow", "..."))
    self.load_button.setText(_translate("MainWindow", "Load"))

  @pyqtSlot()
  def open_dialog(self):
    fname = QtWidgets.QFileDialog.getOpenFileName(
        self,
        "Open File",
        "${HOME}",
        "All Files (*);; Python Files (*.py);; PNG Files (*.png)",
    )
    self.files_path.setText(fname[0])
        

    
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_Load()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())