import cv2
import time
import grpc
from concurrent import futures
import threading
import camera_pb2
import camera_pb2_grpc


class CameraService(camera_pb2_grpc.CameraServiceServicer):
    def __init__(self):
        # Initialize camera
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise RuntimeError("Failed to open camera /dev/video0")
        print("Camera initialized successfully.")

        # Shared frame and lock for thread safety
        self.latest_frame = None
        self.lock = threading.Lock()

        # Start the camera read thread
        self.running = True
        self.read_thread = threading.Thread(target=self._read_frames, daemon=True)
        self.read_thread.start()

    def _read_frames(self):
        """Continuously read frames from the camera."""
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to capture frame from camera.")
                continue

            # Update the latest frame
            with self.lock :
                self.latest_frame = frame

            # Throttle frame rate (e.g., 30 FPS)
            time.sleep(1 / 30)

    def StreamFrames(self, request, context):
        """Stream frames to the client."""
        while True:
            with self.lock:
                if self.latest_frame is None:
                    continue

                # Encode frame as JPEG
                _, buffer = cv2.imencode('.jpg', self.latest_frame)

            yield camera_pb2.FrameData(frame=buffer.tobytes(), timestamp=int(time.time() * 1000))

    def __del__(self):
        # Stop the camera read thread and release resources
        self.running = False
        if self.read_thread.is_alive():
            self.read_thread.join()
        if self.cap.isOpened():
            self.cap.release()
        print("Camera released successfully.")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    camera_pb2_grpc.add_CameraServiceServicer_to_server(CameraService(), server)
    server.add_insecure_port("0.0.0.0:50051")
    server.start()
    print("gRPC server started on port 50051")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
