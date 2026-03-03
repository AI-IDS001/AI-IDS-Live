# 🛡️ AI-IDS: Intelligent Network Intrusion Detection System

## 📌 Project Overview
AI-IDS is a web-based cybersecurity tool that uses Machine Learning (Random Forest) to detect network anomalies in real-time. Unlike rule-based firewalls, this system learns from traffic patterns to identify malicious activity with **84% accuracy**.

## 🚀 Key Features
- **AI-Powered Detection:** Uses a trained Random Forest model to classify traffic as `Normal` or `Attack`.
- **Premium Dashboard:** A modern, dark-mode UI with glassmorphism design.
- **Instant Analysis:** Processes CSV network logs in milliseconds.
- **Threat Scoring:** Calculates a dynamic risk score based on the ratio of malicious packets.

## 🛠️ Tech Stack
- **Backend:** Python, Flask, Pandas, Scikit-Learn.
- **Frontend:** HTML5, CSS3, JavaScript (Fetch API).
- **Model:** Random Forest Classifier (Trained on NSL-KDD Dataset).
- **Pipeline:** Automated preprocessing (StandardScaler) + Inference.

## 📂 Project Structure
```text
/AI_IDS_WebApp
│
├── app.py                 # The Flask API Server
├── nids_pipeline.pkl      # The Trained ML Brain (Model + Scaler)
├── static/
│   ├── style.css          # Premium Dark Mode Styling
│   └── script.js          # Frontend Logic & API Handling
├── templates/
│   └── index.html         # Main Dashboard Interface
└── README.md              # Documentation