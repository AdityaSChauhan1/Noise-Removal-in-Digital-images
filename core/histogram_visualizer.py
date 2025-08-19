# core/histogram_visualizer.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGraphicsScene, QGraphicsView
from PyQt5.QtGui import QPixmap, QImage, QPainter, QColor
from PyQt5.QtCore import Qt

class HistogramVisualizer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.label = QLabel("Histogram")
        self.graphics_view = QGraphicsView()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.graphics_view)
        self.setLayout(self.layout)

    def compute_histogram(self, image_matrix):
        histogram = [0] * 256
        for row in image_matrix:
            for pixel in row:
                histogram[pixel] += 1
        return histogram

    def normalize_histogram(self, histogram, height):
        max_freq = max(histogram)
        if max_freq == 0:
            return [0] * 256
        scale = height / max_freq
        return [int(val * scale) for val in histogram]

    def draw_histogram_gui(self, histogram, height=100, width=256):
        normalized = self.normalize_histogram(histogram, height)
        image = QImage(width, height, QImage.Format_RGB32)
        image.fill(Qt.white)
        painter = QPainter(image)
        painter.setPen(Qt.black)
        for x in range(len(normalized)):
            y = height - normalized[x]
            painter.drawLine(x, height, x, y)
        painter.end()
        pixmap = QPixmap.fromImage(image)
        scene = QGraphicsScene()
        scene.addPixmap(pixmap)
        self.graphics_view.setScene(scene)
        self.graphics_view.fitInView(scene.sceneRect(), Qt.KeepAspectRatio)

    def update_histogram(self, image_matrix):
        if image_matrix and all(isinstance(row, list) for row in image_matrix):
            histogram = self.compute_histogram(image_matrix)
            self.draw_histogram_gui(histogram)

    def get_widget(self):
        return self
