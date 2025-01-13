from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, HTMLResponse
import grpc
import cv2
import numpy as np
import camera_pb2
import camera_pb2_grpc
from starlette.templating import Jinja2Templates

app = FastAPI()

# Template directory for HTML rendering
templates = Jinja2Templates(directory="templates")


def stream_frames():
    """Stream frames from gRPC server to the client."""
    channel = grpc.insecure_channel("192.168.10.38:50051")
    stub = camera_pb2_grpc.CameraServiceStub(channel)

    try:
        for response in stub.StreamFrames(camera_pb2.Empty()):
            # Decode JPEG frame
            frame = np.frombuffer(response.frame, dtype=np.uint8)
            img = cv2.imdecode(frame, cv2.IMREAD_COLOR)

            # Encode frame to JPEG for streaming
            _, jpeg = cv2.imencode('.jpg', img)
            yield (b"--frame\r\n"
                   b"Content-Type: image/jpeg\r\n\r\n" + jpeg.tobytes() + b"\r\n")
    except grpc.RpcError as e:
        print(f"gRPC Error: {e}")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Render the main HTML page."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/video_feed")
async def video_feed():
    """Stream video feed to the browser."""
    return StreamingResponse(stream_frames(),
                             media_type="multipart/x-mixed-replace; boundary=frame")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
