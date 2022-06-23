# from PySide2 import QtCore, QtWidgets
#
# class MyApp(QtWidgets.QMainWindow):
#     def __init__(self, parent=None):
#         QtWidgets.QMainWindow.__init__(self, parent)
#         self.t = TestThread()
#         self.result_list = [0,0,0,0]
#         self.initUi()
#
#     def initUi(self):
#         centralWidget = QtWidgets.QWidget()
#         self.setCentralWidget(centralWidget)
#         layout = QtWidgets.QVBoxLayout()
#
#         self.button = QtWidgets.QPushButton("start")
#         self.button.clicked.connect(self.t.start)
#
#         self.button2 = QtWidgets.QPushButton("stop")
#         self.button2.clicked.connect(self.stopThread)
#
#         layout.addWidget(self.button)
#         layout.addWidget(self.button2)
#
#         centralWidget.setLayout(layout)
#
#         self.t.started.connect(lambda: print("Поток запущен"))
#         self.t.finished.connect(lambda: print("Поток завершен"))
#         self.t.mysignal.connect(self.sum_result, QtCore.Qt.AutoConnection)
#
#
#     def sum_result(self, list_):
#         self.result_list = [x+y for x, y in zip(self.result_list, list_)]
#         print(self.result_list)
#
#     def stopThread(self):
#         self.t.status = False
#
#
# class TestThread(QtCore.QThread):
#     mysignal = QtCore.Signal(list)  # обязательно передать тип возвращаемого значения
#     def run(self) -> None:
#         self.mysignal.emit(list([1,2,3,4]))  # излучатель сигнала из потока
#
#
#
# if __name__ == "__main__":
#     app = QtWidgets.QApplication()
#     myapp = MyApp()
#     myapp.show()
#     app.exec_()

import time
from PySide2 import QtCore, QtWidgets

class MyApp(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.result_list = [0,0,0,0]
        self.initUi()

    def initUi(self):
        centralWidget = QtWidgets.QWidget()
        self.setCentralWidget(centralWidget)
        layout = QtWidgets.QVBoxLayout()
        self.button = QtWidgets.QPushButton("start")
        self.button.clicked.connect(self.start_thread)
        layout.addWidget(self.button)
        centralWidget.setLayout(layout)


    def start_thread(self):
        t = TestThread().start()
        # # t.started.connect(lambda: print("Поток запущен"))
        t.finished.connect(lambda: print("Поток завершен"))
        # t.mysignal.connect(self.sum_result, QtCore.Qt.AutoConnection)


    def sum_result(self, list_):
        self.result_list = [x+y for x, y in zip(self.result_list, list_)]
        print(self.result_list)


class TestThread(QtCore.QThread):
    mysignal = QtCore.Signal(list)  # обязательно передать тип возвращаемого значения
    def run(self) -> None:
        time.sleep(2)
        self.mysignal.emit(list([1,2,3,4]))  # излучатель сигнала из потока



if __name__ == "__main__":
    app = QtWidgets.QApplication()
    myapp = MyApp()
    myapp.show()
    app.exec_()