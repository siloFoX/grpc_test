import grpc
import cv2
import numpy as np
import camera_pb2
import camera_pb2_grpc

def main():
    channel = grpc.insecure_channel("localhost:50051")
    stub = camera_pb2_grpc.CameraServiceStub(channel)

    try:
        for response in stub.StreamFrames(camera_pb2.Empty()):
            # Decode JPEG frame
            frame = np.frombuffer(response.frame, dtype=np.uint8)
            img = cv2.imdecode(frame, cv2.IMREAD_COLOR)

            # Display frame
            cv2.imshow("Stream", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except grpc.RpcError as e:
        print(f"gRPC Error: {e}")
    finally:
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
