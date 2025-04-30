from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import shutil
import subprocess
from ultralytics import YOLO
import cv2
import numpy as np

# Initialize FastAPI app
app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Upload and result directories
UPLOAD_FOLDER = "./uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.mount("/static", StaticFiles(directory=UPLOAD_FOLDER), name="static")

# Load YOLO model
model = YOLO("backend/best.onnx")  # adjust path if needed

# Helper functions
def normalize_image(image):
    return image / 255.0

def resize_image(image, size=(640, 640)):
    return cv2.resize(image, size)

@app.post("/process")
async def process_file(file: UploadFile = File(...), type: str = Form(...)):
    filename = file.filename
    ext = filename.split('.')[-1].lower()
    allowed = {'jpg', 'jpeg', 'png', 'mp4'}

    if ext not in allowed:
        return JSONResponse(status_code=400, content={"error": "Unsupported file format"})

    filepath = os.path.join(UPLOAD_FOLDER, filename)

    # Save uploaded file
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Process image
    if type.lower() == "image":
        image = cv2.imread(filepath)
        if image is None:
            return JSONResponse(status_code=400, content={"error": "Failed to load image"})

        resized = resize_image(image)
        norm_img = normalize_image(resized)
        norm_img_uint8 = (norm_img * 255).astype(np.uint8)

        # Run YOLO prediction
        results = model.predict(source=norm_img_uint8, imgsz=640, conf=0.5)
        annotated = results[0].plot(line_width=1)

        result_path = os.path.join(UPLOAD_FOLDER, "result_image.jpg")
        cv2.imwrite(result_path, annotated)

        return {
            "message": "Image processed",
            "result_image": f"/static/result_image.jpg"
        }

    # Process video
    elif type.lower() == "video":
        output_path = os.path.join(UPLOAD_FOLDER, "converted_input.mp4")
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'panic', '-i', filepath, output_path])

        # Run YOLO prediction on video
        model.predict(source=output_path, save=True, save_txt=False)

        # Get most recent prediction folder
        detect_folder = "runs/detect"
        subdirs = sorted(os.listdir(detect_folder), key=lambda x: os.path.getctime(os.path.join(detect_folder, x)))
        latest = os.path.join(detect_folder, subdirs[-1])
        pred_video = os.path.join(latest, "converted_input.avi")

        result_video = os.path.join(UPLOAD_FOLDER, "result_video.mp4")
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'panic', '-i', pred_video, result_video])

        return {
            "message": "Video processed",
            "result_video": f"/static/result_video.mp4"
        }

    else:
        return JSONResponse(status_code=400, content={"error": "Invalid type. Use 'image' or 'video'."})
