# -----------------------------------------------------------
# Функция реализует:
# - рисование зон действия поражающих факторов
# -
#
# (C) 2022 Kuznetsov Konstantin
# email kuznetsovkm@yandex.ru
# -----------------------------------------------------------

def draw_from_data(self, data: list, fill_thickness: int, scale_plan:float, pic_size: tuple):
    '''
    Рисование зон
    :param data список радиусов вида [[1,2,3,4,5,6],[1,2,3,4,5,6]..n]
                количество списков = количетву отрисовываемых объектов .
    :param fill_thickness ширина линии отрисовки
                        fill_thickness = 0 - русует с заливкой,
                        fill_thickness > 0 рисует зоны шириной  fill_thickness пикселей.
    :param scale_plan - масштаб отрисовки data
    :param scale_plan
    '''


    # 2.2. Получить координаты и типы объектов
    type_obj = []
    coordinate_obj = []
    for row in range(0, self.table_data.rowCount()):  # получим типы объектов
        type_obj.append(int(self.table_data.item(row, 13).text()))
        coordinate_obj.append(eval(self.table_data.item(row,
                                                        self.table_data.columnCount() - 1).text()))

    # 3. Нарисовать
    # 3.1. Определим все цвета зон покнопкам
    color_zone_arr = self.get_color_for_zone()

    # создадим соразмерный pixmap_zone и сделаем его прозрачным
    pixmap_zone = QPixmap(pixmap.width(), pixmap.height())
    pixmap_zone.fill(QColor(255, 255, 255, 255))
    # Создадим QPainter
    qp = QPainter(pixmap_zone)
    # Начнем рисование
    qp.begin(pixmap_zone)

    for zone_index in range(-1, -7, -1):
        i = 0  # итератор для объектов
        k = 0  # итератор для объектов без заливки
        for obj in type_obj:
            # # начинаем рисовать с последнего цвета
            color = color_zone_arr[zone_index]
            zone = math.fabs(float(data[i][zone_index]) * scale_plan * 2)  # т.к. на вход радиус, а нужен диаметр
            # зона может быть 0 тогда ничего рисовать не надо
            if zone == 0:
                continue

            # определим ручку и кисточку
            pen = QPen(QColor(color[0], color[1], color[2], color[3]), zone, QtCore.Qt.SolidLine)
            brush = QBrush(QColor(color[0], color[1], color[2], color[3]))
            # со сглаживаниями
            pen.setJoinStyle(Qt.RoundJoin)
            # закругленный концы
            pen.setCapStyle(Qt.RoundCap)
            qp.setPen(pen)
            qp.setBrush(brush)

            # возьмем координаты оборудования
            obj_coord = self.get_polygon(coordinate_obj[i])
            if len(obj_coord) >= 2:  # координаты можно преобразовать в полигон

                if obj == 0:
                    # линейн. получим полигон
                    qp.drawPolyline(obj_coord)
                else:
                    # стац. об. получим полигон
                    qp.drawPolyline(obj_coord)
                    qp.drawPolygon(obj_coord, Qt.OddEvenFill)
            else:  # не получается полигон, значит точка
                pen_point = QPen(QColor(color[0], color[1], color[2], color[3]), 1, QtCore.Qt.SolidLine)
                qp.setPen(pen_point)
                point = QPoint(int(float(coordinate_obj[i][0])), int(float(coordinate_obj[i][1])))
                qp.drawEllipse(point, zone / 2, zone / 2)  # т.к. нужен радиус

            i += 1  # следующий объект

        # Рисуем прозрачные

        if fill_thickness != 0:
            for obj in reversed(type_obj):
                zone_without_fill = math.fabs(
                    float(data[k][zone_index]) * scale_plan * 2) - fill_thickness

                # определим ручку и кисточку
                pen_without_fill = QPen(QColor(255, 255, 255, 255), zone_without_fill,
                                        Qt.SolidLine)
                brush_without_fill = QBrush(QColor(255, 255, 255, 255))
                # со сглаживаниями
                pen_without_fill.setJoinStyle(Qt.RoundJoin)
                # закругленный концы
                pen_without_fill.setCapStyle(Qt.RoundCap)
                qp.setPen(pen_without_fill)
                qp.setBrush(brush_without_fill)

                # возьмем координаты оборудования
                obj_coord = self.get_polygon(coordinate_obj[k])
                if len(obj_coord) >= 2:  # координаты можно преобразовать в полигон

                    if obj == 0:
                        # линейн. получим полигон
                        qp.drawPolyline(obj_coord)
                    else:
                        # стац. об. получим полигон
                        qp.drawPolyline(obj_coord)
                        qp.drawPolygon(obj_coord, Qt.OddEvenFill)
                else:  # не получается полигон, значит точка
                    pen_point = QPen(QColor(255, 255, 255, 255), 1,
                                     Qt.SolidLine)
                    qp.setPen(pen_point)
                    point = QPoint(int(float(coordinate_obj[k][0])), int(float(coordinate_obj[k][1])))
                    qp.drawEllipse(point, zone_without_fill / 2, zone_without_fill / 2)  # т.к. нужен радиус

                k += 1  # следующий объект

    # Завершить рисование
    qp.end()
    # удалить белый фон (при наличии)
    pixmap_zone = class_data_draw.Data_draw().del_white_pixel(pixmap_zone)
    # Положим одну картинку на другую
    painter = QPainter(pixmap)
    painter.begin(pixmap)
    painter.setOpacity(self.opacity.value())
    painter.drawPixmap(0, 0, pixmap_zone)
    painter.end()
    # Разместим на сцене pixmap с pixmap_zone
    self.scene.addPixmap(pixmap)
    self.scene.setSceneRect(QRectF(pixmap.rect()))