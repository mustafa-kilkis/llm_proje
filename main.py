import os
from dotenv import load_dotenv
from scraper import fetch_website_contents
from openai import OpenAI

# Load environment variables (fetches API key from .env file if present)
load_dotenv(override=True)

# ----------------------------------------------------
# 1. PROVIDER CONFIGURATION (Gemini vs. Ollama)
# ----------------------------------------------------
# USE_OLLAMA acts as a toggle. Set to True for local execution, False for cloud.
USE_OLLAMA = True

if USE_OLLAMA:
    gemini_client = OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama"  # Local models do not require a valid API key
    )
    MODEL_NAME = "llama3.2"
else:
    gemini_client = OpenAI(
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        api_key=os.getenv("GEMINI_API_KEY")
    )
    MODEL_NAME = "models/gemini-3.7-flash"

# ----------------------------------------------------
# 2. PROMPT ENGINEERING & TEMPLATES
# ----------------------------------------------------
SYSTEM_PROMPT = """
Sen bir yazılım uzmanısın ve web sitelerini tararken özetler veriyorsun.
"""

USER_PROMPT_PREFIX = """
Burada bir web sitesinin içeriği var. Bu web sitesinin özetini ver:
"""

def messages_for(website_content):
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": USER_PROMPT_PREFIX + website_content}
    ]

# ----------------------------------------------------
# 3. CORE SUMMARIZATION FUNCTION
# ----------------------------------------------------
def summarize(url):
    print(f"[{MODEL_NAME}] ile web sitesi taranıyor: {url}...")
    website_text = fetch_website_contents(url)
    
    response = gemini_client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages_for(website_text)
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    target_url = "https://tr.wikipedia.org/wiki/Anasayfa"
    result = summarize(target_url)
    print("\n--- ÖZET ---\n")
    print(result)