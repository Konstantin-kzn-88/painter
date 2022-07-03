from shapely.geometry import LineString, Polygon

"""
Модуль geom предназначен для:
 - вычисления расстояния между точками
 - площади произвольного выпуклого многоугольника
"""

def lenght_for_line(data:list)->float:
    length = LineString(list(zip(*[iter(data)] * 2))).length  # shapely
    return length

def area_for_poligon(data:list)->float:
    area = Polygon(list(zip(*[iter(data)] * 2))).area  # shapely
    return area

