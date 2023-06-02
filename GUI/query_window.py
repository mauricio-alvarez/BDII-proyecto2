# Form implementation generated from reading ui file 'query_window.ui'
#
# Created by: PyQt6 UI code generator 6.5.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Query(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1401, 780)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.background = QtWidgets.QLabel(parent=self.centralwidget)
        self.background.setGeometry(QtCore.QRect(0, -10, 1401, 771))
        self.background.setText("")
        #self.background.setPixmap(QtGui.QPixmap("images/bg_query_window.png"))
        #self.background.setScaledContents(True)
        self.background.setObjectName("background")
        self.query_title = QtWidgets.QLabel(parent=self.centralwidget)
        self.query_title.setGeometry(QtCore.QRect(20, 10, 241, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.query_title.setFont(font)
        self.query_title.setObjectName("query_title")
        self.query = QtWidgets.QPlainTextEdit(parent=self.centralwidget)
        self.query.setGeometry(QtCore.QRect(20, 40, 1001, 131))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.query.setFont(font)
        self.query.setBackgroundVisible(False)
        self.query.setCenterOnScroll(False)
        self.query.setObjectName("query")
        self.top_k = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.top_k.setGeometry(QtCore.QRect(1060, 50, 113, 20))
        self.top_k.setObjectName("top_k")
        self.search_button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.search_button.setGeometry(QtCore.QRect(1200, 50, 61, 41))
        self.search_button.setObjectName("search_button")
        self.home_button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.home_button.setGeometry(QtCore.QRect(1350, 700, 51, 41))
        self.home_button.setObjectName("home_button")
        self.verticalLayoutWidget = QtWidgets.QWidget(parent=self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(39, 249, 641, 421))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.python_layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.python_layout.setContentsMargins(0, 0, 0, 0)
        self.python_layout.setObjectName("python_layout")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(parent=self.centralwidget)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(710, 250, 641, 421))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.postgres_layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.postgres_layout.setContentsMargins(0, 0, 0, 0)
        self.postgres_layout.setObjectName("postgres_layout")
        self.postgres_title = QtWidgets.QLabel(parent=self.centralwidget)
        self.postgres_title.setGeometry(QtCore.QRect(710, 210, 261, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.postgres_title.setFont(font)
        self.postgres_title.setObjectName("postgres_title")
        self.python_time = QtWidgets.QLabel(parent=self.centralwidget)
        self.python_time.setGeometry(QtCore.QRect(40, 680, 201, 31))
        self.python_time.setText("")
        self.python_time.setObjectName("python_time")
        self.postgre_time = QtWidgets.QLabel(parent=self.centralwidget)
        self.postgre_time.setGeometry(QtCore.QRect(710, 680, 211, 31))
        self.postgre_time.setText("")
        self.postgre_time.setObjectName("postgre_time")
        self.python_title = QtWidgets.QLabel(parent=self.centralwidget)
        self.python_title.setGeometry(QtCore.QRect(40, 210, 261, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.python_title.setFont(font)
        self.python_title.setObjectName("python_title")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1401, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.query_title.setText(_translate("MainWindow", "Query:"))
        self.query.setPlaceholderText(_translate("MainWindow", "Write your Query here...."))
        self.top_k.setPlaceholderText(_translate("MainWindow", "Top K"))
        self.search_button.setText(_translate("MainWindow", "SEARCH"))
        self.home_button.setText(_translate("MainWindow", "HOME"))
        self.postgres_title.setText(_translate("MainWindow", "Using PostgreSQL - Top K"))
        self.python_title.setText(_translate("MainWindow", "Using Python - Top K"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_Query()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
