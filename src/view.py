from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QVBoxLayout, \
    QApplication, QSlider, QHBoxLayout, QLabel, QFileDialog, QComboBox
import tuning_constants as tuning
import pyqtgraph as pg
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

        self.setMinimumHeight(1000)
        self.setMinimumWidth(1000)

        self.central_widget = QWidget()
        self.image_view = pg.ImageView()
        self.image_view.roi.setSize([100, 800])
        self.image_view.roi.setPos([0, 0])

        # Video Selection & Controls
        self.slider_frame = create_slider([1, image.frames_total], self.update_frame)
        self.frame_label = QLabel("Frame: " + str(self.image.frame))

        self.toggle_image = QPushButton("Toggle Original/Processed", self)
        self.toggle_image.setCheckable(True)
        self.toggle_image.clicked.connect(self.toggle_image_clicked)

        self.select_video_button = QPushButton("Select Video", self)
        self.select_video_button.clicked.connect(self.open_filename_dialog)

        # Tuning Selection Drop-down
        self.tuning_set_dropdown_label = QLabel("Select tuning set: ")
        self.tuning_string_dropdown_label = QLabel("Select selected string: ")

        self.select_tuning = QComboBox()
        self.select_tuning.addItem(tuning.BASS_STD)
        self.select_tuning.addItem(tuning.BASS_5_STR_STD)
        self.select_tuning.addItem(tuning.GUITAR_STD)
        self.select_tuning.currentIndexChanged.connect(self.update_string_options)

        self.select_string = QComboBox()
        self.update_string_options(0)

        # Tuning Analysis Results
        self.analyzed_tuning_label = QLabel("Approximate tuning of string: " + str(self.image.detected_tuning()))

        # Set Bounding Box
        self.set_bounding_box_button = QPushButton("Set string region")
        self.set_bounding_box_button.clicked.connect(self.set_bounding_box)

        # Start tuning detection
        self.start_tuning_detection_button = QPushButton("Start tuning detection")
        self.start_tuning_detection_button.clicked.connect(self.start_tuning_detection)

        # Add widgets to layout
        self.tuning_selection_box = QHBoxLayout()
        self.tuning_selection_box.addWidget(self.tuning_set_dropdown_label)
        self.tuning_selection_box.addWidget(self.select_tuning)
        self.tuning_selection_box.addWidget(self.tuning_string_dropdown_label)
        self.tuning_selection_box.addWidget(self.select_string)
        self.tuning_selection_box.addWidget(self.analyzed_tuning_label)
        self.tuning_selection_box.addStretch()
        self.tuning_selection_box.addWidget(self.set_bounding_box_button)
        self.tuning_selection_box.addWidget(self.start_tuning_detection_button)

        self.slider_box_frame = QHBoxLayout()
        self.slider_box_frame.addWidget(self.select_video_button)
        self.slider_box_frame.addWidget(self.toggle_image)
        self.slider_box_frame.addWidget(self.frame_label)
        self.slider_box_frame.addWidget(self.slider_frame)

        self.controls_layout = QVBoxLayout()
        self.controls_layout.addLayout(self.slider_box_frame)
        self.controls_layout.addLayout(self.tuning_selection_box)

        self.tuning_options_layout = QHBoxLayout()

        # Add all layouts to main window
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.addLayout(self.controls_layout)
        self.layout.addWidget(self.image_view)
        self.setCentralWidget(self.central_widget)

        self.update_image()

    def open_filename_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(self,
                                                  "QFileDialog.getOpenFileName()", "../data",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if filename:
            self.image.set_video_path(filename)
            self.update_image()

    def toggle_image_clicked(self):
        if self.toggle_image.isChecked():
            self.image.show_processed = False
        else:
            self.image.show_processed = True
        self.update_image()

    def update_frame(self):
        value = self.slider_frame.value()
        self.image.set_frame(value)
        self.frame_label.setText("Frame: " + str(value))
        if not self.slider_frame.isSliderDown():
            self.update_image()

    def update_string_options(self, tuning_index):
        tuning_set = self.select_tuning.itemText(tuning_index)
        self.select_string.clear()
        self.select_string.addItems(tuning.tuning_map(tuning_set))
        self.select_string.currentIndexChanged.connect(self.update_selected_string)

    def update_selected_string(self, string_index):
        self.image.set_selected_string(self.select_string.itemText(string_index))
        self.analyzed_tuning_label.setText("Approximate tuning of string: " + str(self.image.detected_tuning()))

    def set_bounding_box(self):
        pos = self.image_view.roi.pos()
        size = self.image_view.roi.size()
        p1 = pos
        p2 = pos + size
        bounding_box = [p1, p2]
        self.image.set_bounding_box(bounding_box)

    def start_tuning_detection(self):
        self.image.start_tuning_detection()

    def update_image(self):
        rgb_image = cv.cvtColor(self.image.get_image(), cv.COLOR_BGR2RGB)
        self.image_view.setImage(np.rot90(np.fliplr(rgb_image)))


if __name__ == '__main__':
    app = QApplication([])
    window = UIWindow()
    window.show()
    app.exit(app.exec_())
