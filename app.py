from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from ultralytics import YOLO
import cv2

app = Flask(__name__)

# Path to your model
model = YOLO('try/best (1).pt')  # Replace with the actual model path

# Path to the folder where uploaded images will be saved
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Process the uploaded image
        image = cv2.imread(file_path)
        results = model(image)
        
        # Get the first result
        result = results[0]

        # Extract class names and bounding boxes
        boxes = result.boxes.xyxy.cpu().numpy()
        scores = result.boxes.conf.cpu().numpy()
        class_ids = result.boxes.cls.cpu().numpy()

        # Fetch class names from the model
        class_names = model.names

        # Annotate image with bounding boxes and labels
        for box, score, class_id in zip(boxes, scores, class_ids):
            x1, y1, x2, y2 = map(int, box)
            label = f"{class_names[int(class_id)]}: {score:.2f}"
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        # Save the processed image
        processed_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'processed_' + filename)
        cv2.imwrite(processed_image_path, image)

        # Get the class names (you can choose to display only the first one if there are multiple detections)
        detected_classes = [class_names[int(class_id)] for class_id in class_ids]

        return render_template('preview.html', filename='processed_' + filename, detected_classes=detected_classes)

if __name__ == '__main__':
    app.run(debug=True)
