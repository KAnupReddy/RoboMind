# 🤖 RoboMind — AI Robotics Chatbot

RoboMind is an AI chatbot focused on **AI integration in robotics**. It runs as a local Flask web app (with a CLI version too) and uses **Mistral AI** (`mistral-large-latest`) to give detailed, friendly, expert-level answers on robotics topics.

## ✨ Features

- 💬 **Streaming responses** — answers appear token by token in the browser (Server-Sent Events)
- 🧠 **Conversation memory** — keeps context across the whole chat session
- 🌐 **Web UI** — dark, sci-fi themed chat interface with quick topics, model info and session stats
- ⌨️ **CLI mode** — chat from the terminal with `chatbot.py`
- 🪟 **One-click launch on Windows** — `run_chatbot.bat` finds Python (or downloads a portable one), installs dependencies and opens the browser
- 📚 **Robotics expertise** — ROS/ROS2, computer vision, motion planning, SLAM, sensor fusion, reinforcement learning, drones/UAV, edge AI (Jetson, Raspberry Pi) and more

## 🧰 Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python 3.8+, Flask |
| LLM | Mistral AI (`mistralai` SDK), model `mistral-large-latest` |
| Frontend | HTML, CSS, JavaScript, marked.js, highlight.js |

## 📁 Project Structure

```
chatbot_anup/
├── app.py              # Flask web server (streaming chat API)
├── chatbot.py          # Command-line version of the chatbot
├── requirements.txt    # Python dependencies
├── run_chatbot.bat     # Windows launcher (sets up Python + runs app)
├── templates/
│   └── index.html      # Web chat interface
└── static/             # Static assets
```

## 🚀 Getting Started

### 1. Get a Mistral API key

Create a free key at [console.mistral.ai](https://console.mistral.ai/).

### 2. Clone the repo

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set your API key as an environment variable

**Windows (Command Prompt):**
```bat
set MISTRAL_API_KEY=your_key_here
```

**Windows (PowerShell):**
```powershell
$env:MISTRAL_API_KEY="your_key_here"
```

**macOS / Linux:**
```bash
export MISTRAL_API_KEY=your_key_here
```

### 5. Run it

**Web app:**
```bash
python app.py
```
Then open **http://localhost:5000** (it also opens automatically).

**Terminal version:**
```bash
python chatbot.py
```
Type `clear` to reset the conversation and `exit` / `quit` to leave.

### Windows shortcut

Edit `run_chatbot.bat` and set your key on the `set MISTRAL_API_KEY=` line, then double-click it. It installs everything and launches the app for you.

> ⚠️ **Never commit your real API key.** Keep `run_chatbot.bat` in the repo with a placeholder (`your_key_here`) only.

## 🔌 API Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| `GET` | `/` | Serves the chat UI |
| `POST` | `/chat` | Sends `{"message": "..."}` and streams the reply as Server-Sent Events |
| `POST` | `/clear` | Clears the conversation history |

## ⚙️ Configuration

- **Model:** change `model="mistral-large-latest"` in `app.py` / `chatbot.py`
- **Personality & answer length:** edit `SYSTEM_PROMPT` in `app.py` / `chatbot.py`
- **Port:** change `port=5000` at the bottom of `app.py`

## 🛣️ Possible Improvements

- Per-user sessions (conversation history is currently shared across all visitors)
- Save / export chat history
- Support for other LLM providers

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.

## 📄 License

Add a license of your choice (e.g. MIT) in a `LICENSE` file.

## 👤 Author

**Anup Reddy** — [GitHub](https://github.com/<your-username>)

---

⭐ If you like this project, give it a star!
