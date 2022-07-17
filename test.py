import sys
from PySide2.QtGui import QPixmap, QImage
from PySide2.QtWidgets import QMainWindow, QApplication, QLabel, QHBoxLayout, QPushButton, QWidget
import numpy as np

# 1. Случайные числа в матрице N на M
N = 5
M = 5
data = np.random.random((N, M))
bins = np.array([0.00, 0.10, 0.15, 0.25, 0.30, 0.40, 0.6, 0.8, 0.95])
palette = np.array([[0, 30, 255], [0, 80, 255], [0, 100, 255],
                    [0, 255, 255], [20, 255, 255], [100, 100, 255],
                    [200, 50, 255], [255, 255, 100], [255, 255, 0]],  dtype='uint8')


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
        print(im)
        h, w, _ = im.shape
        heat_map = QPixmap(QImage(im, w, h, 3 * w, QImage.Format_RGB888))
        heat_map.save('test_output.png')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
