from flask import Flask, request, jsonify, render_template
from groq import Groq

app = Flask(__name__)

GROQ_API_KEY = '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'
client = Groq(api_key=GROQ_API_KEY)

with open("Z:/python/Mann/knowledge.txt", "r", encoding="utf-8") as file:
    knowledge = file.read()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")

    if user_message.lower() in ["hi", "hello", "hey"]:
        return jsonify({
            "response": "Hello! I am an XplainAI chatbot. I can help you understand AI concepts. Ask me anything related to AI!"
        })

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{
            "role": "user",
            "content": (
                f"Answer from this data: {knowledge}\n\n"
                f"Question: {user_message}\n"
                "if the answer is not in the data, say 'Please ask another question or question related to AI'."
            ),
        }],
    )

    bot_reply = completion.choices[0].message.content.strip()
    return jsonify({"response": bot_reply})


if __name__ == "__main__":
    app.run(debug=True)
