# Real-Time Face Recognition & Emotion Detection  

A real-time AI-powered application that uses **Flask (Python)** as backend and **React.js** as frontend to perform face recognition and detect emotions like Happy, Sad, Angry, Neutral, and Surprise.  

---

## 🚀 Features
- Real-time face recognition using OpenCV & face_recognition  
- Emotion detection powered by TensorFlow/Keras & FER library  
- Frontend built with React.js for smooth UI  
- Backend built with Flask for fast API responses  
- Displays detected face + emotion live via webcam  

---

## 🛠 Tech Stack
**Frontend:** React.js, JavaScript, HTML, CSS  
**Backend:** Flask, Python  
**Libraries:** OpenCV, face_recognition, TensorFlow, Keras, FER  
**Other:** CORS, NumPy  

---

## ⚙️ Setup Instructions

1️⃣ Backend (Flask)
bash
cd backend
pip install -r requirements.txt
python app.py
Runs on: http://127.0.0.1:5000

2️⃣ Frontend (React)
bash
Copy code
cd frontend
npm install
npm start
Runs on: http://localhost:3000

📂 Project Structure
php
Copy code
face-emotion-project/
│── backend/         # Flask backend with APIs
│   ├── app.py       # Main Flask app
│   ├── requirements.txt
│   ├── known_faces/ # Store reference face images
│   └── static/      # Static files (HTML/JS/CSS if needed)
│
│── frontend/        # React.js frontend
│   ├── src/         
│   ├── public/      
│   └── package.json
│
└── README.md        # Project documentation


🚀 Future Enhancements
Deploy project to cloud (Heroku/AWS/GCP/Azure)

Add Docker support for easier setup

Support more emotions & intensity levels

Add user authentication (login/register)

Store recognition history in a database (PostgreSQL/MongoDB)


👨‍💻 Author
Suhail Shaik
🔗 GitHub | LinkedIn