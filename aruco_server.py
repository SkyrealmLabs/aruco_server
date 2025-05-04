from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import cv2
import numpy as np
import base64
import time

app = FastAPI()

# Allow all origins (you can restrict this in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ArUco dictionary and detector
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
parameters = cv2.aruco.DetectorParameters()

class ImageData(BaseModel):
    image: str  # base64-encoded image string

@app.post("/detect")
async def detect_aruco(data: ImageData):
    start_time = time.time()

    try:
        # Decode base64 image
        image_data = base64.b64decode(data.image.split(',')[1])
        np_arr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image data: {e}")

    try:
        # Detect ArUco markers
        detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)
        corners, ids, _ = detector.detectMarkers(img)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Marker detection failed: {e}")

    duration = time.time() - start_time
    print(f"Processed in {duration:.2f} seconds. Markers: {ids.flatten().tolist() if ids is not None else 'None'}")

    return {"markers": ids.flatten().tolist() if ids is not None else []}
