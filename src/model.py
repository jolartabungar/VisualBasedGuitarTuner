import cv2 as cv
import numpy as np
import tuning_constants as tuning
import tuner_comparison as tuner
from skimage.metrics import structural_similarity as ssim


class Image:
    def __init__(self):
        self.video_path = None
        self.cap = None
        self.frame = 1
        self.frames_total = 0
        self.video_height = 0
        self.video_width = 0

        self.set_video_path("../data/bass_tuned_1.mp4")
        self.edge_detector_model = cv.ximgproc.createStructuredEdgeDetection('../detection_model/model.yml')

        self.show_processed = False
        self.bounding_box = None
        self.selected_string = tuning.STRING_E

        self.tuning_detection_active = False
        self.initial_tuning_frame = None
        self.initial_frame_index = 0
        self.final_frame_index = 0
        self.oscillation_cycle_complete = False

    def set_frame(self, value):
        self.frame = value

    def set_video_path(self, path):
        self.video_path = path
        self.cap = cv.VideoCapture(self.video_path)

        # Set capture to camera if video not found
        if self.cap.get(7) == 0.0:
            self.cap = cv.VideoCapture(0)

        _flag, image = self.cap.read()
        self.video_height, self.video_width, channels = image.shape

        self.frames_total = int(self.cap.get(7) - 1)

    def set_bounding_box(self, box):
        # Correct box coordinates if out of bounds
        p1, p2 = box

        if int(p1.x()) < 0:
            p1[0] = 0
        if int(p1.y()) < 0:
            p1[1] = 0
        if int(p2.x()) >= self.video_width:
            p2[0] = self.video_width - 1
        if int(p2.y()) >= self.video_height:
            p2[1] = self.video_height - 1

        self.bounding_box = [p1, p2]
        print(self.bounding_box)

        self.tuning_detection_active = False

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
        if s > 0.8:
            return True
        return False

    def calculate_frequency(self):
        # Assume video is recorded with 30 FPS
        period = abs(self.final_frame_index - self.initial_frame_index) / 30
        print('Period: ' + str(period))
        frequency = tuner.calculate_frequency_period(period)
        print('Frequency: ' + str(frequency))
        return frequency

    def detected_tuning(self):
        if self.tuning_detection_active:
            if self.oscillation_cycle_complete:
                return tuner.tune_bass(self.calculate_frequency())
            return 'Tuning in progress...'

        return 'Not currently tuning'

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
            if self.frame != self.initial_frame_index:
                self.oscillation_cycle_complete = self.compare_frames(self.retrieve_cropped_frame(img))

        return self.isolate_strings(img) if self.show_processed else img
