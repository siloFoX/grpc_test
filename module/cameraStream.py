import cv2
import threading

# USB cam supported resolutions : [(640, 480), (320, 240)]

class CameraStream:
    def __init__(self, camera_index=0, width = 640, height = 480) :
        self.cap = cv2.VideoCapture(camera_index)
        if not self.cap.isOpened():
            raise RuntimeError("Failed to open camera.")
        
        print("Current resolution : ", self._set_resolution(width, height))
        
        self.latest_frame = None
        self.lock = threading.Lock()
        self.running = True
        
        # Start the camera read thread
        self.thread = threading.Thread(target=self._update_frame, daemon=True)
        self.thread.start()

    def _update_frame(self):
        """Continuously read frames from the camera."""
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                # Update the latest frame
                with self.lock:
                    self.latest_frame = frame

    def _set_resolution (self, width = 1920, height = 1200) :
        """카메라 해상도를 정의한다. None"""
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        return int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    def get_frame(self):
        """Return the latest frame."""
        with self.lock:
            return self.latest_frame
        
    def get_resolution (self) :
        """카메라 해상도를 출력한다. (int, int)"""
        
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        return width, height

    def release(self):
        """Release the camera resource."""
        self.running = False
        self.thread.join()
        self.cap.release()

    @staticmethod
    def find_supported_resolutions(camera_index=0):
        cap = cv2.VideoCapture(camera_index)
        if not cap.isOpened():
            raise RuntimeError("Failed to open camera.")
        
        supported_resolutions = []
        test_resolutions = [
            (1920, 1080),
            (1280, 720),
            (640, 480),
            (320, 240),
        ]
        
        for width, height in test_resolutions :
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            
            actual_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            actual_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            if (actual_width, actual_height) == (width, height):
                supported_resolutions.append((actual_width, actual_height))
        
        cap.release()
        return supported_resolutions


if __name__ == "__main__" :
    camera = CameraStream()
    camera.release()