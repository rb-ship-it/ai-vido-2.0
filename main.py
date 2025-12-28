import os
import time
from google import genai
from google.genai import types

# The client automatically picks up GEMINI_API_KEY from your GitHub Secrets
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def get_funny_trends_and_image():
    # 1. Generate the Roast using the latest Flash model
    text_model = "gemini-2.0-flash"
    text_prompt = "List 1 trending AI video technology today and write a hilarious one-sentence roast."
    
    print(f"Generating roast with {text_model}...")
    text_response = client.models.generate_content(
        model=text_model, 
        contents=text_prompt
    )
    roast_text = text_response.text

    # 2. Generate the Meme Thumbnail
    # We use the specialized 2.5-flash-image model (formerly "nano banana")
    image_model = "gemini-2.5-flash-image"
    image_prompt = f"A hilarious, high-quality meme image about: {roast_text}. Funny cartoon style."
    
    print(f"Generating image with {image_model}...")
    image_response = client.models.generate_content(
        model=image_model,
        contents=image_prompt,
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE"],
            image_config=types.ImageConfig(aspect_ratio="1:1")
        )
    )

    # 3. Save the image file locally for GitHub to find
    for part in image_response.parts:
        if part.inline_data:
            with open("trend_thumb.png", "wb") as f:
                f.write(part.as_bytes())
    
    return roast_text

def update_readme(roast):
    header = "# 🎬 ai-vido-2.0: Daily Funny Trends\n\n"
    # This line embeds the image in your GitHub front page
    image_md = "![Today's Roast](trend_thumb.png)\n\n" 
    footer = f"\n\n---\n*Last automated update: {time.strftime('%Y-%m-%d %H:%M:%S')}*"
    
    with open("README.md", "w") as f:
        f.write(header + image_md + roast + footer)

if __name__ == "__main__":
    try:
        roast = get_funny_trends_and_image()
        update_readme(roast)
        print("Success! Trends and image updated.")
    except Exception as e:
        print(f"Automation failed: {e}")
