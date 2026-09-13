import os
import json
import requests
from bs4 import BeautifulSoup
from google import genai
from google.genai import types

# ==========================================
# 0. API KEY સેટિંગ
# ==========================================
# અહીં ફક્ત તમારી અંગ્રેજી અક્ષરો વાળી API Key જ મૂકવી (દા.ત. "AIzaSy...")
GEMINI_API_KEY = "તમારી_સાચી_અંગ્રેજી_API_KEY"

# ==========================================
# 1. READ TOOLS
# ==========================================
def read_web_content(url: str) -> str:
    """Read: Fetches and cleans live text content from a web page."""
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        resp = requests.get(url, headers=headers, timeout=12)
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "noscript"]):
            tag.decompose()
        text = soup.get_text(separator=" ", strip=True)
        return text[:4000]
    except Exception as e:
        return f"Error reading URL: {str(e)}"

# ==========================================
# 2. ACT TOOLS
# ==========================================
def trigger_webhook_or_form(endpoint_url: str, payload_json: str) -> str:
    """Act: Sends the finalized reasoning payload to an endpoint."""
    try:
        payload = json.loads(payload_json)
        resp = requests.post(
            endpoint_url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        return f"Action dispatched successfully. Status Code: {resp.status_code}"
    except Exception as e:
        return f"Action execution response: {str(e)}"

def save_structured_decision(filename: str, report_markdown: str) -> str:
    """Act: Persists the strategic report to local storage."""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(report_markdown)
        return f"File '{filename}' successfully saved."
    except Exception as e:
        return f"Error writing file: {str(e)}"

# ==========================================
# 3. AGENT CORE (Gemini 2.5 Flash)
# ==========================================
SYSTEM_PROMPT = """
You are 'Anakin Sentinel' — an Autonomous Agent built for Anakin Forge.
Loop:
1. READ target URLs.
2. REASON through multi-step logic.
3. ACT: Persist reports and trigger dispatch actions.
Complete tasks end-to-end autonomously.
"""

def execute_mission(mission_prompt: str):
    print("==================================================")
    print("🚀 Anakin Sentinel Agent: Mission Started")
    print("==================================================\n")

    # API key ક્લીનિંગ (વધારાની સ્પેસ કે હિડન કેરેક્ટર દૂર કરવા)
    clean_key = GEMINI_API_KEY.strip()

    client = genai.Client(api_key=clean_key)
    tools = [read_web_content, trigger_webhook_or_form, save_structured_decision]

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=mission_prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            tools=tools,
            temperature=0.1
        )
    )

    print("\n==================================================")
    print("🏁 Mission Execution Complete")
    print("==================================================")
    print(response.text)

if __name__ == "__main__":
    sample_mission = (
        "Execute a full agentic pipeline:\n"
        "1. READ the latest headlines from 'https://news.ycombinator.com'.\n"
        "2. REASON and select the top 2 innovations related to AI or DevTools.\n"
        "3. ACT: Save the report to 'agent_verdict.md'.\n"
        "4. ACT: Trigger a webhook to 'https://httpbin.org/post' with the summary payload."
    )
    execute_mission(sample_mission)
