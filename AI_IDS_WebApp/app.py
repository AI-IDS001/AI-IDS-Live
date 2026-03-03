import pandas as pd
import joblib
from flask import Flask, request, jsonify, render_template
import os

# --- CONFIGURATION ---
MODEL_PATH = 'nids_pipeline.pkl'
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}

# Initialize the App
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- LOAD THE BRAIN (Global Scope) ---
print("⏳ Loading AI-IDS Model...")
try:
    model_pipeline = joblib.load(MODEL_PATH)
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model_pipeline = None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- ROUTES ---

@app.route('/')
def home():
    """Renders the main dashboard."""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_traffic():
    """
    API Endpoint: Receives a CSV file, runs the model, returns JSON stats.
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
        
    if file and allowed_file(file.filename):
        try:
            # 1. Read the CSV directly into Pandas
            df = pd.read_csv(file)
            
            # 2. Validation: Ensure we have the right columns (41 features)
            # We check if the input shape matches what the model expects (minus the label col if present)
            expected_features = 41
            if df.shape[1] < expected_features:
                 return jsonify({"error": f"Invalid CSV format. Expected {expected_features} columns, got {df.shape[1]}."}), 400

            # 3. Clean: Drop 'label' or 'binary_target' if user accidentally included them
            # (In production, incoming traffic won't have labels, but test files might)
            cols_to_drop = [c for c in df.columns if 'label' in c.lower() or 'target' in c.lower()]
            X_input = df.drop(columns=cols_to_drop, errors='ignore')

            # 4. PREDICT with PROBABILITY
            # We need the probability to apply our Custom Threshold (0.8)
            probs = model_pipeline.predict_proba(X_input)[:, 1] # Probability of being 'Attack' (Class 1)

            # 5. Apply the "Safety Threshold" (0.8)
            # If Model is > 80% sure it's an attack, mark as 1. Otherwise 0.
            predictions = (probs > 0.5).astype(int)

            # 6. Generate Report Stats
            total_packets = len(predictions)
            attack_count = int(sum(predictions))
            normal_count = total_packets - attack_count
            
            # Calculate Risk Score (0 to 100)
            risk_score = round((attack_count / total_packets) * 100, 1)

            results = {
                "status": "success",
                "total_packets": total_packets,
                "attacks_detected": attack_count,
                "normal_traffic": normal_count,
                "risk_score": risk_score,
                "preview": predictions[:10].tolist() # Send first 10 results for debugging
            }

            return jsonify(results)

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return jsonify({"error": "Invalid file type. Please upload a CSV."}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)