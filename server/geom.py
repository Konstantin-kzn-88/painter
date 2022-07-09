from shapely.geometry import LineString, Polygon

"""
Модуль geom предназначен для:
 - вычисления расстояния между точками
 - площади произвольного выпуклого многоугольника
 - диаметр зоны для рисования
"""
def lenght_for_line(data:list)->float:
    return LineString(list(zip(*[iter(data)] * 2))).length

def area_for_poligon(data:list)->float:
    return Polygon(list(zip(*[iter(data)] * 2))).area

def zone_with_scale(zone: float, scale: float)->float:
    return zone * scale * 2 # т.к. на вход радиус, а нужен диаметр


