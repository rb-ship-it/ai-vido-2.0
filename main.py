import os
import time
import base64
from google import genai

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def get_funny_trends_and_image():
    # Use 1.5-flash for the text roast
    text_prompt = "List 1 trending AI video tech today and write a hilarious one-sentence roast."
    text_response = client.models.generate_content(model="gemini-1.5-flash", contents=text_prompt)
    roast_text = text_response.text

    # Use Nano Banana (2.5-flash-image) for the thumbnail
    image_prompt = f"A hilarious, high-quality cartoon meme of: {roast_text}. Cinematic lighting, funny style."
    print("Generating thumbnail...")
    
    image_response = client.models.generate_content(
        model="gemini-1.5-flash-latest"", # Use the specialized image model
        contents=image_prompt,
        config={"response_modalities": ["IMAGE"]} # Request image output
    )

    # Save the generated image to your repo
    for part in image_response.parts:
        if part.inline_data:
            with open("trend_thumb.png", "wb") as f:
                f.write(part.as_bytes())
    
    return roast_text

def update_readme(roast):
    header = "# 🎬 ai-vido-2.0: Daily Funny Trends\n\n"
    # Display the image in the README using Markdown
    image_md = "![Today's Roast](trend_thumb.png)\n\n" 
    footer = f"\n\n---\n*Last automated update: {time.strftime('%Y-%m-%d %H:%M:%S')}*"
    
    with open("README.md", "w") as f:
        f.write(header + image_md + roast + footer)

if __name__ == "__main__":
    roast = get_funny_trends_and_image()
    update_readme(roast)
