from flask import Blueprint, render_template, request
from flask_login import login_required
import google.generativeai as genai
from decouple import config

ai_bp = Blueprint('ai', __name__)

# Cấu hình Gemini
genai.configure(api_key=config("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash-latest")

@ai_bp.route("/ai-explain", methods=["GET", "POST"])
@login_required
def ai_explain():
    explanation = ""
    code = ""
    if request.method == "POST":
        code = request.form.get("code")
        prompt = f"Giải thích đoạn mã Python sau một cách dễ hiểu:\n\n{code}"
        try:
            response = model.generate_content(prompt)
            explanation = response.text
        except Exception as e:
            explanation = f"Lỗi AI: {str(e)}"
    return render_template("ai/ai_explain.html", code=code, explanation=explanation)
