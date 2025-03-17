from flask import Blueprint, jsonify, request
import openai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define the blueprint
mentor_bp = Blueprint('mentor', __name__)

# Initialize chat history
chat_history = [
    {"role": "system", "content": (
        "You are an AI Mentor specializing in technology and career guidance. "
        "Answer questions related to technology and career advice. Any other topics are outside of your scope. "
        "You can generate minimum code as well. "
        "If any foul language is detected, mention it's against ethics. "
        "Responses should be structured using HTML tags for better readability (e.g., <strong>bold</strong>, <ul>list</ul>, <pre><code>code</pre></code>)."
    )}
]

@mentor_bp.route("/mentor/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        chat_history.append({"role": "user", "content": user_message})

        # Prepare input for GPT-4
        conversation = [{"role": "system", "content": chat_history[0]["content"]}]
        conversation.append({"role": "user", "content": user_message})

        # Make the API request to OpenAI's GPT-4
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Use GPT-4
            messages=conversation,
            max_tokens=512,
            temperature=0.7,
        )

        ai_response = response['choices'][0]['message']['content']
        formatted_response = format_response(ai_response)

        # Save assistant's response to chat history
        chat_history.append({"role": "assistant", "content": formatted_response})

        return jsonify({"response": formatted_response})

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500

def format_response(response_text):
    response_text = response_text.replace("**", "<strong>").replace("<strong>", "</strong>")
    response_text = response_text.replace("*", "<em>").replace("<em>", "</em>")
    response_text = response_text.replace("\n- ", "\n<ul><li>").replace("\n* ", "\n<ul><li>")
    response_text = response_text.replace("\n", "</li>\n") + "</ul>"
    response_text = response_text.replace("```", "<pre><code>").replace("<pre><code>", "</code></pre>")
    response_text = response_text.replace(". ", ".<br><br>")
    return response_text