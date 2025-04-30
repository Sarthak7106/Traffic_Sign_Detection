# 🚦 Traffic Sign Detection System
Website link: https://v0-react-ui-component-conversion.vercel.app/detect 

A deep learning–powered traffic sign detection system using **YOLOv8** and **CNN**, integrated with a full-stack web interface using **FastAPI** and **React.js**.

---

## 📌 Features

- Detects and classifies traffic signs from images in real-time  
- Uses **YOLOv8** for object detection and **CNN** for classification comparison  
- Web-based frontend built with **React.js**  
- Fast and lightweight **FastAPI** backend for model inference  
- API testing and validation using **Postman**

---

## 📁 Dataset Used

- **GTSRB (German Traffic Sign Recognition Benchmark)**  
- **Traffic Sign Detection Dataset (16 Classes)**  
  - Used for quick testing and development due to smaller size and faster processing on low-spec machines

---

## 🎯 Project Objectives

- Build an accurate model for detecting and classifying traffic signs  
- Compare traditional CNN-based classification with YOLOv8 detection  
- Integrate model results into a responsive web app using FastAPI and React  
- Enable real-time inference and user interaction

---

## ⚙️ Tech Stack

| Layer       | Tools / Technologies                      |
|-------------|-------------------------------------------|
| Frontend    | React.js, HTML, CSS                       |
| Backend     | FastAPI, Python                           |
| Deep Learning | YOLOv8 (Ultralytics), CNN (Keras/TensorFlow) |
| Dataset     | GTSRB, Traffic Sign Detection Dataset     |
| API Testing | Postman                                   |

---

## 🧠 Model Overview

- **YOLOv8**: Used for real-time object detection with bounding boxes and labels  
- **CNN**: Used initially for traffic sign classification on GTSRB dataset  

---

## 🏗️ System Architecture

```
[User Uploads Image]
       ↓
[React.js Frontend]
       ↓
[FastAPI Backend → YOLOv8 Inference]
       ↓
[Return Detection Results]
       ↓
[Frontend Displays Results]
```

---

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/traffic-sign-detection.git
cd traffic-sign-detection
```

### 2. Setup Backend (FastAPI)

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### 3. Setup Frontend (React)

```bash
cd frontend
npm install
npm run dev
```

---

## 🧪 API Testing

Use **Postman** to test API endpoints:

- `POST /predict` – Upload image and receive detection result
- `GET /health` – Check server status

---

## 📊 Results

- Achieved high detection accuracy on YOLOv8 for both datasets  
- Smooth integration and real-time performance on local systems  
- Responsive UI with clear bounding box visualizations

---

## 💡 Use Case Scenarios

- Autonomous Vehicles  
- Driver Assistance Systems  
- Smart Traffic Monitoring in Cities  
- Traffic Surveillance & Violation Detection

---

## 🚲 Challenges Faced

- Limited compute power for large models  
- Balancing speed vs. accuracy  
- Integrating ML inference seamlessly into a full-stack web app

---

## 🔮 Future Work

- Expand dataset with real-world, multilingual traffic signs  
- Deploy on cloud infrastructure (e.g., AWS/GCP)  
- Add support for live video detection  
- Enhance UI with additional analytics features

---

## 📚 References

- GTSRB Dataset – [Link](https://benchmark.ini.rub.de/gtsrb_news.html)  
- Ultralytics YOLOv8 – [https://docs.ultralytics.com](https://docs.ultralytics.com)  
- FastAPI Docs – [https://fastapi.tiangolo.com](https://fastapi.tiangolo.com)

