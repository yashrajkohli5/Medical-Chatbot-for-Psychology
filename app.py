from flask import Flask, render_template, request
import httpx

app = Flask(__name__)

# Replace this with your actual OpenRouter API key
OPENROUTER_API_KEY = OPENAI_API_KEY

# Home route - serves the chatbot UI
@app.route("/")
def home():
    return render_template("chat.html")  # Make sure index.html is in the 'templates' folder

# Chatbot response route - handles AJAX POST requests
@app.route("/get", methods=["POST"])
def get_bot_response():
    user_input = request.form["msg"]

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "http://127.0.0.1:5000",  # optional
        "X-Title": "Medical Chatbot",             # optional
    }

    payload = {
        "model": "nvidia/llama-3.1-nemotron-ultra-253b-v1:free",
        "messages": [{"role": "user", "content": user_input}]
    }

    try:
        response = httpx.post("https://openrouter.ai/api/v1/chat/completions",
                              headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
