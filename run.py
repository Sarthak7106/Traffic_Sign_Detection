from flask import Flask, request, jsonify, send_from_directory
import cv2
import numpy as np
import os
from werkzeug.utils import secure_filename
from ultralytics import YOLO
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS globally

# Define allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mp4'}

# Upload folder
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load YOLO model
Valid_model = YOLO(r'C:\Users\rajsa\OneDrive\Desktop\yolo run\backend\best.onnx')

# Helper functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def normalize_image(image):
    return image / 255.0

def resize_image(image, size=(640, 640)):
    return cv2.resize(image, size)

@app.route('/process', methods=['POST'])
def process_input():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        input_type = request.form.get('type', '').lower()

        if input_type == "image":
            image = cv2.imread(filepath)
            if image is not None:
                resized = resize_image(image)
                normalized = normalize_image(resized)
                normalized_uint8 = (normalized * 255).astype(np.uint8)

                results = Valid_model.predict(source=normalized_uint8, imgsz=640, conf=0.5)
                annotated = results[0].plot(line_width=1)
                annotated_rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)

                result_path = os.path.join(app.config['UPLOAD_FOLDER'], 'result_image.jpg')
                cv2.imwrite(result_path, annotated_rgb)

                return jsonify({
                    "message": "Image processed successfully",
                    "result_url": f"http://localhost:5000/uploads/result_image.jpg"
                })

        elif input_type == "video":
            cap = cv2.VideoCapture(filepath)
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            result_path = os.path.join(app.config['UPLOAD_FOLDER'], 'result_video.mp4')
            out = cv2.VideoWriter(result_path, fourcc, 20.0, (640, 640))

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                frame = resize_image(frame)
                results = Valid_model.predict(source=frame, imgsz=640, conf=0.5)
                annotated = results[0].plot(line_width=1)
                out.write(annotated)

            cap.release()
            out.release()
            cv2.destroyAllWindows()

            return jsonify({
                "message": "Video processed successfully",
                "result_url": f"http://localhost:5000/uploads/result_video.mp4"
            })

        else:
            return jsonify({"error": "Invalid input type"}), 400
    else:
        return jsonify({"error": "File not allowed"}), 400

@app.route('/uploads/<path:filename>')
def serve_file(filename):
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if not os.path.exists(file_path):
            return jsonify({"error": "File not found"}), 404
        
        response = send_from_directory(app.config['UPLOAD_FOLDER'], filename)
        
        # Set the content type for videos
        if filename.endswith('.mp4'):
            response.headers["Content-Type"] = "video/mp4"
        
        # Ensure CORS headers are correctly set
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        
        return response
    except Exception as e:
        return jsonify({"error": f"An error occurred while serving the file: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)
