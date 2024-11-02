import random

def random_string():
    random_list = [
        "I'm your travel guide! Please mention a state name (like Kerala, Goa, Rajasthan) or ask about specific travel aspects.",
        "I can help you explore India! Which state would you like to know about?",
        "Not sure what you're looking for? Try asking about a specific state or travel topic like costs, weather, or safety.",
        "I'm here to help with your travel plans! Just mention a state name or ask about travel-related topics.",
        "Looking to explore India? Just mention any state name, and I'll guide you through the attractions!"
    ]

    return random.choice(random_list)