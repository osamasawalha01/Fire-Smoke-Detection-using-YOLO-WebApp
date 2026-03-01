import os
from flask import Flask, request, render_template, send_from_directory, jsonify
from ultralytics import YOLO
from PIL import Image
from io import BytesIO
import base64

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

model = YOLO('best.onnx', task='detect')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        img = None
        filename = None
        if 'file' in request.files and request.files['file'].filename != '':
            file = request.files['file']
            img = Image.open(file.stream)
            filename = 'uploaded.jpg'
        elif 'image' in request.form:
            data_url = request.form['image'].strip()
            if not data_url or len(data_url) < 100:  # Rough check for empty/invalid
                return jsonify({'error': 'Empty or invalid camera frame'}), 400
            _, encoded = data_url.split(',', 1)
            img_data = base64.b64decode(encoded)
            img = Image.open(BytesIO(img_data))
            if img.width < 10 or img.height < 10:  # Too small = black/empty frame
                return jsonify({'error': 'Invalid frame'}), 400
            filename = 'captured.jpg'
        else:
            return jsonify({'error': 'No image provided'}), 400

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        img.save(filepath)

        results = model(filepath)[0]
        annotated_filename = 'result_' + filename
        annotated_path = os.path.join(app.config['UPLOAD_FOLDER'], annotated_filename)
        results.save(annotated_path)

        detections = []
        for box in results.boxes:
            cls_id = int(box.cls[0])
            conf = box.conf[0].item()
            name = results.names[cls_id]
            detections.append(f"{name} ({conf:.2f})")

        detection_text = ', '.join(detections) if detections else "No fire or smoke detected"

        return jsonify({
            'image_url': f'/uploads/{annotated_filename}',
            'detections': detection_text,
            'success': True  # Flag for JS to stop live on success
        })
    except Exception as e:
        return jsonify({'error': f'Processing failed: {str(e)}'}), 500

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
