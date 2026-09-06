import base64
from io import BytesIO
from PIL import Image
import requests
import time
import streamlit as st
import re

# Safe fallback mechanism supporting both local development and Streamlit Cloud secrets
try:
    GROQ_API_KEY = st.secrets.get("your api key", "")
except Exception:
    GROQ_API_KEY = "your api key"  # Replace with your actual API key for local development

def analyze_health_document_openai(image: Image.Image, api_key: str = None) -> str:
    key = (api_key or GROQ_API_KEY).strip()
    if not key:
        raise Exception("No API key set.")

    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")

    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_b64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }

    prompt_text = (
        "You are a friendly medical assistant explaining results to someone with NO medical background. "
        "Use simple, everyday language, avoid jargon, or if you must use a medical term, immediately explain "
        "it in plain words. Be concise, use short bullet points not paragraphs, so the full answer fits "
        "within 1000 output tokens without getting cut off.\n\n"
        "If it is a MEDICINE, cover briefly in plain language:\n"
        "1. What it treats and how it works\n"
        "2. When it's prescribed\n"
        "3. How to take it (dosage basics)\n"
        "4. Side effects to watch for (common and serious)\n"
        "5. Who should NOT take it\n"
        "6. What to avoid while taking it (food and drugs)\n"
        "7. How to store it\n\n"
        "If it is a LAB REPORT, for each value:\n"
        "- Show the number and whether it's Normal, High, or Low\n"
        "- In ONE simple sentence, explain what that means if abnormal (skip normal values)\n"
        "Then end with:\n"
        "- A short plain-language summary avoiding scary diagnostic labels\n"
        "- This line exactly: This is not a diagnosis, please discuss these results with your doctor."
    )

    payload = {
        "model": "qwen/qwen3.6-27b",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_text},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}
                ]
            }
        ],
        "max_tokens": 1000,
        "temperature": 0.2
    }

    for attempt in range(3):
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )

        if response.status_code == 200:
            raw_content = response.json()["choices"][0]["message"]["content"]
            
            # Clean out any accidental <think>...</think> blocks from the response
            cleaned_content = re.sub(r'<think>.*?</think>', '', raw_content, flags=re.DOTALL).strip()
            return cleaned_content

        elif response.status_code == 401:
            raise Exception("Invalid API Key. Generate a fresh key at console.groq.com/keys.")
        elif response.status_code == 429:
            time.sleep(10)
            continue
        elif response.status_code == 503:
            time.sleep(5)
            continue

        raise Exception(f"Groq Error {response.status_code}: {response.text}")

    raise Exception("Analysis failed after multiple retries.")