import os
import sys
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from gemini_service import GeminiAssessmentService
from curriculum_data import GRADE_5_CURRICULUM

# Mutlak yol ile .env dosyasını yükle
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
load_dotenv(dotenv_path=env_path, override=True)

app = Flask(__name__)
service = None

def get_service():
    global service
    if service is None:
        try:
            load_dotenv(dotenv_path=env_path, override=True)
            service = GeminiAssessmentService()
        except Exception as e:
            print(f"Uyarı: Gemini servisi başlatılamadı: {e}")
            service = None
    return service

# Başlangıçta servisi yüklemeyi dene
get_service()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/curriculum")
def get_curriculum():
    return jsonify(GRADE_5_CURRICULUM)

@app.route("/api/generate", methods=["POST"])
def generate():
    srv = get_service()
    if not srv:
        return jsonify({
            "success": False,
            "error": "Gemini API servisi başlatılamadı. Lütfen .env dosyasındaki GEMINI_API_KEY anahtarını kontrol edin."
        }), 500

    data = request.json or {}
    grade_level = data.get("grade_level", "5. Sınıf")
    subject = data.get("subject", "Fen Bilimleri")
    learning_area = data.get("learning_area", "")
    learning_outcome = data.get("learning_outcome", "")
    assessment_tool = data.get("assessment_tool", "A4 Pedagojik Çalışma Kâğıdı")
    difficulty = data.get("difficulty", "Orta")
    question_count = int(data.get("question_count", 1))
    custom_context = data.get("custom_context", "")
    template_style = data.get("template_style", "random")
    advanced_options = data.get("advanced_options", None)

    if not learning_outcome:
        return jsonify({"success": False, "error": "Öğrenme çıktısı boş olamaz."}), 400

    try:
        content_json = srv.generate_assessment(
            grade_level=grade_level,
            subject=subject,
            learning_area=learning_area,
            learning_outcome=learning_outcome,
            assessment_tool=assessment_tool,
            difficulty=difficulty,
            question_count=question_count,
            custom_context=custom_context,
            template_style=template_style,
            advanced_options=advanced_options
        )
        return jsonify({"success": True, "content": content_json})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Antigravity Standart Çalışma Kâğıdı Sunucusu Başlatılıyor: http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)
