# DeepSearch

DeepSearch is an attractive, terminal-first deep research assistant built with Google ADK.  
It converts a plain question into a structured, high-signal answer:

- Quick Summary
- Key Points
- Deep Dive
- Final Takeaway

When a Gemini model is selected, DeepSearch can use Google Search tool calls for live sources.  
When a Gemma model is selected, it automatically disables search tools to avoid compatibility failures.

---

## Highlights

- Clean CLI UX with `rich`
- Structured output format for better readability
- Model-aware tool gating (Gemini: search on, Gemma: search off)
- Easy `.env` configuration
- Works well for quick research workflows and note-taking

---

## Architecture

```text
User Input (CLI)
    |
    v
cli.py
    |
    v
agent.py (ADK LlmAgent)
    |- instruction template
    |- model from RESEARCH_MODEL
    |- tools:
         - Gemini models -> [google_search]
         - Gemma models  -> []
    |
    v
Runner + Session Service
    |
    v
Structured Response
```

---

## Project Structure

```text
deep_research_agent/
├── agent.py          # Agent definition and model/tool logic
├── cli.py            # Interactive CLI loop and rendering
├── requirements.txt  # Python dependencies
├── .env.example      # Safe env template
└── README.md         # Documentation
```

---

## Quick Start

### 1) Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies

```bash
python3 -m pip install -r requirements.txt
```

### 3) Configure environment

```bash
cp .env.example .env
```

Set values in `.env`:

```env
GOOGLE_API_KEY=YOUR_NEW_KEY
GOOGLE_GENAI_USE_VERTEXAI=FALSE
RESEARCH_MODEL=gemma-3-27b-it
```

### 4) Run

```bash
set -a; source .env; set +a; python3 cli.py
```

---

## CLI Commands

| Command | Description |
|---|---|
| `/help` | Show command help |
| `/clear` | Clear terminal screen |
| `/new` | Start a fresh session |
| `/model` | Show active model |
| `/exit` | Quit the app |

---

## Model Options

Pick a model by setting `RESEARCH_MODEL` in `.env`.

| Model ID | Search Tool Support | Best For |
|---|---|---|
| `gemma-3-27b-it` | No | Stable structured responses with lower cost |
| `gemma-3-12b-it` | No | Faster responses |
| `gemini-2.0-flash` | Yes | Source-backed research with web tool calls |

### Compatibility note

Gemma models currently do not support the ADK Google Search tool in this project flow.  
DeepSearch handles this automatically in code.

---

## Example Session

```text
🔬 DeepSearch > Explain quantum computing in simple words with examples
```

Expected shape:

- Topic
- Quick Summary
- Key Points
- Deep Dive
- Final Takeaway

---

## Troubleshooting

### 1) `API key not valid`

