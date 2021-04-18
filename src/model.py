import cv2 as cv
import numpy as np
import tuning_constants as tuning
from skimage.metrics import structural_similarity as ssim


class Image:
    def __init__(self):
        self.video_path = None
        self.cap = None
        self.frame = 1
        self.frames_total = 0

        self.set_video_path("../data/bass_tuned_1.mp4")
        self.edge_detector_model = cv.ximgproc.createStructuredEdgeDetection('../detection_model/model.yml')

        self.show_processed = False
        self.bounding_box = None
        self.selected_string = tuning.STRING_E

        self.tuning_detection_active = False
        self.initial_tuning_frame = None

    def set_frame(self, value):
        self.frame = value

    def set_video_path(self, path):
        self.video_path = path
        self.cap = cv.VideoCapture(self.video_path)
        self.frames_total = int(self.cap.get(7) - 1)

    def set_bounding_box(self, box):
        self.bounding_box = box
        print(self.bounding_box)

    def set_selected_string(self, string):
        self.selected_string = string

    def start_tuning_detection(self):
        if self.bounding_box is not None:
            self.tuning_detection_active = False
            self.initial_tuning_frame = self.retrieve_cropped_frame(self.get_image())
            self.tuning_detection_active = True
        else:
            print("ERROR: No bounding box found!")

    def retrieve_cropped_frame(self, img):
        p1, p2 = self.bounding_box
        cropped = img[int(p1.y()):int(p2.y()), int(p1.x()):int(p2.x())]
        return cropped

    def compare_frames(self, curr_frame):
        initial = cv.cvtColor(self.initial_tuning_frame, cv.COLOR_BGR2GRAY)
        curr = cv.cvtColor(curr_frame, cv.COLOR_BGR2GRAY)

        s = ssim(initial, curr)
        print(s)

    def detected_tuning(self):
        return '> ' + self.selected_string

    def edge_detect_trained(self, image):
        rgb_image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        float32_image = rgb_image.astype(np.float32) / 255.0
        edges = self.edge_detector_model.detectEdges(float32_image) * 255.0

        return np.clip(edges, 0, 255).astype(np.uint8)

    def isolate_strings(self, original_image):
        result_gaussian_blur = cv.GaussianBlur(original_image, (5, 5), 0)
        result_edge = self.edge_detect_trained(result_gaussian_blur)

        return result_edge

    def get_image(self):
        self.cap.set(1, self.frame)
        _flag, img = self.cap.read()
        # img = cv.resize(img[600:1920, 0:1080], (1056, 594))

        if self.tuning_detection_active:
            self.compare_frames(self.retrieve_cropped_frame(img))

        return self.isolate_strings(img) if self.show_processed else img
