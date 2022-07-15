import sys
from PySide2.QtGui import QPixmap, QColor
from PySide2.QtWidgets import QMainWindow, QApplication, QLabel, QHBoxLayout, QPushButton, QWidget
import numpy

# 1. Случайные числа в матрице N на M
N = 500
M = 200
data = numpy.random.random((N, M))


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.title = "Image Viewer"
        self.setWindowTitle(self.title)
        central_widget = QWidget()
        box = QHBoxLayout()
        self.label = QLabel()
        self.button = QPushButton("Click me")
        self.button.clicked.connect(self.save_heat_map)
        box.addWidget(self.label)
        box.addWidget(self.button)
        central_widget.setLayout(box)
        self.setCentralWidget(central_widget)

    def save_heat_map(self):
        # создадим соразмерный pixmap_zone и сделаем его прозрачным
        pixmap_zone = QPixmap(N, M)
        pixmap_zone.fill(QColor(255, 255, 255, 255))
        # Нарисуем тепловую карту
        qimg_zone = pixmap_zone.toImage()
        heat_map = self.create_heat_map(data, N, M, qimg_zone)
        heat_map.save('test_output.png')


    def create_heat_map(self, arr, width: int, height: int, qimg_zone):
        max_el = arr.max()
        for x in range(width):
            for y in range(height):
                if arr[x, y] >= max_el:
                    qimg_zone.setPixelColor(x, y, QColor(255, 0, 0, 255))
                # красный
                elif max_el * 1.00 > arr[x, y] >= max_el * 0.90:
                    qimg_zone.setPixelColor(x, y, QColor(255, 10, 0, 255))
                # рыжий
                elif max_el * 0.90 > arr[x, y] >= max_el * 0.95:
                    qimg_zone.setPixelColor(x, y, QColor(255, 40, 0, 255))
                elif max_el * 0.95 > arr[x, y] >= max_el * 0.80:
                    qimg_zone.setPixelColor(x, y, QColor(255, 80, 0, 255))
                elif max_el * 0.80 > arr[x, y] >= max_el * 0.85:
                    qimg_zone.setPixelColor(x, y, QColor(255, 120, 0, 255))
                elif max_el * 0.85 > arr[x, y] >= max_el * 0.70:
                    qimg_zone.setPixelColor(x, y, QColor(255, 150, 0, 255))
                # желтый
                elif max_el * 0.70 > arr[x, y] >= max_el * 0.65:
                    qimg_zone.setPixelColor(x, y, QColor(255, 170, 0, 255))
                elif max_el * 0.65 > arr[x, y] >= max_el * 0.60:
                    qimg_zone.setPixelColor(x, y, QColor(255, 190, 0, 255))
                elif max_el * 0.60 > arr[x, y] >= max_el * 0.55:
                    qimg_zone.setPixelColor(x, y, QColor(255, 210, 0, 255))
                elif max_el * 0.55 > arr[x, y] >= max_el * 0.50:
                    qimg_zone.setPixelColor(x, y, QColor(255, 230, 0, 255))
                elif max_el * 0.50 > arr[x, y] >= max_el * 0.45:
                    qimg_zone.setPixelColor(x, y, QColor(255, 255, 0, 255))
                # салатовый
                elif max_el * 0.45 > arr[x, y] >= max_el * 0.475:
                    qimg_zone.setPixelColor(x, y, QColor(230, 255, 0, 255))
                elif max_el * 0.475 > arr[x, y] >= max_el * 0.450:
                    qimg_zone.setPixelColor(x, y, QColor(210, 255, 0, 255))
                elif max_el * 0.450 > arr[x, y] >= max_el * 0.425:
                    qimg_zone.setPixelColor(x, y, QColor(180, 255, 0, 255))
                elif max_el * 0.425 > arr[x, y] >= max_el * 0.400:
                    qimg_zone.setPixelColor(x, y, QColor(150, 255, 0, 255))
                # зеленый
                elif max_el * 0.400 > arr[x, y] >= max_el * 0.39:
                    qimg_zone.setPixelColor(x, y, QColor(100, 255, 0, 255))
                elif max_el * 0.39 > arr[x, y] >= max_el * 0.38:
                    qimg_zone.setPixelColor(x, y, QColor(70, 255, 0, 255))
                elif max_el * 0.38 > arr[x, y] >= max_el * 0.37:
                    qimg_zone.setPixelColor(x, y, QColor(40, 255, 0, 255))
                elif max_el * 0.37 > arr[x, y] >= max_el * 0.36:
                    qimg_zone.setPixelColor(x, y, QColor(10, 255, 0, 255))
                elif max_el * 0.36 > arr[x, y] >= max_el * 0.35:
                    qimg_zone.setPixelColor(x, y, QColor(0, 255, 0, 255))

                # голубой
                elif max_el * 0.35 > arr[x, y] >= max_el * 0.245:
                    qimg_zone.setPixelColor(x, y, QColor(0, 255, 40, 255))
                elif max_el * 0.245 > arr[x, y] >= max_el * 0.240:
                    qimg_zone.setPixelColor(x, y, QColor(0, 255, 80, 255))
                elif max_el * 0.240 > arr[x, y] >= max_el * 0.235:
                    qimg_zone.setPixelColor(x, y, QColor(0, 255, 100, 255))
                elif max_el * 0.235 > arr[x, y] >= max_el * 0.23:
                    qimg_zone.setPixelColor(x, y, QColor(0, 255, 120, 255))
                elif max_el * 0.23 > arr[x, y] >= max_el * 0.225:
                    qimg_zone.setPixelColor(x, y, QColor(0, 255, 150, 255))
                elif max_el * 0.225 > arr[x, y] >= max_el * 0.22:
                    qimg_zone.setPixelColor(x, y, QColor(0, 255, 210, 255))
                elif max_el * 0.22 > arr[x, y] >= max_el * 0.215:
                    qimg_zone.setPixelColor(x, y, QColor(0, 255, 240, 255))
                elif max_el * 0.215 > arr[x, y] >= max_el * 0.21:
                    qimg_zone.setPixelColor(x, y, QColor(0, 255, 255, 255))

                # темно-голубой
                elif max_el * 0.21 > arr[x, y] >= max_el * 0.19:
                    qimg_zone.setPixelColor(x, y, QColor(0, 220, 255, 255))
                elif max_el * 0.19 > arr[x, y] >= max_el * 0.18:
                    qimg_zone.setPixelColor(x, y, QColor(0, 210, 255, 255))
                elif max_el * 0.18 > arr[x, y] >= max_el * 0.17:
                    qimg_zone.setPixelColor(x, y, QColor(0, 200, 255, 255))
                elif max_el * 0.17 > arr[x, y] >= max_el * 0.16:
                    qimg_zone.setPixelColor(x, y, QColor(0, 190, 255, 255))
                elif max_el * 0.16 > arr[x, y] >= max_el * 0.15:
                    qimg_zone.setPixelColor(x, y, QColor(0, 160, 255, 255))
                elif max_el * 0.15 > arr[x, y] >= max_el * 0.14:
                    qimg_zone.setPixelColor(x, y, QColor(0, 150, 255, 255))
                #     синий
                elif max_el * 0.14 > arr[x, y] >= max_el * 0.13:
                    qimg_zone.setPixelColor(x, y, QColor(0, 130, 255, 255))
                elif max_el * 0.13 > arr[x, y] >= max_el * 0.125:
                    qimg_zone.setPixelColor(x, y, QColor(0, 110, 255, 255))
                elif max_el * 0.125 > arr[x, y] >= max_el * 0.115:
                    qimg_zone.setPixelColor(x, y, QColor(0, 90, 255, 255))
                elif max_el * 0.115 > arr[x, y] >= max_el * 0.11:
                    qimg_zone.setPixelColor(x, y, QColor(0, 70, 255, 255))
                elif max_el * 0.11 > arr[x, y] >= max_el * 0.108:
                    qimg_zone.setPixelColor(x, y, QColor(0, 50, 255, 255))
                elif max_el * 0.108 > arr[x, y] >= max_el * 0.107:
                    qimg_zone.setPixelColor(x, y, QColor(0, 40, 255, 255))
                elif max_el * 0.107 > arr[x, y] >= max_el * 0.106:
                    qimg_zone.setPixelColor(x, y, QColor(0, 30, 255, 255))
                elif max_el * 0.106 > arr[x, y] >= max_el * 0.102:
                    qimg_zone.setPixelColor(x, y, QColor(0, 20, 255, 255))
                elif max_el * 0.102 > arr[x, y] >= max_el * 0.101:
                    qimg_zone.setPixelColor(x, y, QColor(0, 0, 255, 255))
        return qimg_zone


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
