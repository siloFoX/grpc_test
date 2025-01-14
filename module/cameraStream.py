import cv2
import threading

class CameraStream:
    def __init__(self, camera_index=0):
        self.cap = cv2.VideoCapture(camera_index)
        if not self.cap.isOpened():
            raise RuntimeError("Failed to open camera.")
        
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

    def get_frame(self):
        """Return the latest frame."""
        with self.lock:
            return self.latest_frame

    def release(self):
        """Release the camera resource."""
        self.running = False
        self.thread.join()
        self.cap.release()
