import cv2

class LineTracker(object):
    def __init__(self, cap):
        self._set_resolution(cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.capture = cap
        
        # TODO: use constant names
        self.capture.set(3, 160)
        self.capture.set(4, 120)

    def _set_resolution(self, width, height):
        self.resolution = (int(width), int(height))
        self.roi_w = self.resolution[0]//3
        self.roi_h = self.resolution[1]//2
        self.roi_x = self.resolution[0]//2 - self.roi_w//2
        self.roi_y = self.resolution[1] - self.roi_h
        
        self.roi_x2 = self.roi_x + self.roi_w
        self.roi_y2 = self.roi_y + self.roi_h

    def _get_frame(self):
        ret, frame = self.capture.read()
        if not ret:
            return None
        return frame[self.roi_y:self.roi_y2, self.roi_x:self.roi_x2]

    def __iter__(self):
        return self

    def __next__(self):
        return self.track_line()

    def track_line(self):
        pass
