import sys
from PySide2.QtGui import QPixmap, QImage
from PySide2.QtWidgets import QMainWindow, QApplication, QLabel, QHBoxLayout, QPushButton, QWidget
import numpy as np

# 1. Случайные числа в матрице N на M
N = 500
M = 200
data = np.random.random((N, M))
bins = np.array([0.15, 0.17, 0.19,  # темно голубой
                 0.2, 0.21, 0.22,
                 0.245, 0.3, 0.35,  # голубой
                 0.36, 0.39, 0.4,  # зеленый
                 0.425, 0.435, 0.445,  # салотовый
                 0.455, 0.465, 0.475,
                 0.5, 0.55, 0.6,  # желтый
                 0.63, 0.66, 0.7,
                 0.8, 0.85, 0.9,  # рыжий
                 0.91, 0.95, 0.99])  # красный
palette = np.array([[0, 150, 255, 255], [0, 160, 255, 255], [0, 190, 255, 255],  # темно голубой
                    [0, 255, 150, 255], [0, 255, 120, 255], [0, 255, 100, 255],
                    [0, 255, 80, 255], [0, 255, 60, 255], [0, 255, 40, 255],  # голубой
                    [0, 255, 0, 255], [70, 255, 0, 255], [130, 255, 0, 255],  # зеленый
                    [150, 255, 0, 255], [180, 255, 0, 255], [200, 255, 0, 255],  # салотовый
                    [220, 255, 0, 255], [230, 255, 0, 255], [240, 255, 0, 255],
                    [255, 255, 0, 255], [255, 230, 0, 255], [255, 210, 0, 255],  # желтый
                    [255, 200, 0, 255], [255, 190, 0, 255], [255, 170, 0, 255],
                    [255, 150, 0, 255], [255, 120, 0, 255], [255, 80, 0, 255],  # рыжий
                    [255, 60, 0, 255], [255, 30, 0, 255], [255, 0, 0, 255]], dtype='uint8')
palette[:, [0, 2]] = palette[:, [2, 0]]  # swap channel for Format_ARGB32


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
        digitize = np.digitize(data, bins, right=True)
        digitize = np.expand_dims(digitize, axis=2)
        im = np.choose(digitize, palette, mode='clip')
        h, w, _ = im.shape
        # heat_map = QPixmap(QImage(im, w, h, 4 * w, QImage.Format_ARGB32))
        heat_map = QImage(im, w, h, 4 * w, QImage.Format_ARGB32)
        heat_map.save('test_output.png')


if __name__ == '__main__':
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec_()
    sys.exit()
