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
import time
from pathlib import Path

from PySide2.QtCore import QRectF, Qt
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
    QMenu,
    QAction,
    QMessageBox,
    QInputDialog,
    QGraphicsLineItem,
    QGraphicsItem,
)

from PySide2.QtGui import QImage, QIcon, QPixmap, QFont, QColor, QPainter, QPen

# Классы проекта
# db
from data_base import class_db
from client import client




class Object_point(QGraphicsItem):
    def __init__(self, thickness):
        super().__init__()
        self.tag = None
        self.thickness = thickness

    def boundingRect(self):
        # print('boundingRect')
        return QRectF(-(self.thickness), -(self.thickness), self.thickness, self.thickness)

    def paint(self, painter, option, widget):  # рисуем новый квадрат со стороной 10
        # print('paint')
        painter.setPen(Qt.red)
        painter.setBrush(Qt.red)
        painter.drawRect(-(self.thickness), -(self.thickness), self.thickness, self.thickness)


class Painter(QMainWindow):
    """ Основное окно программы UI"""

    def __init__(self):
        super().__init__()
        self.set_ico()
        self.init_UI()

        # Атрибуты класса
        # а. Переменные отвечающие за подключение БД
        self.db_name = ''
        self.db_path = ''

        # б. Переменная ген.плана
        self.scale = 1

        # в. Переменная отвечающая за индекс строки в self.table_data
        self.row_ind_in_data_grid = None

        # г. Список для запоминания координат для определения масштаба
        # по следующему алгоритму:
        # при каждом нажатии на ген.план запоминает координаты клика (х,у)
        # затем при len(self.draw_point) == 4, запрашивает у пользователя
        # QInputDialog число, чему этом отрезок равен в метрах и вычисляется масштаб
        # self.draw_point становится [].

        self.draw_point = []

        # д. Переменная наличия ключа на сервере
        self.check_key = True

    def set_ico(self):
        """
        Функция установки иконок в приложение
        """
        path_ico = str(Path(os.getcwd()))
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
        self.clear_ico = QIcon(path_ico + '/ico/clear.png')
        self.save_ico = QIcon(path_ico + '/ico/save.png')
        self.del_one_ico = QIcon(path_ico + '/ico/del_one.png')
        self.copy_ico = QIcon(path_ico + '/ico/copy.png')
        self.ok_ico = QIcon(path_ico + '/ico/ok.png')
        self.db_ico = QIcon(path_ico + '/ico/data_base.png')
        self.replace_ico = QIcon(path_ico + '/ico/replace.png')
        self.del_ico = QIcon(path_ico + '/ico/del.png')
        self.plan_ico = QIcon(path_ico + '/ico/plan.png')

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
        self.scene.mousePressEvent = self.scene_press_event
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
        self.type_act.activated[str].connect(self.__select_type_act)
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
        self.plan_list.activated[str].connect(self.plan_list_select)
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
        self.add_row_copy.setIcon(self.copy_ico)
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
        self.del_last_coordinate.setIcon(self.del_one_ico)
        # self.del_last_coordinate.clicked.connect(self.delete_last_coordinate)

        self.del_all_coordinate = QPushButton("")
        self.del_all_coordinate.setToolTip('Удалить все координаты')
        self.del_all_coordinate.setIcon(self.clear_ico)
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

        # ___________5_START________________
        # Меню (тулбар)
        # База данных (меню)
        db_menu = QMenu('База данных', self)
        db_menu.setIcon(self.db_ico)
        db_create = QAction(self.ok_ico, 'Создать', self)
        db_create.setStatusTip('Создать новую базу данных')
        db_create.triggered.connect(self.database_create)
        db_menu.addAction(db_create)
        db_connect = QAction(self.db_ico, 'Подключиться', self)
        db_connect.setStatusTip('Подключиться к существующей базе данных')
        db_connect.triggered.connect(self.database_connect)
        db_menu.addAction(db_connect)
        # Генплан (меню)
        plan_menu = QMenu('Ген.план', self)
        plan_menu.setIcon(self.plan_ico)
        plan_add = QAction(self.ok_ico, 'Добавить', self)
        plan_add.setStatusTip('Добавить новый план объекта')
        plan_add.triggered.connect(self.plan_add)
        plan_menu.addAction(plan_add)
        plan_replace = QAction(self.replace_ico, 'Заменить', self)
        plan_replace.setStatusTip('Заменить план объекта')
        plan_replace.triggered.connect(self.plan_replace)
        plan_menu.addAction(plan_replace)
        plan_save = QAction(self.save_ico, 'Coхранить', self)
        plan_save.setStatusTip('Сохранить текущее изображение плана объекта как файл')
        plan_save.triggered.connect(self.plan_save)
        plan_menu.addAction(plan_save)
        plan_clear = QAction(self.clear_ico, 'Очистить', self)
        plan_clear.setStatusTip('Очистить план объекта')
        # plan_clear.triggered.connect(self.plan_clear)
        plan_menu.addAction(plan_clear)
        plan_del = QAction(self.del_ico, 'Удалить план с объектами', self)
        plan_del.setStatusTip('Удалить изображение плана c объекта')
        # plan_del.triggered.connect(self.plan_del)
        plan_menu.addAction(plan_del)

        # Меню приложения (верхняя плашка)
        menubar = self.menuBar()
        file_menu = menubar.addMenu('Файл')
        file_menu.addMenu(db_menu)
        plans_menu = menubar.addMenu('План')
        plans_menu.addMenu(plan_menu)

        # ___________5_END________________

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
            if header == 'Тип':
                item.setToolTip(
                    '''Тип оборудования:
                    0 - линейный
                    1 - площадной'''
                )
        # масштабирование под контент
        self.table_data.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table_data.horizontalHeader().setSectionResizeMode(8, QHeaderView.ResizeToContents)

    # ___________Функции_БД_START________________
    def database_create(self):
        self.db_name, self.db_path = class_db.Data_base('', '').db_create()
        self.connect_info(self.db_name, self.db_path)

    def database_connect(self):
        self.db_name, self.db_path = class_db.Data_base(self.db_name, self.db_path).db_connect()
        self.connect_info(self.db_name, self.db_path)
        class_db.Data_base(self.db_name, self.db_path).plan_list_update(self.plan_list)
        # self.del_all_item()  # очистить ген.планы от item

    def connect_info(self, name: str, path: str):
        """
        Проверка наличия данных о подключения БД
        Путь и имя базы данных не равны пустым строкам
        """
        if path != '' and name != '':
            self.data_base_info_connect.setText(f'База  данных {self.db_name}.db подключена!')
            self.data_base_info_connect.setStyleSheet('color: green')
        else:
            self.data_base_info_connect.setText('Нет подключения к базе данных...')
            self.data_base_info_connect.setStyleSheet('color: red')

    # ___________Функции_БД_END________________

    # ___________Функции_работы_с_ген.планом_START________________
    # Функции работы с ген.планом
    def plan_add(self):
        class_db.Data_base(self.db_name, self.db_path).plan_add()
        class_db.Data_base(self.db_name, self.db_path).plan_list_update(self.plan_list)

    def plan_save(self):
        text = str(int(time.time()))
        # self.del_all_item()
        self.scene.clearSelection()
        self.scene.setSceneRect(self.scene.itemsBoundingRect())
        image = QImage(self.scene.sceneRect().size().toSize(), QImage.Format_ARGB32)
        image.fill(Qt.transparent)
        painter = QPainter(image)
        self.scene.render(painter)
        image.save((f"{self.db_path}/{text}.jpg"), "JPG")
        painter.end()

    def plan_replace(self):
        """Функция замены ген.плана на сцене"""
        class_db.Data_base(self.db_name, self.db_path).plan_replace(self.plan_list.currentText())
        class_db.Data_base(self.db_name, self.db_path).plan_list_update(self.plan_list)
        self.plan_list_select(self.plan_list.currentText())

    def plan_list_select(self, text: str) -> None:
        """
        Функция выбора ген.плана из списка QComboBox (self.plan_list)
        :@param text: текст из QComboBox (self.plan_list) с наименованием плана

        :@return: None
        """

        self.scale_plan.setText('')
        self.result_type_act.setText('')

        # 1. Ген.план
        data, image_data = class_db.Data_base(self.db_name, self.db_path).get_plan_in_db(text)
        if image_data is not None:
            self.scene.clear()
            qimg = QImage.fromData(image_data)
            self.pixmap = QPixmap.fromImage(qimg)
            self.scene.addPixmap(self.pixmap)
            self.scene.setSceneRect(QRectF(self.pixmap.rect()))

        # 2. Данные для таблицы
        # 2.1. Удалить данные из таблицы
        self.table_data.setRowCount(0)
        if len(data) != 0:
            # 3.1. Установить масштаб
            data = eval(data)
            self.scale_plan.setText(data.pop())  # крайний элемент списка всегда масштаб
            # 3.2. Заполнить таблицу
            for obj in data:
                count_row = self.table_data.rowCount()  # посчитаем количество строк
                self.table_data.insertRow(count_row)
                col = 0
                for item in obj:
                    # Запишем новые координаты после удаления в таблицу
                    widget_item_for_table = QTableWidgetItem(item)
                    self.table_data.setItem(count_row, col,
                                            widget_item_for_table)
                    col += 1

    # ___________Функции_с_ген.планом_END________________

    def scene_press_event(self, event):
        # проверим ключ на сервере
        self.check_key = client.Client().check_key()
        if not self.check_key:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Информация")
            msg.setText("Ключ на сервере отсутсвует!")
            msg.exec()
            self.draw_type_act.setChecked(False)
            self.draw_obj.setChecked(False)
            self.__clear_scale()
            return
        # Проверим наличие ген.плана
        if self.plan_list.currentText() != '--Нет ген.планов--':
            # Проверим нажатие кнопки draw_type_act,
            # что мы хотим определить
            # - масштаб
            # - измерить растояние
            # - определить площадь:

            if self.draw_type_act.isChecked():
                # Отожмем кнопку отрисовки координатов объектов
                self.draw_obj.setChecked(False)
                # 1. Выбран масштаб
                if self.type_act.currentIndex() == 0:
                    self.draw_point.append(str(event.scenePos().x()))  # замеряем координаты клика
                    self.draw_point.append(str(event.scenePos().y()))  # и записываем в draw_point
                    self.draw_all_item(self.draw_point)
                    if len(self.draw_point) == 4:  # как только длина draw_point == 4
                        num_int, ok = QInputDialog.getInt(self, "Масштаб", "Сколько метров:")
                        length = client.Client().server_get_lenght(self.draw_point)
                        if length > 0:
                            if ok and num_int > 0 and length > 0:
                                self.draw_point.clear()  # очищаем
                                self.result_type_act.setText(f"В отрезке {num_int} м: {round(length, 2)} пикселей")
                                self.scale_plan.setText(f"{float(length) / num_int:.3f}")
                                self.draw_type_act.setChecked(False)
                                self.del_all_item()
                            elif ok and num_int <= 0:
                                self.__clear_scale()
                            elif not ok:
                                self.__clear_scale()
                        else:
                            self.__clear_scale()
                    elif len(self.draw_point) > 4:
                        self.__clear_scale()
                # выбрано определение длины отрезка
                if self.type_act.currentIndex() == 1:
                    self.del_all_item()  # удалим все Item
                    if self.scale_plan.text() == "":  # проверим есть ли масштаб
                        msg = QMessageBox(self)
                        msg.setIcon(QMessageBox.Warning)
                        msg.setWindowTitle("Информация")
                        msg.setText("Не установлен масштаб")
                        msg.exec()
                        self.draw_type_act.setChecked(False)
                        return
                    self.draw_point.append(str(event.scenePos().x()))
                    self.draw_point.append(str(event.scenePos().y()))
                    self.draw_all_item(self.draw_point)
                    print(self.draw_point)
                    if len(self.draw_point) > 2:
                        length = client.Client().server_get_lenght(self.draw_point)
                        real_lenght = float(length) / float(self.scale_plan.displayText())
                        real_lenght = round(real_lenght, 2)
                        self.result_type_act.setText(f'Длина линии {real_lenght}, м')

                if self.type_act.currentIndex() == 2:
                    self.del_all_item()  # удалим все Item
                    if self.scale_plan.text() == "":  # проверим есть ли масштаб
                        msg = QMessageBox(self)
                        msg.setIcon(QMessageBox.Warning)
                        msg.setWindowTitle("Информация")
                        msg.setText("Не установлен масштаб")
                        msg.exec()
                        self.draw_type_act.setChecked(False)
                        return
                    self.draw_point.append(str(event.scenePos().x()))
                    self.draw_point.append(str(event.scenePos().y()))
                    self.draw_all_item(self.draw_point)

                    if len(self.draw_point) > 4:
                        area = client.Client().server_get_area(self.draw_point)
                        real_area = float(area) / pow(float(self.scale_plan.displayText()), 2)
                        real_area = round(real_area, 2)
                        self.result_type_act.setText(f'Площадь {real_area}, м2')


    # ___________Функции_отрисовки_объектов_на_ген.плане_START________________
    def del_all_item(self):
        """
        Удаляет все Item с картинки
        """
        # Находим все items на scene и переберем их
        for item in self.scene.items():  # удалить все линии точки и линии
            # Имя item
            name_item = str(item)
            # print(name_item)

            if name_item.find('QGraphicsLineItem') != -1:
                self.scene.removeItem(item)
            elif name_item.find('point') != -1:
                self.scene.removeItem(item)

    def draw_all_item(self, coordinate):
        """
        Рисует все Item на картинке
        """
        if coordinate == []:
            return
        i = 0
        k = 0
        thickness_marker = 5
        while i < len(coordinate):
            # thickness_marker = int(self.thickness_line.value() * 5)  # сторона маркера должна быть в 4 раза больше
            name_rings = Object_point(thickness_marker)
            name_rings.setPos(float(coordinate[i]), float(coordinate[i + 1]))
            self.scene.addItem(name_rings)
            i += 2
        while k < len(coordinate) - 2:
            line = QGraphicsLineItem(float(coordinate[k]), float(coordinate[k + 1]),
                                     float(coordinate[k + 2]), float(coordinate[k + 3]))
            line.setPen(QPen(Qt.blue, thickness_marker // 2))
            self.scene.addItem(line)
            k -= 2
            k += 4

    def __clear_scale(self):
        """
        Вспомогательная функция:
        - очищает массив точек списка масштаба
        - отжимает кнопку действия draw_type_act
        - очищает все items со сцены
        - очищает label с резульатами (длины, площади, масштаба)
        - очищает поле масштаба
        """
        self.draw_point.clear()  # очищаем draw_point
        self.draw_type_act.setChecked(False)
        self.del_all_item()
        self.result_type_act.clear()
        self.scale_plan.clear()

    def __select_type_act(self):
        """
        Вспомогательная функция:
        - очищает массив точек списка масштаба, (длины, площади)
        - очищает все items со сцены
        - отжимает кнопку действия draw_type_act
        """
        self.draw_point.clear()  # очистим координаты
        self.del_all_item()
        self.draw_type_act.setChecked(False)

    # ___________Функции_отрисовки_объектов_на_ген.плане_END________________

    def save_table_in_db(self):
        """
        Функция сохранения информации в базу данных из таблицы данных
        """
        # Проверки перед сохранением
        self.is_action_valid()  # проверки

        # Проверки пройдены, можно запоминать данные:
        class_db.Data_base(self.db_name, self.db_path).save_data_in_db(self.plan_list.currentText(),
                                                                       self.scale_plan.text(),
                                                                       self.table_data)

    def is_action_valid(self):
        """
        Функция проверки наличия всех данных для корректной работы
        """
        # 1. Есть ли база данных
        if self.db_name == '' and self.db_path == '':
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Информация")
            msg.setText("Нет подключения к базе данных!")
            msg.exec()
            return
        # 2. Есть ли генплан
        if self.plan_list.currentText() == '--Нет ген.планов--':
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Информация")
            msg.setText("Нет ген.плана!")
            msg.exec()
            return
        # 3. Есть ли масштаб
        if self.scale_plan.text() == '':
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Информация")
            msg.setText("Не указан масштаб!")
            msg.exec()
            return

        # 4. Есть ли подключение к серверу
        if not self.check_key:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Информация")
            msg.setText("Ключ на сервере отсутсвует!")
            msg.exec()
            return




if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    window = Painter()
    app.exec_()
