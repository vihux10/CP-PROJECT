from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# --- HTML FRONTEND (Embedded) ---
HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Student Performance Predictor</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #f0f2f5; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .container { background: white; padding: 30px; border-radius: 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.1); width: 350px; text-align: center; }
        input { width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ddd; border-radius: 8px; box-sizing: border-box; }
        button { width: 100%; padding: 12px; background: #007bff; color: white; border: none; border-radius: 8px; cursor: pointer; font-size: 16px; transition: 0.3s; }
        button:hover { background: #0056b3; }
        #result { margin-top: 20px; padding: 15px; border-radius: 8px; display: none; }
        .Good { background: #d4edda; color: #155724; }
        .Average { background: #fff3cd; color: #856404; }
        .Poor { background: #f8d7da; color: #721c24; }
    </style>
</head>
<body>
    <div class="container">
        <h2>🎓 Predictor</h2>
        <input type="number" id="hours" placeholder="Study Hours (0-12)">
        <input type="number" id="attendance" placeholder="Attendance % (0-100)">
        <button onclick="predict()">Calculate Result</button>
        <div id="result"></div>
    </div>

    <script>
        async function predict() {
            const h = document.getElementById('hours').value;
            const a = document.getElementById('attendance').value;
            const resDiv = document.getElementById('result');

            const response = await fetch('/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ study_hours: h, attendance: a })
            });

            const data = await response.json();
            resDiv.style.display = 'block';
            resDiv.className = data.performance;
            resDiv.innerHTML = `<strong>Predicted Marks: ${data.predicted_marks}%</strong><br>Status: ${data.performance}`;
        }
    </script>
</body>
</html>
"""

# --- BACKEND ROUTES ---

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        hours = float(data.get('study_hours', 0))
        attendance = float(data.get('attendance', 0))

        # Prediction Logic
        marks = (hours * 8) + (attendance * 0.4)
        marks = min(100, round(marks, 2))
        
        perf = "Good" if marks >= 75 else "Average" if marks >= 40 else "Poor"

        return jsonify({"predicted_marks": marks, "performance": perf})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
