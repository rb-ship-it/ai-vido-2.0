import os
import time
from google import genai
from google.genai import types

# The client automatically finds your GEMINI_API_KEY from the environment
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def get_funny_trends_and_image():
    # Use 1.5-flash-latest to avoid the 404 error
    model_id = "gemini-1.5-flash-latest"
    
    # 1. Generate the Roast
    prompt = "List 1 trending AI video technology today and write a hilarious one-sentence roast."
    text_response = client.models.generate_content(model=model_id, contents=prompt)
    roast_text = text_response.text

    # 2. Generate the Thumbnail
    image_prompt = f"A hilarious, high-quality meme image about: {roast_text}. Funny cartoon style."
    print("Generating thumbnail...")
    
    image_response = client.models.generate_content(
        model="gemini-2.0-flash-exp", # Experimental image generation model
        contents=image_prompt,
        config=types.GenerateContentConfig(response_modalities=["IMAGE"])
    )

    # 3. Save the image file
    for part in image_response.parts:
        if part.inline_data:
            with open("trend_thumb.png", "wb") as f:
                f.write(part.as_bytes())
    
    return roast_text

def update_readme(roast):
    header = "# 🎬 ai-vido-2.0: Daily Funny Trends\n\n"
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
        print(f"Error occurred: {e}")
