import base64
from io import BytesIO
from PIL import Image
import requests
import time
import streamlit as st


def test_api_key(api_key: str):
    """Quick check to confirm a Groq key is valid."""
    key = api_key.strip()
    if not key.startswith("gsk_"):
        return False, "That doesn't look like a Groq key — it should start with 'gsk_'."
    try:
        resp = requests.get(
            "https://api.groq.com/openai/v1/models",
            headers={"Authorization": f"Bearer {key}"},
            timeout=15
        )
        if resp.status_code == 200:
            return True, "Key is valid and working."
        elif resp.status_code == 401:
            return False, "Groq says this key is invalid or revoked. Generate a new one at console.groq.com/keys."
        else:
            return False, f"Unexpected response ({resp.status_code}): {resp.text[:200]}"
    except requests.exceptions.RequestException as e:
        return False, f"Network error reaching Groq: {e}"


def format_result(text: str) -> str:
    """Guarantee the doctor disclaimer is always present, regardless of what the model outputs."""
    disclaimer = "This is not a diagnosis, please discuss these results with your doctor."
    if disclaimer.lower() not in text.lower():
        text = text.rstrip() + f"\n\n---\n**{disclaimer}**"
    return text


def build_payload(img_b64: str) -> dict:
    prompt_text = (
        "You are a friendly medical assistant explaining results to someone with NO medical background. "
        "Use simple, everyday language, avoid jargon, or if you must use a medical term, immediately explain "
        "it in plain words. Use short bullet points, and for each point add one brief clause explaining WHY "
        "it matters (not just WHAT it is), while still keeping the full answer within 1000 output tokens.\n\n"
        "If it is a MEDICINE, cover briefly using markdown headers like '### 1. What it treats':\n"
        "1. What it treats and how it works\n"
        "2. When it's prescribed\n"
        "3. How to take it (dosage basics)\n"
        "4. Side effects to watch for (common and serious)\n"
        "5. Who should NOT take it\n"
        "6. What to avoid while taking it (food and drugs)\n"
        "7. How to store it\n\n"
        "If it is a LAB REPORT, use markdown headers for:\n"
        "1. Biomarker results (number, and whether Normal, High, or Low)\n"
        "2. What abnormal values mean, in one simple sentence each\n"
        "3. Overall summary in plain language, avoiding scary diagnostic labels"
    )

    return {
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
        "max_tokens": 950,
        "temperature": 0.2,
        "reasoning_effort": "none"
    }


def analyze_health_document_openai(image: Image.Image, api_key: str = None) -> str:
    key = (api_key or st.secrets.get("GROQ_API_KEY", "")).strip()
    if not key:
        raise Exception("No API key configured. Set GROQ_API_KEY in Streamlit secrets.")

    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")

    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_b64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }

    payload = build_payload(img_b64)

    last_error = None

    for attempt in range(3):
        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=60
            )
        except requests.exceptions.RequestException as e:
            last_error = str(e)
            time.sleep(2)
            continue

        if response.status_code == 200:
            data = response.json()
            result_text = data["choices"][0]["message"]["content"]
            return format_result(result_text)

        if response.status_code == 401:
            raise Exception("Invalid API Key. Go to console.groq.com/keys, generate a fresh key.")

        if response.status_code == 429:
            error_data = response.json().get("error", {})
            msg = error_data.get("message", "")
            last_error = msg
            if "try again in" in msg:
                try:
                    delay = float(msg.split("try again in")[1].split("s")[0].strip())
                except Exception:
                    delay = 30
                if attempt < 2:
                    time.sleep(delay + 1)
                    continue
            raise Exception(f"Rate limit hit: {msg}")

        if response.status_code == 503:
            last_error = "Model temporarily overloaded (503)."
            if attempt < 2:
                time.sleep((2 ** attempt) * 2)
                continue
            raise Exception(
                "The AI model is temporarily overloaded on Groq's end. "
                "This usually clears up within a minute — please try again shortly."
            )

        last_error = f"Groq Error {response.status_code}: {response.text}"
        raise Exception(last_error)

    raise Exception(f"Analysis failed after multiple retries. Last error: {last_error}")
