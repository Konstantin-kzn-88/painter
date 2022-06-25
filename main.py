# -----------------------------------------------------------
# Класс предназначен для GUI программы Painter
#
# Программа реализует возможность отрисовки зон действия
# поражающих факторов (взрывы, пожары и пр.) для 6 различных
# зон (радиусов).
# Основные особенности:
# - клиент-серверное приложение, графические результаты получаются
# путем отправки на сервер данных и приемом обратно данных для отрисовки
#
# (C) 2022 Kuznetsov Konstantin
# email kuznetsovkm@yandex.ru
# -----------------------------------------------------------

import os
import sys
from pathlib import Path

from PySide2.QtCore import QObject, QRunnable, QThreadPool, QTimer, Signal
from PySide2.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QGridLayout,
    QFormLayout,
    QGroupBox,
    QGraphicsScene,
    QScrollArea,
    QGraphicsView,
)

from PySide2.QtGui import QIcon, QPixmap


class Painter(QMainWindow):
    """ Основное окно программы UI"""

    def __init__(self):
        super().__init__()
        self.init_UI()
        self.set_ico()

    def set_ico(self):
        """
        Функция установки иконок в приложение
        """
        path_ico = str(Path(os.getcwd()).parents[0])
        self.main_ico = QIcon(path_ico + '\ico\painter.png')
        self.setWindowIcon(self.main_ico)

    def init_UI(self):
        self.setGeometry(500, 500, 1000, 750)
        self.setWindowTitle('Painter')
        # Центральный виджет
        central_widget = QWidget()
        # Основная сетка компановки
        grid = QGridLayout(self)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 7)
        grid.setRowStretch(0, 7)
        grid.setRowStretch(1, 1)

        # ___________1_START________________
        # Генплан
        # Рамка
        layout_picture = QFormLayout(self)
        GB_picture = QGroupBox('План расположения')
        GB_picture.setStyleSheet("QGroupBox { font-weight : bold; }")
        #создаем сцену и плосы прокрутки картинки
        self.scene = QGraphicsScene(self)
        # создаем полосы прокрутки
        self.area = QScrollArea(self)
        # добавляем картинку
        self.pixmap = QPixmap()
        self.scene.addPixmap(self.pixmap)
        # создаем обработчик клика мыши по сцене
        # self.scene.mousePressEvent = self.scene_press_event
        # создаем вид который визуализирует сцену
        self.view = QGraphicsView(self.scene, self)
        self.area.setWidget(self.view)
        self.area.setWidgetResizable(True)
        layout_picture.addRow("", self.area)
        GB_picture.setLayout(layout_picture)
        # ___________1_END________________

        # ___________N_START________________
        # Разместим основные QGroupBox на сетке
        grid.addWidget(GB_picture, 0, 0, 1, 0)
        # Установить отсновну сетку как слой
        central_widget.setLayout(grid)
        # Установить центральный виджет
        self.setCentralWidget(central_widget)
        # ___________N_START________________
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Painter()
    app.exec_()
