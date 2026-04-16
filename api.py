from flask import Flask, request, jsonify
from resume_parser import extract_text_from_pdf
from skill_matcher import extract_skills, calculate_match

app = Flask(__name__)

@app.route("/")
def home():
    return "API Running"

@app.route("/analyze", methods=["POST"])
def analyze_resume():
    try:
        file = request.files.get("resume")
        job_description = request.form.get("job_description")

        if not file or not job_description:
            return jsonify({"error": "Missing inputs"}), 400

        resume_text = extract_text_from_pdf(file)

        resume_skills = extract_skills(resume_text)
        job_skills = extract_skills(job_description)

        score, matched, missing = calculate_match(resume_skills, job_skills)

        return jsonify({
            "score": score,
            "matched_skills": matched,
            "missing_skills": missing
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)