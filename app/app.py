import json
import sys
from pathlib import Path

from flask import Flask, jsonify, render_template_string, request


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.agent.agent import ReviewAgent


app = Flask(__name__)
agent = ReviewAgent(config={"agent": {"enable_llm": False, "complexity_threshold": 10}})


PAGE = """
<!doctype html>
<html>
<head>
  <meta charset=\"utf-8\" />
  <title>AI Code Review Agent</title>
  <style>
    body { font-family: sans-serif; max-width: 960px; margin: 24px auto; padding: 0 12px; }
    textarea { width: 100%; min-height: 260px; }
    button { margin-top: 12px; padding: 8px 16px; }
    pre { background: #f6f8fa; padding: 12px; overflow-x: auto; }
  </style>
</head>
<body>
  <h1>AI Code Review Agent</h1>
  <form method=\"post\" action=\"/review\">
    <textarea name=\"code\" placeholder=\"Paste Python code here\">{{ code }}</textarea>
    <br />
    <button type=\"submit\">Review</button>
  </form>
  {% if report %}
  <h2>Result</h2>
  <pre>{{ report }}</pre>
  {% endif %}
</body>
</html>
"""


@app.get("/")
def index():
    return render_template_string(PAGE, code="", report=None)


@app.post("/review")
def review():
    code = request.form.get("code", "")
    report_obj = agent.review(code)
    report_text = json.dumps(report_obj, ensure_ascii=False, indent=2)
    return render_template_string(PAGE, code=code, report=report_text)


@app.post("/api/review")
def api_review():
    payload = request.get_json(force=True)
    code = payload.get("code", "")
    return jsonify(agent.review(code))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
