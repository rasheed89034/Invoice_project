# Invoice_project
# 🎙️ AI Voice-to-Invoice Generator (Solar Systems)

An end-to-end, hands-free **AI Voice-to-Invoice Generation Pipeline** engineered for field sales teams in the renewable energy sector. This application captures natural verbal inputs, utilizes Large Language Models (LLMs) for deterministic structured data extraction, features a real-time editable UI sync, and programmatically compiles downloadable PDF invoices.

🚀 **Live Deployment:** [Test the Live App Here](https://invoiceproject-jfdjiampxkreg5owgtbkcu.streamlit.app/)

---

## 🛠️ Tech Stack & Architecture

* **Frontend UI:** `Streamlit` (Session state-driven dynamic 2-column layout)
* **Speech-to-Text (STT):** `OpenAI Whisper (Base Model)` + System-level `FFmpeg`
* **LLM Orchestration:** `LangChain` + `Gemini API` (`gemini-3.1-flash-lite`)
* **Data Validation:** `Pydantic` (Strict schema formatting via `.with_structured_output()`)
* **Document Generation:** `Jinja2` HTML Templating + `xhtml2pdf (Pisa)` 

---

## ⚙️ Core Pipeline Architecture

1. **Audio Streaming:** Captures voice commands via high-stability audio recorder packages or fallback file upload streams (.mp3, .wav).
2. **STT Transcription:** Whisper processes the raw audio bytes inside temporary file streams to output an unformatted string transcript.
3. **Structured NLP Extraction:** LangChain pipes the transcript into Gemini using a specific context window. The model recognizes verbal delimiters like *"next"* and maps verbal tokens directly into structural fields.
4. **Deterministic Calculation:** Streamlit captures the JSON payload, dynamically tracks state updates, handles mathematical syncing (Gross, Balance, Discount), and handles manual overrides seamlessly.
5. **PDF Compilation:** Binds the final JSON dictionary to a Jinja2 template and renders a clean binary stream for automated downloading.

---

## 🚀 Installation & Local Setup

### 1. Prerequisites
Ensure you have **FFmpeg** installed on your system for audio processing:
```bash
# macOS (using Homebrew)
brew install ffmpeg

# Ubuntu/Linux
sudo apt update && sudo apt install ffmpeg
