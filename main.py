import json
import re
import random_responses
from flask import Flask, request, jsonify

app = Flask(name)

# Existing code...

@app.route('/get_response', methods=['POST'])
def get_bot_response():
    user_input = request.json.get('message')
    bot_response = get_response(user_input)
    return jsonify({'response': bot_response})

if name == 'main':
    app.run(debug=True)

# Load JSON data
def load_json(file):
    with open(file) as bot_responses:
        print(f"Loaded '{file}' successfully!")
        return json.load(bot_responses)

# Store JSON data
response_data = load_json("bot.json")

def get_response(input_string):
    split_message = re.split(r'\s+|[,;?!.-]\s*', input_string.lower())
    score_list = []
    exact_match_responses = []

    # Add debug print
    print(f"Processing input: {split_message}")

    for response in response_data:
        response_score = 0
        required_score = 0
        required_words = response["required_words"]

        # Add debug print
        print(f"Checking response type: {response['response_type']}")
        print(f"Required words: {required_words}")

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

    # Add debug print
    print(f"Score list: {score_list}")
    print(f"Exact matches: {exact_match_responses}")

    if exact_match_responses:
        best_exact_response = max(exact_match_responses, key=lambda x: x[0])
        return best_exact_response[1]

    best_response = max(score_list, key=lambda x: x[0])
    if best_response[0] != 0:
        return best_response[1]

    return random_responses.random_string()

while True:
    user_input = input("You: ")
    print("Bot:", get_response(user_input))