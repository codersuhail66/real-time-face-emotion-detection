from flask import Flask, Response, jsonify
from flask_cors import CORS
import cv2
from fer import FER

app = Flask(__name__)
CORS(app)

# FER with HaarCascade (requires grayscale uint8)
emotion_detector = FER(mtcnn=False)
latest_emotion = {"emotion": "neutral"}

camera = cv2.VideoCapture(0)   


def generate_frames():
    global latest_emotion
    while True:
        success, frame = camera.read()
        if not success:
            continue

        try:
            # FER needs RGB, but we keep BGR for streaming
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Detect emotions
            emotions = emotion_detector.detect_emotions(rgb_frame)

            for e in emotions:
                (x, y, w, h) = e["box"]
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                emotion, score = max(e["emotions"].items(), key=lambda item: item[1])
                cv2.putText(frame, f"{emotion} ({score:.2f})", (x, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

                latest_emotion["emotion"] = emotion

            # Encode the (still BGR) frame for streaming
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

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

if __name__ == "__main__":
    app.run(debug=True)
