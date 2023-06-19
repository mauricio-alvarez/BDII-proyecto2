# How to convert ui files to python
# python -m PyQt6.uic.pyuic -o output.py -x input.ui

from PyQt6.QtWidgets import (QApplication, QMainWindow)
from main_window import Ui_MainWindow
from query_window import Ui_Query
from load_window import Ui_Load
from documentation_window import Ui_Documentation
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from postrgresIndex import Postgre
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from spimi import Spimi
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from recoveryData import Recovery

class MainWindow(QMainWindow):
  def __init__(self):
    super(MainWindow,self).__init__()
    # Main Window
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)
    # Postgres and Spimi Index
    self.postgres = Postgre()
    self.spimi = Spimi()
    # Main Window buttons to open other windows
    self.ui.make_queries.clicked.connect(self.query_window)
    self.ui.load_data.clicked.connect(self.load_window)
    self.ui.documentation.clicked.connect(self.documentation_window)

  def query_window(self):
    self.spimi.dictWord = self.spimi.loadDict("dictWord.txt","texto")
    self.spimi.dictDoc = self.spimi.loadDict("dictDocs.txt","texto")
    
    self.query_window = QMainWindow()
    self.ui_q = Ui_Query()
    self.ui_q.setupUi(self.query_window)
    self.show_window(self.query_window, self)
    self.ui_q.home_button.clicked.connect(lambda checked: self.show_window(self, self.query_window))
    # TO DO --> Own buttons Functions
    self.ui_q.search_button.clicked.connect(self.searchQuery)

  def load_window(self):
    self.load_window = QMainWindow()
    self.ui_l = Ui_Load()
    self.ui_l.setupUi(self.load_window)
    self.show_window(self.load_window, self)
    self.ui_l.cancel_button.clicked.connect(lambda checked: self.show_window(self, self.load_window))
    # TO DO --> Own buttons Functions
    self.ui_l.load_button.clicked.connect(self.load)

  def documentation_window(self):
    self.doc_window = QMainWindow()
    self.ui_d = Ui_Documentation()
    self.ui_d.setupUi(self.doc_window)
    self.show_window(self.doc_window, self)
    self.ui_d.home_button.clicked.connect(lambda checked: self.show_window(self, self.doc_window))
    # TO DO --> Own buttons Functions

  def searchQuery(self):
    if self.ui_q.top_k.text() != "" and self.ui_q.query.toPlainText() != "":
      self.clearLayout(self.ui_q.postgres_layout)
      self.clearLayout(self.ui_q.python_layout)
      print("Query: " + self.ui_q.query.toPlainText() + "\n" + "with Top K: " + self.ui_q.top_k.text())
      query = self.postgres.process_text(self.ui_q.query.toPlainText())
      query_spimi = Recovery(self.ui_q.query.toPlainText(),self.spimi.dictWord,self.spimi.dictDoc)
      
      try:
        result_sql, time_sql = self.postgres.consultQuery(query,self.ui_q.top_k.text())
      except:
        result_sql = ["No se encontraron resultados"]
        time_sql = 0
      
      try:
        result_spimi, time_index = query_spimi.Recovery_data(self.ui_q.top_k.text())
      except ValueError:
        result_spimi = ["No se encontraron resultados"]
        time_index = 0

      self.ui_q.addElementsSQL(result_sql)
      self.ui_q.addElementSPIMI(result_spimi)

      self.ui_q.postgre_time.setText("Tiempo de ejecución: " + str(time_sql) + " ms")
      self.ui_q.python_time.setText("Tiempo de ejecución: " + str(time_index) + " ms")
      
    else:
      self.ui_q.query.setPlaceholderText("FIRST YOU NEED TO Write your Query here AND THEN SELECT A TOP K....")

  def load(self):
    # Set up Spimi
    dictWords = {}
    dictDocs = {}
    self.spimi.dictWord = self.spimi.loadDict("dictWord.txt","texto")
    self.spimi.dictDoc = self.spimi.loadDict("dictDocs.txt","texto")
    if self.ui_l.files_path.text() != "":
      self.spimi.indexNewDocuments(self.ui_l.files_path.text())    
      self.spimi.saveDict(self.spimi.dictWord, "dictWord.txt","texto")
      self.spimi.saveDict(self.spimi.dictDoc, "dictDocs.txt","texto")
    
    # Set up Postgres
    if not self.postgres.isFull():
      self.postgres.loadData(self.ui_l.files_path.text())
      self.postgres.createIndex(['title', 'abstract'])

  def clearLayout(self, layout):
    while layout.count():
      child = layout.takeAt(0)
      if child.widget():
        child.widget().deleteLater()

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