# core/image_handler.py

import os

class ImageHandler:
    def __init__(self):
        self.image_matrix = []
        self.width = 0
        self.height = 0

    def load_image(self, file_path):
        from PyQt5.QtGui import QImage
        from PyQt5.QtWidgets import QMessageBox

        if not os.path.exists(file_path):
            raise FileNotFoundError("Image not found!")

        image = QImage(file_path)
        if image.isNull():
            raise ValueError("Invalid image format")

        self.width = image.width()
        self.height = image.height()

        self.image_matrix = self.to_grayscale(image)

    def to_grayscale(self, qimage):
        matrix = []
        for y in range(qimage.height()):
            row = []
            for x in range(qimage.width()):
                pixel = qimage.pixel(x, y)
                r = (pixel >> 16) & 0xFF
                g = (pixel >> 8) & 0xFF
                b = pixel & 0xFF
                gray = int((r + g + b) / 3)
                row.append(gray)
            matrix.append(row)
        return matrix

    def get_matrix(self):
        return self.image_matrix

    def from_matrix(self, matrix):
        from PyQt5.QtGui import QImage
        height = len(matrix)
        width = len(matrix[0])
        image = QImage(width, height, QImage.Format_RGB32)
        for y in range(height):
            for x in range(width):
                gray = max(0, min(255, matrix[y][x]))
                color = (gray << 16) + (gray << 8) + gray
                image.setPixel(x, y, color)
        return image
