from flask import Flask, render_template, request, jsonify
from groq import Groq
import os


app = Flask(__name__)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


SYSTEM_PROMPT = """
You are an art-block assistant.

Your job is to help users START creating, not inspire them.

Rules:
- Ask short, focused questions.
- Identify the type of art block (overwhelm, fear, boredom, low energy).
- Ask about medium and time.
- Give ONE small, actionable task.
- Do NOT give multiple ideas.
- Do NOT be poetic or motivational.
- help th user take the next step.
- Keep it concise (under 50 words).
- guide the user to create art.
- don't repeat questions
- End with a clear instruction.
"""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    print("User message:", user_message)

    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=200
        )

        reply = completion.choices[0].message.content
        print("Bot reply:", reply)

        return jsonify({"reply": reply})

    except Exception as e:
        print("🔥 AI ERROR:", e)
        return jsonify({
            "reply": "I’m having trouble thinking right now. Try again."
        })



if __name__ == "__main__":
    app.run(debug=True)
