from flask import Blueprint, request, jsonify
import openai
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OpenAI API key not found. Ensure it's set in the .env file.")

openai.api_key = OPENAI_API_KEY

mentor_bp = Blueprint("mentor", __name__)

chat_history = [
    {
        "role": "system",
        "content": (
            "You are an AI Mentor specializing in technology and career guidance. "
            "Just answer questions that are based on technology and career advice. Anything other than these topics are said to be out of your topic"
            "Answer something related to any job position related to Tech field."
            "You can generate minimum code as well."
            "If any foul language is detected, tell its against ethics and not to use it."
            "Your responses should be well-structured and formatted using HTML tags for better readability. "
            "Use <strong>bold</strong> for emphasis, <ul> for lists, and <pre><code> for code blocks. "
            "Maintain a friendly and professional tone."
        )
    }
]

@mentor_bp.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        chat_history.append({"role": "user", "content": user_message})

        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=chat_history
        )

        ai_response = response.choices[0].message.content.strip()

        if ai_response.lower().startswith("html"):
            ai_response = ai_response[4:].strip()

        formatted_response = format_response(ai_response)

        chat_history.append({"role": "assistant", "content": formatted_response})

        return jsonify({"response": formatted_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def format_response(response_text):
    response_text = response_text.replace("**", "<strong>").replace("<strong>", "</strong>")

    response_text = response_text.replace("*", "<em>").replace("<em>", "</em>")

    response_text = response_text.replace("\n- ", "\n<ul><li>").replace("\n* ", "\n<ul><li>")
    response_text = response_text.replace("\n", "</li>\n") + "</ul>"

    response_text = response_text.replace("```", "<pre><code>").replace("<pre><code>", "</code></pre>")

    response_text = response_text.replace(". ", ".<br><br>")

    return response_text
