import cv2

class LineTracker(object):
    def __init__(self, cam):
        width, height = cam.resolution()
        self._set_resolution(width, height)

        self._capture = cam
        self._preview = False

    def _set_resolution(self, width, height):
        self.resolution = (int(width), int(height))
        self.roi_w = self.resolution[0]//3
        self.roi_h = self.resolution[1]//2
        self.roi_x = self.resolution[0]//2 - self.roi_w//2
        self.roi_y = self.resolution[1] - self.roi_h
        
        self.roi_x2 = self.roi_x + self.roi_w
        self.roi_y2 = self.roi_y + self.roi_h

    def _get_frame(self):
        frame = self._capture.read()
        if frame is None:
            return None
        return frame[self.roi_y:self.roi_y2, self.roi_x:self.roi_x2]

    def __iter__(self):
        return self

    def __next__(self):
        return self.track_line()

    def preview(self, active: bool):
        self._preview = active

    def track_line(self):
        pass
