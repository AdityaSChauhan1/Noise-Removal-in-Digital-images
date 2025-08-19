# import sys
# import os
# import time
# from PyQt5.QtWidgets import (
#     QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
#     QFileDialog, QSlider, QComboBox, QGridLayout, QMessageBox, QSizePolicy
# )
# from PyQt5.QtGui import QPixmap
# from PyQt5.QtCore import Qt

# from image_handler import ImageHandler
# from noise_generator import NoiseGenerator
# from filter_applier import FilterApplier
# from image_editor import ImageEditor


# class GUIApp(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Noise Removal in Images - Python Qt")

#         # Initialize first to avoid AttributeError
#         self.original_matrix = []
#         self.current_matrix = []

#         # Modules
#         self.handler = ImageHandler()
#         self.noiser = NoiseGenerator()
#         self.filterer = FilterApplier()
#         self.editor = ImageEditor()

#         self.init_ui()

#     def init_ui(self):
#         layout = QVBoxLayout()

#         # --- Image Displays ---
#         self.original_label = QLabel("Original Image")
#         self.filtered_label = QLabel("Processed Image")

#         self.original_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
#         self.original_label.setAlignment(Qt.AlignCenter)
#         self.filtered_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
#         self.filtered_label.setAlignment(Qt.AlignCenter)

#         image_box = QHBoxLayout()
#         image_box.addWidget(self.original_label)
#         image_box.addWidget(self.filtered_label)
#         layout.addLayout(image_box)

#         # --- Controls: Load / Save ---
#         button_box = QHBoxLayout()

#         self.upload_btn = QPushButton("Upload")
#         self.save_btn = QPushButton("Save Output")

#         self.upload_btn.clicked.connect(self.load_image)
#         self.save_btn.clicked.connect(self.save_image)

#         button_box.addWidget(self.upload_btn)
#         button_box.addWidget(self.save_btn)
#         layout.addLayout(button_box)

#         # --- Controls: Noise ---
#         noise_box = QHBoxLayout()
#         self.noise_combo = QComboBox()
#         self.noise_combo.addItems(["Gaussian", "Rayleigh", "Erlang", "Exponential", "Uniform", "Impulse"])

#         self.noise_btn = QPushButton("Add Noise")
#         self.noise_btn.clicked.connect(self.apply_noise)

#         noise_box.addWidget(QLabel("Noise:"))
#         noise_box.addWidget(self.noise_combo)
#         noise_box.addWidget(self.noise_btn)
#         layout.addLayout(noise_box)

#         # --- Controls: Filters ---
#         filter_box = QHBoxLayout()
#         self.filter_combo = QComboBox()
#         self.filter_combo.addItems([
#             "Arithmetic Mean", "Geometric Mean", "Harmonic Mean", "Contraharmonic",
#             "Median", "Max", "Min", "Midpoint", "Alpha-Trimmed", "Adaptive Median"
#         ])

#         self.filter_btn = QPushButton("Apply Filter")
#         self.filter_btn.clicked.connect(self.apply_filter)

#         filter_box.addWidget(QLabel("Filter:"))
#         filter_box.addWidget(self.filter_combo)
#         filter_box.addWidget(self.filter_btn)
#         layout.addLayout(filter_box)

#         # --- Controls: Edit ---
#         editor_box = QGridLayout()

#         self.brightness_slider = QSlider(Qt.Horizontal)
#         self.brightness_slider.setRange(-100, 100)
#         self.brightness_slider.setValue(0)

#         self.contrast_slider = QSlider(Qt.Horizontal)
#         self.contrast_slider.setRange(10, 300)
#         self.contrast_slider.setValue(100)

#         self.exposure_slider = QSlider(Qt.Horizontal)
#         self.exposure_slider.setRange(10, 300)
#         self.exposure_slider.setValue(100)

#         editor_box.addWidget(QLabel("Brightness"), 0, 0)
#         editor_box.addWidget(self.brightness_slider, 0, 1)
#         editor_box.addWidget(QLabel("Contrast"), 1, 0)
#         editor_box.addWidget(self.contrast_slider, 1, 1)
#         editor_box.addWidget(QLabel("Exposure"), 2, 0)
#         editor_box.addWidget(self.exposure_slider, 2, 1)

