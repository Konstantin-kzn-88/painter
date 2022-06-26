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

from PySide2.QtCore import QModelIndex
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
    QTableWidget,
    QTableWidgetItem,
    QStyleFactory,
    QHeaderView,
)

from PySide2.QtGui import QIcon, QPixmap, QFont, QColor


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
        self.plus_ico = QIcon(path_ico + '/ico/plus.png')
        self.minus_ico = QIcon(path_ico + '/ico/minus.png')
        self.book_ico = QIcon(path_ico + '/ico/book.png')
        self.object_ico = QIcon(path_ico + '/ico/object.png')
        self.clear = QIcon(path_ico + '/ico/clear.png')
        self.save_ico = QIcon(path_ico + '/ico/save.png')
        self.del_one = QIcon(path_ico + '/ico/del_one.png')
        self.copy = QIcon(path_ico + '/ico/copy.png')

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
        # Упаковываем все в QGroupBox Рамка №1
        layout_scale = QFormLayout(self)
        GB_scale = QGroupBox('Интрументы')
        GB_scale.setStyleSheet("QGroupBox { font-weight : bold; }")
        layout_scale.addRow("", self.scale_plan)
        layout_scale.addRow("", self.type_act)
        layout_scale.addRow("", self.draw_type_act)
        layout_scale.addRow("", self.result_type_act)
        GB_scale.setLayout(layout_scale)

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
        self.color_zone1_btn = QPushButton("R1")
        self.color_zone1_btn.setIcon(self.color_ico)
        self.color_zone1_btn.setToolTip("Цвет зоны 1")
        self.color_zone1_btn.setStyleSheet("background-color: red")
        # self.color_zone1_btn.clicked.connect(self.select_color)
        self.color_zone2_btn = QPushButton("R2")
        self.color_zone2_btn.setIcon(self.color_ico)
        self.color_zone2_btn.setToolTip("Цвет зоны 2")
        self.color_zone2_btn.setStyleSheet("background-color: blue")
        # self.color_zone2_btn.clicked.connect(self.select_color)
        self.color_zone3_btn = QPushButton("R3")
        self.color_zone3_btn.setIcon(self.color_ico)
        self.color_zone3_btn.setToolTip("Цвет зоны 3")
        self.color_zone3_btn.setStyleSheet("background-color: orange")
        # self.color_zone3_btn.clicked.connect(self.select_color)
        self.color_zone4_btn = QPushButton("R4")
        self.color_zone4_btn.setIcon(self.color_ico)
        self.color_zone4_btn.setToolTip("Цвет зоны 4")
        self.color_zone4_btn.setStyleSheet("background-color: green")
        # self.color_zone4_btn.clicked.connect(self.select_color)
        self.color_zone5_btn = QPushButton("R5")
        self.color_zone5_btn.setIcon(self.color_ico)
        self.color_zone5_btn.setToolTip("Цвет зоны 5")
        self.color_zone5_btn.setStyleSheet("background-color: magenta")
        # self.color_zone5_btn.clicked.connect(self.select_color)
        self.color_zone6_btn = QPushButton("R6")
        self.color_zone6_btn.setIcon(self.color_ico)
        self.color_zone6_btn.setToolTip("Цвет зоны 6")
        self.color_zone6_btn.setStyleSheet("background-color: yellow")
        # self.color_zone6_btn.clicked.connect(self.select_color)

        # Упаковываем все в QGroupBox Рамка №1
        layout_zone = QFormLayout(self)
        GB_zone = QGroupBox('Выбор цвета')
        GB_zone.setStyleSheet("QGroupBox { font-weight : bold; }")
        hbox_zone_1_3 = QHBoxLayout()
        hbox_zone_1_3.addWidget(self.color_zone1_btn)
        hbox_zone_1_3.addWidget(self.color_zone2_btn)
        hbox_zone_1_3.addWidget(self.color_zone3_btn)
        layout_zone.addRow("", hbox_zone_1_3)
        hbox_zone_2_6 = QHBoxLayout()
        hbox_zone_2_6.addWidget(self.color_zone4_btn)
        hbox_zone_2_6.addWidget(self.color_zone5_btn)
        hbox_zone_2_6.addWidget(self.color_zone6_btn)
        layout_zone.addRow("", hbox_zone_2_6)
        GB_zone.setLayout(layout_zone)
        # ___________3_END________________

        # ___________4_START________________
        # Рамка
        layout_data = QFormLayout(self)
        GB_data = QGroupBox('Данные об объектах')
        GB_data.setStyleSheet("QGroupBox { font-weight : bold; }")

        # таблица
        data_grid = QGridLayout(self)
        data_grid.setColumnStretch(0, 15)
        data_grid.setColumnStretch(1, 1)

        self.table_data = QTableWidget(0, 9)
        self.table_data_view()  # фукция отрисовки заголовков таблицы
        # self.table_data.clicked[QModelIndex].connect(self.get_index_in_table)
        # кнопки управления
        layout_control = QFormLayout(self)
        GB_control = QGroupBox('Действия объекта')

        self.add_row = QPushButton("Добавить")
        self.add_row.setStyleSheet("text-align: left;")
        self.add_row.setIcon(self.plus_ico)
        self.add_row.setToolTip("Добавить строку в таблицу")
        # self.add_row.clicked.connect(self.add_in_table)
        self.add_row_copy = QPushButton("")
        self.add_row_copy.setIcon(self.copy)
        self.add_row_copy.setToolTip("Скопировать последнюю строку")
        # self.add_row.clicked.connect(self.add_in_table)

        self.del_row = QPushButton("Удалить")
        self.del_row.setStyleSheet("text-align: left;")
        self.del_row.setIcon(self.minus_ico)
        self.del_row.setToolTip("Удалить строку из таблицу")
        # self.del_row.clicked.connect(self.del_in_table)

        self.draw_obj = QPushButton("Координаты")
        self.draw_obj.setStyleSheet("text-align: left;")
        self.draw_obj.setToolTip('Указать координаты выбранного в таблице объекта')
        self.draw_obj.setIcon(self.object_ico)
        # self.draw_obj.clicked.connect(self.change_draw_obj)
        self.draw_obj.setCheckable(True)
        self.draw_obj.setChecked(False)

        self.del_last_coordinate = QPushButton("")
        self.del_last_coordinate.setToolTip('Удалить последнюю координату')
        self.del_last_coordinate.setIcon(self.del_one)
        # self.del_last_coordinate.clicked.connect(self.delete_last_coordinate)

        self.del_all_coordinate = QPushButton("")
        self.del_all_coordinate.setToolTip('Удалить все координаты')
        self.del_all_coordinate.setIcon(self.clear)
        # self.del_all_coordinate.clicked.connect(self.delete_all_coordinates)

        self.save_table = QPushButton("Сохранить")
        self.save_table.setToolTip('Сохранить объекты в базу данных')
        self.save_table.setIcon(self.save_ico)
        # self.save_table.clicked.connect(self.save_table_in_db)

        hbox_add = QHBoxLayout()
        hbox_add.addWidget(self.add_row)
        hbox_add.addWidget(self.add_row_copy)
        layout_control.addRow("", hbox_add)
        layout_control.addRow("", self.del_row)
        layout_control.addRow("", self.draw_obj)
        hbox_coordinate = QHBoxLayout()
        hbox_coordinate.addWidget(self.del_last_coordinate)
        hbox_coordinate.addWidget(self.del_all_coordinate)
        layout_control.addRow("", hbox_coordinate)
        layout_control.addRow("", self.save_table)
        GB_control.setLayout(layout_control)

        data_grid.addWidget(self.table_data, 0, 0, 1, 1)
        data_grid.addWidget(GB_control, 0, 1, 1, 1)
        layout_data.addRow("", data_grid)
        GB_data.setLayout(layout_data)
        # ___________4_END________________

        # ___________N_START________________
        # Разместим основные QGroupBox на сетке
        grid.addWidget(GB_picture, 0, 0, 1, 0)
        grid.addWidget(GB_scale, 1, 0, -1, 1)
        grid.addWidget(GB_plan, 2, 2, 1, 1)
        grid.addWidget(GB_zone, 1, 2, 1, 1)
        grid.addWidget(GB_data, 1, 1, -1, 1)
        # Установить отсновну сетку как слой
        central_widget.setLayout(grid)
        # Установить центральный виджет
        self.setCentralWidget(central_widget)
        # ___________N_START________________
        self.show()

    def table_data_view(self):
        """
        Оформление таблицы для введения данных self.table_data
        """

        header_list = ['Название объекта', 'R1, м', 'R2, м',
                       'R3, м', 'R4, м',
                       'R5, м', 'R6, м', 'Тип', 'Координаты']

        for header in header_list:
            item = QTableWidgetItem(header)
            item.setBackground(QColor(0, 225, 0))
            self.table_data.setHorizontalHeaderItem(header_list.index(header), item)
        # масштабирование под контент
        self.table_data.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table_data.horizontalHeader().setSectionResizeMode(8, QHeaderView.ResizeToContents)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    window = Painter()
    app.exec_()
