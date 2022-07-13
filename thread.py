import random
import sys
import numpy as np
import time

from PySide2.QtCore import QObject, QRunnable, QThreadPool, QTimer, Signal
from PySide2.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

# Многопоточка
class WorkerSignals(QObject):
    finished = Signal()
    error = Signal(str)
    result = Signal(int)


class Worker(QRunnable):
    def __init__(self, wait=1):
        super().__init__()
        self.signals = WorkerSignals()
        self.wait = wait

    def run(self):
        try:
            time.sleep(self.wait)
            var = 1

        except Exception as e:
            self.signals.error.emit(str(e))
        else:
            self.signals.finished.emit()
            self.signals.result.emit(var)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.sum_var_after_worker = 0


        self.threadpool = QThreadPool()
        print(
            "Multithreading with maximum %d threads" % self.threadpool.maxThreadCount()
        )

        self.counter = 0
        layout = QVBoxLayout()

        self.l = QLabel("Start")
        b = QPushButton("DANGER!")
        b.pressed.connect(self.oh_no)

        layout.addWidget(self.l)
        layout.addWidget(b)

        w = QWidget()
        w.setLayout(layout)

        self.setCentralWidget(w)

        self.show()

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.recurring_timer)
        self.timer.start()

    def oh_no(self):
        worker = Worker()
        worker.signals.result.connect(self.worker_output)
        worker.signals.finished.connect(self.worker_complete)
        worker.signals.error.connect(self.worker_error)
        self.threadpool.start(worker)

    def worker_output(self, s):
        self.sum_var_after_worker += s
        print("RESULT", s)

    def worker_complete(self):
        print("sum_var", self.sum_var_after_worker)
        print("THREAD COMPLETE!")

    def worker_error(self, t):
        print("ERROR: %s" % t)

    def recurring_timer(self):
        self.counter += 1
        self.l.setText("Counter: %d" % self.counter)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec_()