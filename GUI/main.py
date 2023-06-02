# How to convert ui files to python
# python -m PyQt6.uic.pyuic -o output.py -x input.ui

import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow)
from main_window import Ui_MainWindow
from query_window import Ui_Query
from load_window import Ui_Load
from documentation_window import Ui_Documentation

class MainWindow(QMainWindow):
  def __init__(self):
    super(MainWindow,self).__init__()
    # Main Window
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)

    # Main Window buttons to open other windows
    self.ui.make_queries.clicked.connect(self.query_window)
    self.ui.load_data.clicked.connect(self.load_window)
    self.ui.documentation.clicked.connect(self.documentation_window)

  def query_window(self):
    self.query_window = QMainWindow()
    self.ui_q = Ui_Query()
    self.ui_q.setupUi(self.query_window)
    self.show_window(self.query_window, self)
    self.ui_q.home_button.clicked.connect(lambda checked: self.show_window(self, self.query_window))
    # TO DO --> Own buttons Functions

  def load_window(self):
    self.load_window = QMainWindow()
    self.ui_l = Ui_Load()
    self.ui_l.setupUi(self.load_window)
    self.show_window(self.load_window, self)
    self.ui_l.cancel_button.clicked.connect(lambda checked: self.show_window(self, self.load_window))
    # TO DO --> Own buttons Functions

  def documentation_window(self):
    self.doc_window = QMainWindow()
    self.ui_d = Ui_Documentation()
    self.ui_d.setupUi(self.doc_window)
    self.show_window(self.doc_window, self)
    self.ui_d.home_button.clicked.connect(lambda checked: self.show_window(self, self.doc_window))
    # TO DO --> Own buttons Functions


  def show_window(self, win1, win2):
    if win1.isVisible():
        win1.hide()
        win2.show()
    else:
        win2.hide()
        win1.show()



if __name__ == "__main__":
    # Creating the app
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec()
    sys.exit(app.exec())