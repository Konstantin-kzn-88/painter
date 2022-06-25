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
    QHBoxLayout,
    QWidget,
    QGridLayout,
    QFormLayout,
    QGroupBox,
    QGraphicsScene,
    QScrollArea,
    QGraphicsView,
    QLineEdit,
    QComboBox,
)

from PySide2.QtGui import QIcon, QPixmap, QFont


class Painter(QMainWindow):
    """ Основное окно программы UI"""

    def __init__(self):
        super().__init__()
        self.set_ico()
        self.init_UI()


    def set_ico(self):
        """
        Функция установки иконок в приложение
        """
        path_ico = str(Path(os.getcwd()).parents[0])
        self.main_ico = QIcon(path_ico + '/ico/painter.png')
        self.setWindowIcon(self.main_ico)

        self.scale_ico = QIcon(path_ico + '/ico/scale.png')
        self.dist_ico = QIcon(path_ico + '/ico/polyline.png')
        self.area_ico = QIcon(path_ico + '/ico/area.png')
        self.area_ico = QIcon(path_ico + '/ico/area.png')
        self.color_ico = QIcon(path_ico + '/ico/color_select.png')

    def init_UI(self):
        self.setGeometry(500, 500, 1000, 750)
        self.setWindowTitle('Painter')
        # Центральный виджет
        central_widget = QWidget()
        # Основная сетка компановки
        grid = QGridLayout(self)
        grid.setRowStretch(0, 7)

        # ___________1_START________________
        # Генплан
        # Рамка
        layout_picture = QFormLayout(self)
        GB_picture = QGroupBox('План расположения')
        GB_picture.setStyleSheet("QGroupBox { font-weight : bold; }")
        # создаем сцену и плосы прокрутки картинки
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

        # ___________2_START________________
        # Рамка №1. Маштаб  (то что будет в рамке 1)
        self.scale_plan = QLineEdit()
        self.scale_plan.setPlaceholderText("Масштаб")
        self.scale_plan.setToolTip("В одном пикселе метров")
        self.scale_plan.setReadOnly(True)
        # Упаковываем все в QGroupBox Рамка №1
        layout_scale = QFormLayout(self)
        GB_scale = QGroupBox('Масштаб')
        GB_scale.setStyleSheet("QGroupBox { font-weight : bold; }")
        layout_scale.addRow("", self.scale_plan)
        GB_scale.setLayout(layout_scale)

        # Рамка №2. Действия (масштаб, расстояние, площадь)  (то что будет в рамке 2)
        self.type_act = QComboBox()  # тип действия
        self.type_act.addItems(["Масштаб", "Расстояние", "Площадь"])
        self.type_act.setItemIcon(0, self.scale_ico)
        self.type_act.setItemIcon(1, self.dist_ico)
        self.type_act.setItemIcon(2, self.area_ico)
        # self.type_act.activated[str].connect(self.select_type_act)
        self.result_type_act = QLabel()  # для вывода результата применения type_act + draw_type_act
        self.draw_type_act = QPushButton("Применить")
        # self.draw_type_act.clicked.connect(self.change_draw_type_act)
        self.draw_type_act.setCheckable(True)
        self.draw_type_act.setChecked(False)

        # Упаковываем все в QGroupBox Рамка №2
        layout_act = QFormLayout(self)
        GB_act = QGroupBox('Действие')
        GB_act.setStyleSheet("QGroupBox { font-weight : bold; }")
        layout_act.addRow("", self.type_act)
        layout_act.addRow("", self.draw_type_act)
        layout_act.addRow("", self.result_type_act)
        GB_act.setLayout(layout_act)

        # Рамка №3. Главной вкладки. Ситуацилнные планы. (то что будет в рамке 3)
        self.plan_list = QComboBox()  # ген.планы объекта
        self.plan_list.addItems(["--Нет ген.планов--"])
        self.plan_list.setToolTip("""Ген.планы объекта""")
        # self.plan_list.activated[str].connect(self.plan_list_select)
        self.data_base_info_connect = QLabel()  # информация о подключении базы данных
        self.data_base_info_connect.setText('Нет подключения к базе данных...')
        self.data_base_info_connect.setFont(QFont("Times", 10, QFont.Bold))
        self.data_base_info_connect.setStyleSheet('color: red')

        # Упаковываем все в QGroupBox Рамка №3
        layout_plan = QFormLayout(self)
        GB_plan = QGroupBox('Выбор ген.плана')
        GB_plan.setStyleSheet("QGroupBox { font-weight : bold; }")
        layout_plan.addRow("", self.plan_list)
        layout_plan.addRow("", self.data_base_info_connect)
        GB_plan.setLayout(layout_plan)
        # ___________2_END________________

        # ___________3_START________________
        # Рамка №1. Владки зон поражения. (то что будет в рамке 1)
        # color_zone набор кнопок для зон 6 возможных зон поражения
        self.color_zone1_btn = QPushButton("Зона 1")
        self.color_zone1_btn.setIcon(self.color_ico)
        self.color_zone1_btn.setToolTip("Цвет зоны 1")
        self.color_zone1_btn.setStyleSheet("background-color: red")
        # self.color_zone1_btn.clicked.connect(self.select_color)
        self.color_zone2_btn = QPushButton("Зона 2")
        self.color_zone2_btn.setIcon(self.color_ico)
        self.color_zone2_btn.setToolTip("Цвет зоны 2")
        self.color_zone2_btn.setStyleSheet("background-color: blue")
        # self.color_zone2_btn.clicked.connect(self.select_color)
        self.color_zone3_btn = QPushButton("Зона 3")
        self.color_zone3_btn.setIcon(self.color_ico)
        self.color_zone3_btn.setToolTip("Цвет зоны 3")
        self.color_zone3_btn.setStyleSheet("background-color: orange")
        # self.color_zone3_btn.clicked.connect(self.select_color)
        self.color_zone4_btn = QPushButton("Зона 4")
        self.color_zone4_btn.setIcon(self.color_ico)
        self.color_zone4_btn.setToolTip("Цвет зоны 4")
        self.color_zone4_btn.setStyleSheet("background-color: green")
        # self.color_zone4_btn.clicked.connect(self.select_color)
        self.color_zone5_btn = QPushButton("Зона 5")
        self.color_zone5_btn.setIcon(self.color_ico)
        self.color_zone5_btn.setToolTip("Цвет зоны 5")
        self.color_zone5_btn.setStyleSheet("background-color: magenta")
        # self.color_zone5_btn.clicked.connect(self.select_color)
        self.color_zone6_btn = QPushButton("Зона 6")
        self.color_zone6_btn.setIcon(self.color_ico)
        self.color_zone6_btn.setToolTip("Цвет зоны 6")
        self.color_zone6_btn.setStyleSheet("background-color: yellow")
        # self.color_zone6_btn.clicked.connect(self.select_color)

        # Упаковываем все в QGroupBox Рамка №1
        layout_zone = QFormLayout(self)
        GB_zone = QGroupBox('Выбор цвета')
        GB_zone.setStyleSheet("QGroupBox { font-weight : bold; }")
        hbox_zone_1_2 = QHBoxLayout()
        hbox_zone_1_2.addWidget(self.color_zone1_btn)
        hbox_zone_1_2.addWidget(self.color_zone2_btn)
        layout_zone.addRow("", hbox_zone_1_2)
        hbox_zone_3_4 = QHBoxLayout()
        hbox_zone_3_4.addWidget(self.color_zone3_btn)
        hbox_zone_3_4.addWidget(self.color_zone4_btn)
        layout_zone.addRow("", hbox_zone_3_4)
        hbox_zone_5_6 = QHBoxLayout()
        hbox_zone_5_6.addWidget(self.color_zone5_btn)
        hbox_zone_5_6.addWidget(self.color_zone6_btn)
        layout_zone.addRow("", hbox_zone_5_6)
        GB_zone.setLayout(layout_zone)
        # ___________3_END________________

        # ___________N_START________________
        # Разместим основные QGroupBox на сетке
        grid.addWidget(GB_picture, 0, 0, 1, 0)
        grid.addWidget(GB_scale, 1, 0, 1, 1)
        grid.addWidget(GB_act, 2, 0, 1, 1)
        grid.addWidget(GB_plan, 3, 0, 1, 1)
        grid.addWidget(GB_zone, 1, 1, -1, -1)
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