#         self.edit_btn = QPushButton("Apply Editing")
#         self.edit_btn.clicked.connect(self.apply_editing)

#         editor_box.addWidget(self.edit_btn, 3, 0, 1, 2)
#         layout.addLayout(editor_box)

#         self.setLayout(layout)

#     # === Event Override to make images scale ===
#     def resizeEvent(self, event):
#         self.render_images()
#         return super().resizeEvent(event)

#     # === Slot Functions ===

#     def load_image(self):
#         path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.bmp)")
#         if not path:
#             return

#         try:
#             self.handler.load_image(path)
#             self.original_matrix = self.handler.get_matrix()
#             self.current_matrix = [row[:] for row in self.original_matrix]
#             self.render_images()
#         except Exception as e:
#             QMessageBox.critical(self, "Error", str(e))

#     def save_image(self):
#         img = self.handler.from_matrix(self.current_matrix)
#         filename = f"output_{int(time.time())}.png"
#         save_path = os.path.join("assets/saved_outputs", filename)
#         img.save(save_path)
#         QMessageBox.information(self, "Saved", f"Image saved as {filename}")

#     def render_images(self):
#         if not self.original_matrix or not self.current_matrix:
#             return

#         orig = self.handler.from_matrix(self.original_matrix)
#         proc = self.handler.from_matrix(self.current_matrix)

#         label_width = self.original_label.width()
#         label_height = self.original_label.height()

#         self.original_label.setPixmap(QPixmap.fromImage(orig).scaled(label_width, label_height, Qt.KeepAspectRatio))
#         self.filtered_label.setPixmap(QPixmap.fromImage(proc).scaled(label_width, label_height, Qt.KeepAspectRatio))

#     def apply_noise(self):
#         name = self.noise_combo.currentText()
#         if name == "Gaussian":
#             self.current_matrix = self.noiser.add_gaussian(self.current_matrix)
#         elif name == "Rayleigh":
#             self.current_matrix = self.noiser.add_rayleigh(self.current_matrix)
#         elif name == "Erlang":
#             self.current_matrix = self.noiser.add_erlang(self.current_matrix)
#         elif name == "Exponential":
#             self.current_matrix = self.noiser.add_exponential(self.current_matrix)
#         elif name == "Uniform":
#             self.current_matrix = self.noiser.add_uniform(self.current_matrix)
#         elif name == "Impulse":
#             self.current_matrix = self.noiser.add_impulse(self.current_matrix)
#         self.render_images()

#     def apply_filter(self):
#         name = self.filter_combo.currentText()
#         if name == "Arithmetic Mean":
#             self.current_matrix = self.filterer.arithmetic_mean(self.current_matrix)
#         elif name == "Geometric Mean":
#             self.current_matrix = self.filterer.geometric_mean(self.current_matrix)
#         elif name == "Harmonic Mean":
#             self.current_matrix = self.filterer.harmonic_mean(self.current_matrix)
#         elif name == "Contraharmonic":
#             self.current_matrix = self.filterer.contraharmonic(self.current_matrix, Q=1.5)
#         elif name == "Median":
#             self.current_matrix = self.filterer.median_filter(self.current_matrix)
#         elif name == "Max":
#             self.current_matrix = self.filterer.max_filter(self.current_matrix)
#         elif name == "Min":
#             self.current_matrix = self.filterer.min_filter(self.current_matrix)
#         elif name == "Midpoint":
#             self.current_matrix = self.filterer.midpoint_filter(self.current_matrix)
#         elif name == "Alpha-Trimmed":
#             self.current_matrix = self.filterer.alpha_trimmed(self.current_matrix, d=2)
#         elif name == "Adaptive Median":
#             self.current_matrix = self.filterer.adaptive_median(self.current_matrix)
#         self.render_images()

#     def apply_editing(self):
#         brightness = self.brightness_slider.value()
#         contrast = self.contrast_slider.value() / 100.0
#         exposure = self.exposure_slider.value() / 100.0

#         edited = self.editor.adjust_brightness(self.current_matrix, brightness)
#         edited = self.editor.adjust_contrast(edited, contrast)
#         edited = self.editor.adjust_exposure(edited, exposure)

