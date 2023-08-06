import random
import openai

THEMES = ['Personal Growth',
    'Overcoming Adversity',
    'Entrepreneurship',
    'Mindfulness and Wellness',
    'Perseverance',
    'Self-confidence',
    'Creativity',
    'Leadership',
    'Success and Achievement',
    'Teamwork and Collaboration',
    'Passion and Drive',
    'Kindness and Compassion',
    'Learning and Growth Mindset',
    'Time Management and Productivity',
    'Courage and Bravery',
    'Positive Thinking and Attitude',
    'Adaptability and Flexibility',
    'Diversity and Inclusion',
    'Gratitude and Appreciation',
    'Resilience and Grit'
]

TONES = ['Encouraging',
    'Empathetic',
    'Resilient',
    'Inspiring',
    'Confident',
    'Visionary',
    'Calming',
    'Serene',
    'Uplifting',
    'Supportive',
    'Determined',
    'Cheerful',
    'Energetic',
    'Passionate',
    'Reflective',
    'Motivating',
    'Bold',
    'Optimistic',
    'Hopeful',
    'Thought-provoking',
    'Humorous',
    'Honest',
    'Nurturing',
    'Ambitious',
    'Bold',
    'Transformative',
    'Reassuring',
    'Motivational',
    'Appreciative',
    'Inspirational',
    'Practical',
    'Thoughtful',
    'Sincere',
    'Upbeat',
    'Inquisitive',
    'Dreamy',
    'Patient',
    'Soothing',
    'Straightforward',
    'Honest',
    'Transformative',
    'Confident',
    'Goal-oriented',
    'Empowering',
    'Optimistic',
    'Visionary',
    'Practical',
    'Enthusiastic',
    'Refreshing',
    'Playful'
]

# Get the openai key
def motivate(
    openai_key: str,
    type: str = 'one-liner', # either quote or one liner
    n_words: int = 30,
):
    """Motivate the user by pinging the OpenAI
    """
    
    # Users can customize 
    type_of_motivation = ['quote', 'one-liner']
    if type.lower() not in type_of_motivation:
        raise ValueError(f"{type} is not a valid motivation type.")
    
    theme = THEMES[random.randint(0, len(THEMES) - 1)]
    tone = TONES[random.randint(0, len(TONES) - 1)]
    
    prompt = f"Give me a {type} motivation words with the theme {theme} and tone of {tone} in under {n_words} words. \
    Do not include anything else besides the {type}. Do not go above {n_words} words."    
    
    if type == 'quote': # sometimes it'll kick back "unknown" for a quote. I don't like this.
        prompt += " If the quote is unknown, find a different quote using a theme of your choice and a tone of your choice."
    
    # make the request
    openai.api_key = openai_key
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [
            {
                "role" : "system",
                "content" : f"You are to trying to encourage me by providing a motivational {type}." 
            },
            {
                "role" : "user",
                "content" : prompt
            }
        ]
    )
    
    print(response["choices"][0]["message"]["content"])