- Verify `.env` has a real key (not placeholder)
- Regenerate key at [Google AI Studio API Key](https://aistudio.google.com/apikey)
- Reload environment and run again

### 2) `429 RESOURCE_EXHAUSTED`

Your project/key quota is exhausted.

- Rate limits: [Gemini API rate limits](https://ai.google.dev/gemini-api/docs/rate-limits)
- Usage dashboard: [AI Dev rate-limit dashboard](https://ai.dev/rate-limit)
- Retry after the delay shown in the error message

### 3) `Google search tool is not supported for model ...`

- Use a Gemini model if you need live web search (`gemini-2.0-flash`)
- Or keep Gemma and run without search tool support

---

## Security Best Practices

- Never commit real API keys
- Keep `.env` private
- Rotate keys immediately if exposed
- Use `.env.example` with placeholders only

---

## Roadmap

- Save results to markdown files
- Add streaming output mode
- Add model fallback strategy
- Add persistent session history
- Add prompt presets for common research tasks

---

## Credits

Built by Gokulakrishnan.
# 🔬 DeepSearch — Deep Research Agent CLI

> Point-by-point research answers with sources, powered by **Google Gemma 4** via **Google ADK**

```
  ██████╗ ███████╗███████╗██████╗ ███████╗███████╗ █████╗ ██████╗  ██████╗██╗  ██╗
  ██╔══██╗██╔════╝██╔════╝██╔══██╗██╔════╝██╔════╝██╔══██╗██╔══██╗██╔════╝██║  ██║
  ██║  ██║█████╗  █████╗  ██████╔╝███████╗█████╗  ███████║██████╔╝██║     ███████║
  ██║  ██║██╔══╝  ██╔══╝  ██╔═══╝ ╚════██║██╔══╝  ██╔══██║██╔══██╗██║     ██╔══██║
  ██████╔╝███████╗███████╗██║     ███████║███████╗██║  ██║██║  ██║╚██████╗██║  ██║
  ╚═════╝ ╚══════╝╚══════╝╚═╝     ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
```

## ✨ What It Does

DeepSearch is a CLI-based deep research agent that:

- 📌 **Breaks down answers point-by-point** — clear, numbered key points
- 🔗 **Provides source links** — real URLs from web search, not hallucinated
- 📋 **Gives a quick summary** — 2-3 sentences you can understand instantly
- 🧠 **Deep-dives the topic** — explains like you're 16, no jargon
- ✅ **Final takeaway** — the single most important thing to know

---

## 📁 Project Structure

```
deep_research_agent/
├── agent.py          # Core agent logic (ADK + Gemma 4)
├── cli.py            # CLI interface with rich terminal UI
├── requirements.txt  # Python dependencies
├── .env.example      # Environment variable template
└── README.md         # This file
```

---

## 🚀 Quick Start

### 1. Clone / Set up

```bash
cd deep_research_agent
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Get Your API Key

1. Go to **[https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)**
2. Create a free API key (no credit card needed)
3. Copy the key

### 4. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and paste your key:
```env
GOOGLE_API_KEY=AIzaSy...your_actual_key_here
GOOGLE_GENAI_USE_VERTEXAI=FALSE
RESEARCH_MODEL=gemma-3-27b-it
```

### 5. Run DeepSearch

```bash
# Load env and run
export $(cat .env | xargs) && python cli.py

# Or set key directly
GOOGLE_API_KEY=your_key python cli.py
```

---

## 💬 Usage

Once running, just type your research question:

```
🔬 DeepSearch > What is quantum computing and how does it work?
🔬 DeepSearch > Latest AI breakthroughs in 2025
🔬 DeepSearch > Explain blockchain simply with real examples
🔬 DeepSearch > How does CRISPR gene editing work?
```

### CLI Commands

| Command   | Description                        |
|-----------|------------------------------------|
| `/help`   | Show help and available commands   |
| `/clear`  | Clear the terminal screen          |
| `/new`    | Start a fresh session (new history)|
| `/model`  | Show which model is active         |
| `/exit`   | Quit DeepSearch                    |

---

## 🤖 Model Options

Edit `RESEARCH_MODEL` in your `.env`:

| Model                              | Speed   | Quality | Notes                    |
|------------------------------------|---------|---------|--------------------------|
| `gemma-3-27b-it`                   | Medium  | ⭐⭐⭐⭐⭐ | Best open model (default)|
| `gemma-3-12b-it`                   | Fast    | ⭐⭐⭐⭐  | Lighter, still great     |
| `gemini-2.0-flash`                 | Fast    | ⭐⭐⭐⭐⭐ | Gemini — very capable    |
| `gemini-2.5-flash-preview-04-17`   | Fast    | ⭐⭐⭐⭐⭐ | Latest Gemini Flash      |

---

## 📤 Example Output

```markdown
### 🔍 TOPIC: What is quantum computing?

---

### 📋 QUICK SUMMARY
Quantum computing uses quantum mechanics to process information in ways 
classical computers can't. Instead of bits (0 or 1), it uses "qubits" 
that can be both at once, making it exponentially more powerful for 
certain problems.

---

### 📌 KEY POINTS

**Point 1: What is a Qubit?**
→ Unlike classical bits that are 0 OR 1, qubits can be 0, 1, or both 
  simultaneously (called superposition). This is the core difference.
🔗 Source: https://quantum.google/learn/

**Point 2: Why It Matters**
→ Quantum computers can solve certain problems millions of times faster 
  than any classical computer — like breaking encryption or drug discovery.
🔗 Source: https://www.ibm.com/quantum

...

### ✅ FINAL TAKEAWAY
Quantum computing isn't just a faster computer — it's a fundamentally 
different way of processing information that will transform cryptography, 
medicine, and AI.
```

---

## 🛠 How It Works

```
User Query
    │
    ▼
Google ADK Runner
    │
    ├── LlmAgent (Gemma 4 / Gemini)
    │       └── System Prompt: structured research format
    │
    └── google_search Tool
            └── Live web search for real sources
                    │
                    ▼
            Structured Response:
            Summary → Key Points → Deep Dive → Takeaway
```

---

## 📦 Dependencies

- **[google-adk](https://github.com/google/adk-python)** — Google Agent Development Kit
- **[google-genai](https://pypi.org/project/google-genai/)** — Google AI Python SDK
- **[rich](https://rich.readthedocs.io/)** — Beautiful terminal output
- **python-dotenv** — Environment variable loading

---

## 🔑 Free Tier Info

Google AI Studio offers a **free tier** with Gemma models:
- ✅ No credit card required
- ✅ Generous rate limits for personal use
- ✅ Access to Gemma 3 (27B, 12B) and Gemini Flash
- 🔗 Get key: [aistudio.google.com/apikey](https://aistudio.google.com/apikey)

---

## 🧑‍💻 Built With

- Google ADK v1.30+ (with Gemma 4 support added in v1.30)
- Google Gemma 3/4 models via Gemini API
- Rich terminal UI
- Python asyncio for async ADK runner

---

*Built by Gokulakrishnan | gokulakrishnan.dev*