from flask import Flask, request, jsonify, render_template
import json
import re
import random_responses
from flask_cors import CORS

app = Flask(__name__) 
CORS(app)  # Enable CORS for all routes
# Load chatbot data
def load_json(file):
    with open(file, 'r', encoding='utf-8') as bot_responses:
        return json.load(bot_responses)

response_data = load_json("bot.json")

def get_response(input_string):
    split_message = re.split(r'\s+|[,;?!.-]\s*', input_string.lower())
    score_list = []
    exact_match_responses = []

    for response in response_data:
        response_score = 0
        required_score = 0
        required_words = response["required_words"]

        if required_words:
            for word in split_message:
                if word in required_words:
                    required_score += 1

        if required_score == len(required_words):
            for word in split_message:
                if word in response["user_input"]:
                    response_score += 1

            if required_score == len(required_words):
                exact_match_responses.append((response_score, response["bot_response"]))

        score_list.append((response_score, response["bot_response"]))

    if exact_match_responses:
        best_exact_response = max(exact_match_responses, key=lambda x: x[0])
        return best_exact_response[1]

    best_response = max(score_list, key=lambda x: x[0])
    if best_response[0] != 0:
        return best_response[1]

    return random_responses.random_string()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def chat_response():
    user_message = request.json["message"]
    bot_response = get_response(user_message)
    return jsonify(response=bot_response)

if __name__ == '__main__':
    app.run(debug=True)