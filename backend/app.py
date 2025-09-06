from flask import Flask, Response, jsonify, request
from flask_cors import CORS
import cv2
from fer import FER
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize emotion detector
emotion_detector = FER(mtcnn=False)
latest_emotion = {"emotion": "neutral"}

# Camera for local webcam streaming
camera = cv2.VideoCapture(0)

@app.route('/test')
def test():
    return jsonify({"status": "API working!"})



def generate_frames():
    global latest_emotion
    while True:
        success, frame = camera.read()
        if not success:
            continue

        try:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            emotions = emotion_detector.detect_emotions(rgb_frame)

            for e in emotions:
                (x, y, w, h) = e["box"]
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                emotion, score = max(e["emotions"].items(), key=lambda item: item[1])
                cv2.putText(frame, f"{emotion} ({score:.2f})", (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

                latest_emotion["emotion"] = emotion

            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        except Exception as e:
            print("❌ Error in generate_frames:", e)
            continue


@app.route("/video_feed")
def video_feed():
    return Response(generate_frames(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/latest_emotion")
def get_emotion():
    return jsonify(latest_emotion)


@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    img = cv2.imread(filepath)
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    emotions = emotion_detector.detect_emotions(rgb_img)

    if emotions:
        e = emotions[0]
        emotion, score = max(e["emotions"].items(), key=lambda item: item[1])
    else:
        emotion, score = "neutral", 0.0

    return jsonify({"emotion": emotion, "score": score})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

    
