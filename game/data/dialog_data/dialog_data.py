STRANGER_GREETINGS = [
    "Hey!",
    "Hi!",
    "Howdy!",
    "Hey there!",
    "How are you?",
]
FRIEND_GREETINGS = [
    "Hey {player_name}!",
    "Hi {player_name}!",
    "Hey there {player_name}!",
    "Great to see you {player_name}!",
    "Good to see you!",
]
GREETINGS = STRANGER_GREETINGS + FRIEND_GREETINGS

GREETINGS_WRAP = []

FAREWELLS = [
    "Take care.",
    "See you around.",
    "Later.",
    "Bye." "Take care!",
    "Bye for now.",
]

GET_NAME_PROMPTS = ["What's your name", "I don't think we've met, what's your name?"]
GET_NAME_RESPONSES = [
    "I'm {name}, nice to meet you.",
    "I'm {name}.",
    "Name's {name}.",
    "It's {name}.",
    "Sorry, I'm {name}",
    "{name}.",
]

GET_NAME_WRAP = [
    "Nice to meet you.",
]

ANNOY_MESSAGES = ["Did you need something?", "Yes?", "You're starting to annoy me pal."]
APOLOGY_MESSAGES = ["Sorry!", "My bad", "Okay, I'm sorry."]

DEFAULT_NPC_DIALOG = {
    "greeting": {
        "text": GREETINGS,
        "choices": [
            {"text": GET_NAME_PROMPTS, "next": "get_name"},
            {"text": FAREWELLS, "next": "goodbye"},
        ],
    },
    "get_name": {
        "text": GET_NAME_RESPONSES,
        "choices": [
            {"text": GET_NAME_WRAP, "next": "goodbye"},
        ],
    },
    "goodbye": {
        "text": FAREWELLS,
        "choices": [
            {"text": FAREWELLS, "next": None},
        ],
    },
    "annoy": {
        "text": ANNOY_MESSAGES,
        "choices": [
            {"text": APOLOGY_MESSAGES, "next": None},
        ],
    },
}
