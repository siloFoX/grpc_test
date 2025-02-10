import cv2
import threading

class URLStream :
    def __init__(self, url):
        self.url = url
        self.cap = cv2.VideoCapture(url)  # OpenCV VideoCapture로 MJPEG 스트림 열기
        if not self.cap.isOpened() :
            raise RuntimeError(f"Failed to connect to MJPEG stream: {url}")
        
        self.latest_frame = None
        self.lock = threading.Lock()
        self.running = True

        # Start the stream reading thread
        self.thread = threading.Thread(target=self._update_frame, daemon=True)
        self.thread.start()

    def _update_frame(self):
        """Continuously read frames from the MJPEG stream."""
        while self.running:
            ret, frame = self.cap.read()  # MJPEG 스트림에서 프레임 읽기
            if ret:
                with self.lock:
                    self.latest_frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
            else:
                print("Failed to read frame from MJPEG stream.")
                break

    def get_frame(self):
        """Return the latest frame."""
        with self.lock:
            return self.latest_frame

    def release(self):
        """Stop the stream and release resources."""
        self.running = False
        self.thread.join()
        self.cap.release()

if __name__ == "__main__" :
    camera = URLStream(url = "rtsp://admin:admin@192.168.10.12:1935")
    print(camera.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    print(camera.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))