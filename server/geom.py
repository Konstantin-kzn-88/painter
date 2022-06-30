from shapely.geometry import LineString, Polygon

def lenght_for_line(data:list)->float:
    x_a = float(data[0])  # по координатам двух точек
    y_a = float(data[1])  # вычисляем расстояние в пикселях
    x_b = float(data[2])
    y_b = float(data[3])
    length = LineString([(x_a, y_a), (x_b, y_b)]).length
    return length