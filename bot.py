import os
import json
import random
import time
from google import genai

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def run_daily_bot():
    # 1. Load your curated list
    with open("trends.json", "r") as f:
        trends = json.load(f)
    
    # 2. Pick a random meme/trend
    selected = random.choice(trends)
    topic = selected["topic"]
    
    # 3. Generate Content
    model_id = "gemini-1.5-flash"
    roast_prompt = f"Write a hilarious one-sentence roast about: {topic}."
    roast = client.models.generate_content(model=model_id, contents=roast_prompt).text

    image_prompt = f"A funny meme image about {topic}. Cartoon style."
    image_response = client.models.generate_content(
        model="gemini-2.0-flash-exp", 
        contents=image_prompt,
        config={'response_modalities': ["IMAGE"]}
    )

    # 4. Save Image
    for part in image_response.parts:
        if part.inline_data:
            with open("trend_thumb.png", "wb") as f:
                f.write(part.as_bytes())

    # 5. Update README
    with open("README.md", "w") as f:
        f.write(f"# 🎬 Daily AI Roast\n\n![Meme](trend_thumb.png)\n\n**Topic:** {topic}\n\n**Roast:** {roast}")

if __name__ == "__main__":
    run_daily_bot()
