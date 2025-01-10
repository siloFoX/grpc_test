import cv2
import time
import grpc
from concurrent import futures
import camera_pb2
import camera_pb2_grpc

class CameraService(camera_pb2_grpc.CameraServiceServicer):
    def StreamFrames(self, request, context):
        cap = cv2.VideoCapture(0)  # Open USB camera (0 = /dev/video0)
        if not cap.isOpened():
            context.abort(grpc.StatusCode.UNAVAILABLE, "Camera not available")
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                # Encode frame as JPEG
                _, buffer = cv2.imencode('.jpg', frame)
                yield camera_pb2.FrameData(frame=buffer.tobytes(), timestamp=int(time.time() * 1000))
                
                # Throttle frame rate (e.g., 30 FPS)
                time.sleep(1 / 30)
        finally:
            cap.release()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    camera_pb2_grpc.add_CameraServiceServicer_to_server(CameraService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("gRPC server started on port 50051")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