#         self.current_matrix = edited
#         self.render_images()


# gui/main_window.py
import sys
import os
import time
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFileDialog, QSlider, QComboBox, QGridLayout, QMessageBox, QSizePolicy,
    QGroupBox, QScrollArea
)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

from image_handler import ImageHandler
from noise_generator import NoiseGenerator
from filter_applier import FilterApplier
from image_editor import ImageEditor
from histogram_visualizer import HistogramVisualizer


class GUIApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Processing Tool")
        self.setMinimumSize(800, 800)

        # Initialize image matrices
        self.original_matrix = []
        self.current_matrix = []
        self.backup_matrix = []

        # Modules
        self.handler = ImageHandler()
        self.noiser = NoiseGenerator()
        self.filterer = FilterApplier()
        self.editor = ImageEditor()

        self.init_ui()
        self.setStyleSheet("""
            QPushButton {
                font-size: 12px;
                min-width: 80px;
                max-width: 120px;
                padding: 5px;
            }
            QLabel {
                font-size: 12px;
            }
            QComboBox {
                font-size: 12px;
            }
            QSlider {
                min-height: 30px;
            }
        """)

    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout()
        
        # Scroll area for the content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)

        # --- Image Displays ---
        image_box = QHBoxLayout()
        
        # Original image group
        orig_group = QGroupBox("Original Image")
        orig_layout = QVBoxLayout()
        self.original_label = QLabel()
        self.original_label.setAlignment(Qt.AlignCenter)
        self.original_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.original_histogram = HistogramVisualizer()
        orig_layout.addWidget(self.original_label)
        orig_layout.addWidget(self.original_histogram.get_widget())
        orig_group.setLayout(orig_layout)
        
        # Processed image group
        proc_group = QGroupBox("Processed Image")
        proc_layout = QVBoxLayout()
        self.filtered_label = QLabel()
        self.filtered_label.setAlignment(Qt.AlignCenter)
        self.filtered_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.filtered_histogram = HistogramVisualizer()
        proc_layout.addWidget(self.filtered_label)
        proc_layout.addWidget(self.filtered_histogram.get_widget())
        proc_group.setLayout(proc_layout)
        
        image_box.addWidget(orig_group)
        image_box.addWidget(proc_group)
        layout.addLayout(image_box)

        # --- Controls: Load / Save / Clear ---
        control_box = QHBoxLayout()
        
        self.upload_btn = QPushButton("Upload Image")
        self.save_btn = QPushButton("Save Image")
        self.clear_btn = QPushButton("Reset Image")
        
        self.upload_btn.clicked.connect(self.load_image)
        self.save_btn.clicked.connect(self.save_image)
        self.clear_btn.clicked.connect(self.reset_image)
        
        control_box.addWidget(self.upload_btn)
        control_box.addWidget(self.save_btn)
        control_box.addWidget(self.clear_btn)
        layout.addLayout(control_box)

        # --- Controls: Noise ---
        noise_group = QGroupBox("Add Noise")
        noise_layout = QHBoxLayout()
        
        self.noise_combo = QComboBox()
        self.noise_combo.addItems(["Gaussian", "Rayleigh", "Erlang", "Exponential", "Uniform", "Impulse"])
        
        self.noise_btn = QPushButton("Add Noise")
        self.noise_btn.clicked.connect(self.apply_noise)
        
        noise_layout.addWidget(QLabel("Noise Type:"))
        noise_layout.addWidget(self.noise_combo)
        noise_layout.addWidget(self.noise_btn)
        noise_group.setLayout(noise_layout)
        layout.addWidget(noise_group)

        # --- Controls: Filters ---
        filter_group = QGroupBox("Apply Filter")
        filter_layout = QHBoxLayout()
        
        self.filter_combo = QComboBox()
        self.filter_combo.addItems([
            "Arithmetic Mean", "Geometric Mean", "Harmonic Mean", "Contraharmonic",
            "Median", "Max", "Min", "Midpoint", "Alpha-Trimmed", "Adaptive Median"
        ])
        
        self.filter_btn = QPushButton("Apply Filter")
        self.filter_btn.clicked.connect(self.apply_filter)
        
        filter_layout.addWidget(QLabel("Filter Type:"))
        filter_layout.addWidget(self.filter_combo)
        filter_layout.addWidget(self.filter_btn)
        filter_group.setLayout(filter_layout)
        layout.addWidget(filter_group)

        # --- Controls: Edit ---
        edit_group = QGroupBox("Image Adjustments")
        edit_layout = QGridLayout()
        
        # Brightness slider
        self.brightness_slider = QSlider(Qt.Horizontal)
        self.brightness_slider.setRange(-100, 100)
        self.brightness_slider.setValue(0)
        self.brightness_slider.setTickPosition(QSlider.TicksBelow)
        self.brightness_slider.setTickInterval(20)
        self.brightness_value = QLabel("0")
        self.brightness_value.setAlignment(Qt.AlignCenter)
        
        # Contrast slider
        self.contrast_slider = QSlider(Qt.Horizontal)
        self.contrast_slider.setRange(10, 300)
        self.contrast_slider.setValue(100)
        self.contrast_slider.setTickPosition(QSlider.TicksBelow)
        self.contrast_slider.setTickInterval(20)
        self.contrast_value = QLabel("1.0")
        self.contrast_value.setAlignment(Qt.AlignCenter)
        
        # Exposure slider
        self.exposure_slider = QSlider(Qt.Horizontal)
        self.exposure_slider.setRange(10, 300)
        self.exposure_slider.setValue(100)
        self.exposure_slider.setTickPosition(QSlider.TicksBelow)
        self.exposure_slider.setTickInterval(20)
        self.exposure_value = QLabel("1.0")
        self.exposure_value.setAlignment(Qt.AlignCenter)
        
        # Apply button
        self.edit_btn = QPushButton("Apply Adjustments")
        self.edit_btn.clicked.connect(self.apply_editing)
        
        # Connect slider signals
        self.brightness_slider.valueChanged.connect(self.update_brightness_value)
        self.contrast_slider.valueChanged.connect(self.update_contrast_value)
        self.exposure_slider.valueChanged.connect(self.update_exposure_value)
        
        # Add to layout
        edit_layout.addWidget(QLabel("Brightness:"), 0, 0)
        edit_layout.addWidget(self.brightness_slider, 0, 1)
        edit_layout.addWidget(self.brightness_value, 0, 2)
        
        edit_layout.addWidget(QLabel("Contrast:"), 1, 0)
        edit_layout.addWidget(self.contrast_slider, 1, 1)
        edit_layout.addWidget(self.contrast_value, 1, 2)
        
        edit_layout.addWidget(QLabel("Exposure:"), 2, 0)
        edit_layout.addWidget(self.exposure_slider, 2, 1)
        edit_layout.addWidget(self.exposure_value, 2, 2)
        
        edit_layout.addWidget(self.edit_btn, 3, 0, 1, 3)
        edit_group.setLayout(edit_layout)
        layout.addWidget(edit_group)

        # Set the scroll area content
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)

    # === Slider Value Updates ===
    def update_brightness_value(self, value):
        self.brightness_value.setText(str(value))

    def update_contrast_value(self, value):
        self.contrast_value.setText(f"{value/100:.2f}")

    def update_exposure_value(self, value):
        self.exposure_value.setText(f"{value/100:.2f}")

    # === Image Operations ===
    def load_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.bmp)")
        if not path:
            return

        try:
            self.handler.load_image(path)
            self.original_matrix = self.handler.get_matrix()
            self.current_matrix = [row[:] for row in self.original_matrix]
            self.backup_matrix = [row[:] for row in self.original_matrix]
            self.render_images()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def save_image(self):
        if not self.current_matrix:
            QMessageBox.warning(self, "Warning", "No image to save! Please upload an image first.")
            return

        # Ensure the directory exists
        os.makedirs("assets/saved_outputs", exist_ok=True)
        
        try:
            img = self.handler.from_matrix(self.current_matrix)
            filename = f"output_{int(time.time())}.png"
            save_path = os.path.join("assets/saved_outputs", filename)
            img.save(save_path)
            QMessageBox.information(self, "Saved", f"Image saved as {filename} in assets/saved_outputs")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save image: {str(e)}")

    def reset_image(self):
        if not self.original_matrix:
            QMessageBox.warning(self, "Warning", "No original image to reset to!")
            return
            
        self.current_matrix = [row[:] for row in self.original_matrix]
        # Reset sliders
        self.brightness_slider.setValue(0)
        self.contrast_slider.setValue(100)
        self.exposure_slider.setValue(100)
        self.render_images()

    def render_images(self):
        if not self.current_matrix:
            return

        orig = self.handler.from_matrix(self.original_matrix)
        proc = self.handler.from_matrix(self.current_matrix)

        # Calculate display size based on window size
        display_width = min(self.width() // 2 - 20, 500)
        display_height = min(self.height() // 2 - 20, 500)

        self.original_label.setPixmap(QPixmap.fromImage(orig).scaled(
            display_width, display_height, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.filtered_label.setPixmap(QPixmap.fromImage(proc).scaled(
            display_width, display_height, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        
        # Update histograms
        self.original_histogram.update_histogram(self.original_matrix)
        self.filtered_histogram.update_histogram(self.current_matrix)

    def apply_noise(self):
        if not self.current_matrix:
            QMessageBox.warning(self, "Warning", "Please upload an image first!")
            return

        name = self.noise_combo.currentText()
        try:
            if name == "Gaussian":
                self.current_matrix = self.noiser.add_gaussian(self.current_matrix)
            elif name == "Rayleigh":
                self.current_matrix = self.noiser.add_rayleigh(self.current_matrix)
            elif name == "Erlang":
                self.current_matrix = self.noiser.add_erlang(self.current_matrix)
            elif name == "Exponential":
                self.current_matrix = self.noiser.add_exponential(self.current_matrix)
            elif name == "Uniform":
                self.current_matrix = self.noiser.add_uniform(self.current_matrix)
            elif name == "Impulse":
                self.current_matrix = self.noiser.add_impulse(self.current_matrix)
            
            self.render_images()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to apply noise: {str(e)}")

    def apply_filter(self):
        if not self.current_matrix:
            QMessageBox.warning(self, "Warning", "Please upload an image first!")
            return

        name = self.filter_combo.currentText()
        try:
            if name == "Arithmetic Mean":
                self.current_matrix = self.filterer.arithmetic_mean(self.current_matrix)
            elif name == "Geometric Mean":
                self.current_matrix = self.filterer.geometric_mean(self.current_matrix)
            elif name == "Harmonic Mean":
                self.current_matrix = self.filterer.harmonic_mean(self.current_matrix)
            elif name == "Contraharmonic":
                self.current_matrix = self.filterer.contraharmonic(self.current_matrix, Q=1.5)
            elif name == "Median":
                self.current_matrix = self.filterer.median_filter(self.current_matrix)
            elif name == "Max":
                self.current_matrix = self.filterer.max_filter(self.current_matrix)
            elif name == "Min":
                self.current_matrix = self.filterer.min_filter(self.current_matrix)
            elif name == "Midpoint":
                self.current_matrix = self.filterer.midpoint_filter(self.current_matrix)
            elif name == "Alpha-Trimmed":
                self.current_matrix = self.filterer.alpha_trimmed(self.current_matrix, d=2)
            elif name == "Adaptive Median":
                self.current_matrix = self.filterer.adaptive_median(self.current_matrix)
            
            self.render_images()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to apply filter: {str(e)}")

    def apply_editing(self):
        if not self.current_matrix:
            QMessageBox.warning(self, "Warning", "Please upload an image first!")
            return

        brightness = self.brightness_slider.value()
        contrast = self.contrast_slider.value() / 100.0
        exposure = self.exposure_slider.value() / 100.0

        try:
            edited = self.editor.adjust_brightness(self.current_matrix, brightness)
            edited = self.editor.adjust_contrast(edited, contrast)
            edited = self.editor.adjust_exposure(edited, exposure)
            self.current_matrix = edited
            self.render_images()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to apply adjustments: {str(e)}")

    # === Event Handling ===
    def resizeEvent(self, event):
        self.render_images()
        return super().resizeEvent(event)