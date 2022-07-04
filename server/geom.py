from shapely.geometry import LineString, Polygon

"""
Модуль geom предназначен для:
 - вычисления расстояния между точками
 - площади произвольного выпуклого многоугольника
"""
def lenght_for_line(data:list)->float:
    return LineString(list(zip(*[iter(data)] * 2))).length

def area_for_poligon(data:list)->float:
    return Polygon(list(zip(*[iter(data)] * 2))).area


