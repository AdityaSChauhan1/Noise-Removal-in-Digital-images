# core/image_editor.py

class ImageEditor:
    def __init__(self):
        pass

    def adjust_brightness(self, image, value):
        """
        Increase or decrease brightness by adding value to each pixel.
        value: int (positive to brighten, negative to darken)
        """
        result = []
        for row in image:
            new_row = [self._clip(pixel + value) for pixel in row]
            result.append(new_row)
        return result

    def adjust_contrast(self, image, factor):
        """
        Adjust contrast around the mid-point (128).
        factor > 1 increases contrast, 0 < factor < 1 reduces contrast.
        """
        result = []
        for row in image:
            new_row = [self._clip(int((pixel - 128) * factor + 128)) for pixel in row]
            result.append(new_row)
        return result

    def adjust_exposure(self, image, gamma=1.0):
        """
        Adjust exposure using gamma correction.
        gamma < 1.0 brightens image, gamma > 1.0 darkens it.
        Output pixel = 255 * (pixel / 255) ^ gamma
        """
        result = []
        for row in image:
            new_row = [self._clip(int(255 * ((pixel / 255) ** gamma))) for pixel in row]
            result.append(new_row)
        return result

    def _clip(self, val):
        return max(0, min(255, int(val)))
