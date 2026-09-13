# ⚡ Anakin Sentinel: Autonomous Read-Reason-Act Engine

Built for the **Anakin Forge Hackathon**.

Anakin Sentinel goes beyond chatbots. It is a fully autonomous agent that browses live web pages, reasons through multi-step analytical challenges, and takes concrete real-world actions without human intervention.

## 🚀 Live Run Highlights
In a single prompt, Sentinel autonomously:
1. **READ**: Extracted real-time unstructured content from Hacker News.
2. **REASON**: Analyzed and prioritized top AI/DevTool breakthroughs using **Gemini 2.5 Flash**.
3. **ACT**: 
   - Synthesized and saved a persistent report (`agent_verdict.md`).
   - Dispatched structured completion webhooks to external endpoints.

## 🛠️ Stack & Architecture
- **Reasoning Core**: Gemini 2.5 Flash (via `google-genai`)
- **Web Reader**: BeautifulSoup4 + Anakin Scraper compatibility layer
- **Action Dispatcher**: Native HTTP Webhook & Local Persistence Engine

## 💻 Quickstart
```bash
pip install -r requirements.txt
export GEMINI_API_KEY="your-api-key"
python agent.py
