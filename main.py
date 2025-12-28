import os
import requests
from google import genai

# Setup Gemini Client
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def get_funny_trends():
    # Simple example: fetching AI topics from a news or github source
    # For now, we'll prompt Gemini to 'summarize' the state of AI video
    prompt = "Give me 3 trending AI video technologies right now and write a 1-sentence sarcastic/funny roasting of each for my GitHub README."
    
    response = client.models.generate_content(
        model="gemini-2.0-flash", 
        contents=prompt
    )
    
    return response.text

def update_readme(content):
    header = "# 🎬 ai-vido-2.0: Daily Funny Trends\n\n"
    with open("README.md", "w") as f:
        f.write(header + content + "\n\n*Last updated: auto-magically today.*")

if __name__ == "__main__":
    funny_content = get_funny_trends()
    update_readme(funny_content)
