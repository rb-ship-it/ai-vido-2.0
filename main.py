import os
import time
from google import genai
from google.genai import errors

# Initialize the client
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def get_funny_trends():
    # We switch to 1.5-flash as it has higher reliability for free tier
    model_id = "gemini-1.5-flash"
    prompt = "List 3 current trending AI video technologies. For each, write a one-sentence hilarious or sarcastic roast. Use Markdown formatting."

    # Retry logic: If it fails, wait 30 seconds and try one more time
    for attempt in range(2):
        try:
            print(f"Attempt {attempt + 1}: Contacting {model_id}...")
            response = client.models.generate_content(
                model=model_id,
                contents=prompt
            )
            return response.text
        except errors.ClientError as e:
            if "429" in str(e) and attempt == 0:
                print("Quota hit. Sleeping for 30 seconds before retry...")
                time.sleep(30)
            else:
                return f"AI is currently tired (Error: {e}). Check back later!"

def update_readme(content):
    header = "# 🎬 ai-vido-2.0: Daily Funny Trends\n\n"
    footer = f"\n\n---\n*Last automated update: {time.strftime('%Y-%m-%d %H:%M:%S')}*"
    with open("README.md", "w") as f:
        f.write(header + content + footer)

if __name__ == "__main__":
    funny_content = get_funny_trends()
    update_readme(funny_content)
