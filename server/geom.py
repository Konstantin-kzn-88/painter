from shapely.geometry import LineString, Polygon

def lenght_for_line(data:list)->float:
    i = 0
    get_tuple = []
    while i < len(data):
        tuple_b = (float(data[i]), float(data[i + 1]))
        get_tuple.append(tuple_b)
        i += 2
        if i == len(data):
            break
    length = LineString(get_tuple).length  # shapely
    return length

def area_for_poligon(data:list)->float:
    i = 0
    get_tuple = []
    while i < len(data):
        tuple_b = (float(data[i]), float(data[i + 1]))
        get_tuple.append(tuple_b)
        i += 2
        if i == len(data):
            break
    area = Polygon(get_tuple).area  # shapely
    return area