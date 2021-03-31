import cv2 as cv
import numpy as np


class Image:
    def __init__(self):
        self.cap = cv.VideoCapture("../data/vid1.mp4")
        self.edge_detector_model = cv.ximgproc.createStructuredEdgeDetection('../detection_model/model.yml')
        self.frames_total = int(self.cap.get(7) - 1)

        self.frame = 1
        self.dilate_iteration = 0
        self.erode_iteration = 0
        self.thresh1 = 0
        self.thresh2 = 0

        self.use_canny = False

    def set_frame(self, value):
        self.frame = value

    def set_dilate_iteration(self, value):
        self.dilate_iteration = value

    def set_erode_iteration(self, value):
        self.erode_iteration = value

    def set_thresh1(self, value):
        self.thresh1 = value

    def set_thresh2(self, value):
        self.thresh2 = value

    def edge_detect_canny(self, image):
        # gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        # _, thresh = cv.threshold(gray_image, 30, 255, cv.THRESH_BINARY)

        # kernel_sharpen = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
        # morph = cv.morphologyEx(image, cv.MORPH_OPEN, kernel_sharpen)
        #
        # result_morph = morph.copy()
        # contours = cv.findContours(morph, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        # contours = contours[0] if len(contours) == 2 else contours[1]
        # for c in contours:
        #     area = cv.contourArea(c)
        #     if area < 100:
        #         cv.drawContours(result_morph, [c], 0, (0, 0, 0), -1)

        result_canny = cv.Canny(image, self.thresh1, self.thresh2, apertureSize=3, L2gradient=False)
        return result_canny

    def edge_detect_trained(self, image):
        rgb_image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        float32_image = rgb_image.astype(np.float32) / 255.0
        edges = self.edge_detector_model.detectEdges(float32_image) * 255.0
        return np.clip(edges, 0, 255).astype(np.uint8)

    def remove_salt_pepper_noise(self, image):
        src = image.copy()
        count = 0
        last_median = src
        median = cv.medianBlur(src, 3)

        while not np.array_equal(last_median, median):
            zeroed = np.invert(np.logical_and(median, src))
            src[zeroed] = 0
            count = count + 1
            if count > 70:
                break

            last_median = median
            median = cv.medianBlur(src, 3)

        return src
    
    def find_significant_contours(self, image):
        contours, hierarchy = cv.findContours(
            image,
            cv.RETR_TREE,
            cv.CHAIN_APPROX_SIMPLE
        )

        contours_to_draw = contours

        if hierarchy is not None:
            lvl_1_contours = []
            for contour_index, _tuple in enumerate(hierarchy[0]):
                if _tuple[3] != -1:
                    _tuple = np.insert(_tuple.copy(), 0, [contour_index])
                    lvl_1_contours.append(_tuple)
                
            contours_with_area = []
            for _tuple in lvl_1_contours:
                contour_index = _tuple[0]
                contour = contours[contour_index]
                area = cv.contourArea(contour)
                contours_with_area.append(contour)

            contours_to_draw = contours_with_area

        result_contours = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)
        for i in range(len(contours_to_draw)):
            cv.drawContours(result_contours, contours_to_draw, i, (255, 255, 255), 2, cv.LINE_AA, maxLevel=1)
        
        return result_contours

    def isolate_strings(self, original_image):
        gray_image = cv.cvtColor(original_image, cv.COLOR_BGR2GRAY)
        result_gaussian_blur = cv.GaussianBlur(original_image, (5, 5), 0)

        result_edge = self.edge_detect_canny(result_gaussian_blur) \
            if self.use_canny else self.edge_detect_trained(result_gaussian_blur)

        # Kernel for erode/dilate
        kernel_erode_dilate = np.ones((2, 2), np.uint8)

        result_erode_dilate = result_edge
        if self.dilate_iteration != 0:
            result_erode_dilate = cv.dilate(result_erode_dilate, kernel_erode_dilate, iterations=self.dilate_iteration)

        if self.erode_iteration != 0:
            result_erode_dilate = cv.erode(result_erode_dilate, kernel_erode_dilate, iterations=self.erode_iteration)

        result_contours = self.find_significant_contours(result_erode_dilate)

        return result_erode_dilate

    def get_image(self):
        self.cap.set(1, self.frame)
        _flag, img = self.cap.read()
        img = cv.resize(img[600:1920, 0:1080], (1056, 594))

        return self.isolate_strings(img)
