import cv2
import time
import grpc
from concurrent import futures
import threading
import camera_pb2
import camera_pb2_grpc

from module.cameraStream import CameraStream


class CameraService(camera_pb2_grpc.CameraServiceServicer):
    def __init__(self) :
        self.camera_stream = CameraStream(camera_index = 0)

    def StreamFrames(self, request, context):
        """Stream frames to the client."""
        while True :
            frame = self.camera_stream.get_frame()
            if frame is None : 
                continue
            
            # Encode frame as JPEG
            _, buffer = cv2.imencode('.jpg', frame)
            yield camera_pb2.FrameData(frame=buffer.tobytes(), timestamp=int(time.time() * 1000))

    def __del__(self):
        self.camera_stream.release()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    camera_pb2_grpc.add_CameraServiceServicer_to_server(CameraService(), server)
    server.add_insecure_port("0.0.0.0:50051")
    server.start()
    print("gRPC server started on port 50051")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
