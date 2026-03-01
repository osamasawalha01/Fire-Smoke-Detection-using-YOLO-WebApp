# Fire & Smoke Detection Web App 🛡️🔥

## 📌 Project Overview
This is a deep learning-based web application designed to detect fire and smoke in real-time. Built using the **YOLOv9** architecture, the system can process both static image uploads and live camera streams to provide instant visual feedback with confidence scores.

## 🚀 Key Features
* **Real-time Detection:** Capable of identifying 'Fire' and 'Smoke' classes from live camera frames.
* **Web Integration:** A robust Flask backend that handles image processing and serves an interactive GUI.
* **Inference Optimization:** The model is exported to **ONNX** format to ensure high performance and low latency during detection.
* **Responsive Interface:** Custom-built frontend using HTML, CSS, and JavaScript for a seamless user experience.

## 🛠️ Tech Stack
* **AI & Computer Vision:** Python, PyTorch, Ultralytics (YOLOv9), ONNX Runtime, OpenCV.
* **Backend:** Flask.
* **Frontend:** HTML5, CSS3, JavaScript.
* **Data Handling:** PIL (Pillow), PyYAML.

## 📊 Dataset & Training
* Trained on the **Fire and Smoke Detection dataset** from Kaggle.
* Fine-tuned using `yolov9c.pt` over 30 epochs with a batch size of 12.
* Achieved high precision in detecting both fire and smoke in diverse environmental conditions.

## ⚙️ How to Run
1. **Clone the Repo:**
   ```bash
   git clone [https://github.com/osamasawalha01/Fire-Smoke-Detection-using-YOLO-WebApp.git](https://github.com/osamasawalha01/Fire-Smoke-Detection-using-YOLO-WebApp.git)
   Osama Sawalha
