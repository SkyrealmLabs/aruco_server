from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import base64
import logging
import time

app = Flask(__name__)
CORS(app, resources={r"/detect": {"origins": "*"}})  # You can restrict "*" to a specific domain in production

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = app.logger

# Load ArUco dictionary and parameters
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
parameters = cv2.aruco.DetectorParameters()

@app.route('/detect', methods=['POST'])
def detect_aruco():
    start_time = time.time()
    data = request.json

    if not data or 'image' not in data:
        return jsonify({"error": "No image provided"}), 400

    try:
        # Decode base64 image
        image_data = base64.b64decode(data['image'].split(',')[1])
        np_arr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    except Exception as e:
        logger.error(f"Error decoding image: {e}")
        return jsonify({"error": "Invalid image data", "details": str(e)}), 400

    try:
        # Detect ArUco markers
        detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)
        corners, ids, _ = detector.detectMarkers(img)
    except Exception as e:
        logger.error(f"Error detecting markers: {e}")
        return jsonify({"error": "Marker detection failed", "details": str(e)}), 500

    duration = time.time() - start_time
    logger.info(f"Image processed in {duration:.2f} seconds. Markers found: {ids.flatten().tolist() if ids is not None else 'None'}")

    if ids is not None:
        return jsonify({"markers": ids.flatten().tolist()})
    else:
        return jsonify({"markers": []})

# For development only (use Gunicorn in production)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
