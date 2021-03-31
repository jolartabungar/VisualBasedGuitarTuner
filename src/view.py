from PyQt5.QtCore import Qt, QThread, QTimer
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QVBoxLayout, QApplication, QSlider, QHBoxLayout, QLabel
import cv2 as cv
import numpy as np


def create_slider(_range, _slider_on_change):
    slider = QSlider(Qt.Horizontal)
    slider.setRange(_range[0], _range[1])
    slider.setTickPosition(QSlider.TicksBelow)
    slider.setTickInterval(1)
    slider.sliderReleased.connect(_slider_on_change)
    slider.valueChanged.connect(_slider_on_change)
    return slider


class UIWindow(QMainWindow):
    def __init__(self, image=None):
        super().__init__()
        self.image = image
        self.setWindowTitle("Visual Based Guitar Tuner")

        self.central_widget = QWidget()
        self.image_view = QLabel()

        # Sliders
        self.slider_frame = create_slider([1, image.frames_total], self.update_frame)
        self.slider_dilate_iter = create_slider([0, 10], self.update_dilate_iter)
        self.slider_erode_iter = create_slider([0, 10], self.update_erode_iter)
        self.slider_thresh1 = create_slider([0, 500], self.update_thresh1)
        self.slider_thresh2 = create_slider([0, 500], self.update_thresh2)

        self.frame_label = QLabel("Frame: " + str(self.image.frame))
        self.dilate_iter_label = QLabel("Dilate iterations: " + str(self.image.dilate_iteration))
        self.erode_iter_label = QLabel("Erode iterations: " + str(self.image.erode_iteration))
        self.thresh1_label = QLabel("Thresh 1: " + str(self.image.thresh1))
        self.thresh2_label = QLabel("Thresh 2: " + str(self.image.thresh2))

        # Toggle Button
        self.toggle_canny = QPushButton("Toggle Canny/Trained", self)
        self.toggle_canny.setCheckable(True)
        self.toggle_canny.clicked.connect(self.toggle_canny_clicked)

        self.slider_box_frame = QHBoxLayout()
        self.slider_box_frame.addWidget(self.frame_label)
        self.slider_box_frame.addWidget(self.slider_frame)

        self.slider_box_thresh1 = QHBoxLayout()
        self.slider_box_thresh1.addWidget(self.thresh1_label)
        self.slider_box_thresh1.addWidget(self.slider_thresh1)

        self.slider_box_thresh2 = QHBoxLayout()
        self.slider_box_thresh2.addWidget(self.thresh2_label)
        self.slider_box_thresh2.addWidget(self.slider_thresh2)

        self.slider_box_dilate_iter = QHBoxLayout()
        self.slider_box_dilate_iter.addWidget(self.dilate_iter_label)
        self.slider_box_dilate_iter.addWidget(self.slider_dilate_iter)

        self.slider_box_erode_iter = QHBoxLayout()
        self.slider_box_erode_iter.addWidget(self.erode_iter_label)
        self.slider_box_erode_iter.addWidget(self.slider_erode_iter)

        self.edge_detect_controls_box = QHBoxLayout()
        self.edge_detect_sliders_box = QVBoxLayout()
        self.edge_detect_sliders_box.addLayout(self.slider_box_thresh1)
        self.edge_detect_sliders_box.addLayout(self.slider_box_thresh2)
        self.edge_detect_controls_box.addWidget(self.toggle_canny)
        self.edge_detect_controls_box.addLayout(self.edge_detect_sliders_box)

        self.controls_layout = QVBoxLayout()
        self.controls_layout.addLayout(self.slider_box_frame)
        self.controls_layout.addLayout(self.slider_box_dilate_iter)
        self.controls_layout.addLayout(self.slider_box_erode_iter)
        self.controls_layout.addLayout(self.edge_detect_controls_box)

        self.layout = QVBoxLayout(self.central_widget)
        self.layout.addLayout(self.controls_layout)
        self.layout.addWidget(self.image_view)
        self.setCentralWidget(self.central_widget)

        self.update_image()

    def update_frame(self):
        value = self.slider_frame.value()
        self.image.set_frame(value)
        self.frame_label.setText("Frame: " + str(value))
        if not self.slider_frame.isSliderDown():
            self.update_image()

    def update_dilate_iter(self):
        value = self.slider_dilate_iter.value()
        self.image.set_dilate_iteration(value)
        self.dilate_iter_label.setText("Dilate iteration: " + str(value))
        if not self.slider_dilate_iter.isSliderDown():
            self.update_image()

    def update_erode_iter(self):
        value = self.slider_erode_iter.value()
        self.image.set_erode_iteration(value)
        self.erode_iter_label.setText("Erode iteration: " + str(value))
        if not self.slider_erode_iter.isSliderDown():
            self.update_image()

    def update_thresh1(self):
        value = self.slider_thresh1.value()
        self.image.set_thresh1(value)
        self.thresh1_label.setText("Thresh 1: " + str(value))
        if not self.slider_thresh1.isSliderDown():
            self.update_image()

    def update_thresh2(self):
        value = self.slider_thresh2.value()
        self.image.set_thresh2(value)
        self.thresh2_label.setText("Thresh 2: " + str(value))
        if not self.slider_thresh2.isSliderDown():
            self.update_image()

    def toggle_canny_clicked(self):
        if self.toggle_canny.isChecked():
            self.image.use_canny = True
        else:
            self.image.use_canny = False
        self.update_image()

    def update_image(self):
        rgb_image = cv.cvtColor(self.image.get_image(), cv.COLOR_BGR2RGB)
        height, width, channel = rgb_image.shape
        bytes_per_line = 3 * width
        q_img = QImage(rgb_image.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        self.image_view.setPixmap(QPixmap.fromImage(q_img))


if __name__ == '__main__':
    app = QApplication([])
    window = UIWindow()
    window.show()
    app.exit(app.exec_())
