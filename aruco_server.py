from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import base64

app = Flask(__name__)
CORS(app)  # Allow connections from Expo app

# Load ArUco dictionary
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
parameters = cv2.aruco.DetectorParameters()

@app.route('/detect', methods=['POST'])
def detect_aruco():
    data = request.json
    print(data)

    if 'image' not in data:
        return jsonify({"error": "No image provided"}), 400

    # Decode base64 image
    image_data = base64.b64decode(data['image'].split(',')[1])
    np_arr = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # Detect markers
    detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)
    corners, ids, _ = detector.detectMarkers(img)

    # Return marker IDs if detected
    if ids is not None:
        return jsonify({"markers": ids.flatten().tolist()})
    else:
        return jsonify({"markers": []})

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5001)
