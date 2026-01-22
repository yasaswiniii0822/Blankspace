from flask import Flask, render_template, request, jsonify
from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    raise RuntimeError("GROQ_API_KEY not found in environment")

print("API KEY LOADED: True")

app = Flask(__name__)
client = Groq(api_key=API_KEY)

SYSTEM_PROMPT = """
You are a friendly, calm art-block assistant.

Your goal is to gently help users feel safe enough to start creating.

Guidelines:
- Be warm, reassuring, and conversational.
- Acknowledge feelings without being dramatic or poetic.
- Ask 1–2 thoughtful questions max.
- Help identify the type of art block (overwhelm, fear, boredom, low energy).
- Ask about the medium and available time if relevant.
- Suggest ONE small, low-pressure action to start.
- Avoid clichés and generic motivation.
- Do not overwhelm the user with options.
- End with a gentle, clear next step.

Tone:
- Supportive, kind, and grounded.
- It’s okay to be a bit longer if it helps the user feel understood.
"""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(force=True)
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"reply": "Say something first."})

        print("USING MODEL: llama-3.3-70b-versatile")

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            max_tokens=80,
            temperature=0.4
        )

        reply = completion.choices[0].message.content
        return jsonify({"reply": reply})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"reply": f"ERROR: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)
