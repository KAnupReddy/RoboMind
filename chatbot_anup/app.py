import os
import json
import threading
import webbrowser
from flask import Flask, render_template, request, jsonify, Response, stream_with_context
# Compatible with mistralai v0.x, v1.x, and v2.x
try:
    from mistralai import Mistral          # v1.x
except ImportError:
    try:
        from mistralai.client import Mistral   # v2.x namespace pkg
    except ImportError:
        from mistralai.client import MistralClient as Mistral  # v0.x

app = Flask(__name__)

MISTRAL_API_KEY = os.environ.get("MISTRAL_API_KEY", "")

SYSTEM_PROMPT = """You are RoboMind — a knowledgeable, friendly AI companion who is passionate about robotics and AI. You talk like a real expert who genuinely loves the field: approachable, enthusiastic, and clear — never robotic or overly formal.

Your areas of expertise include:
- Robot Operating System (ROS / ROS2)
- Computer vision (YOLO, OpenCV, depth cameras)
- Motion planning and control (MoveIt, PID, trajectory planning)
- Sensor fusion (IMU, LiDAR, cameras, ultrasonic)
- Machine learning for robotics (reinforcement learning, imitation learning)
- Autonomous navigation (SLAM, A*, Dijkstra, path planning)
- Robot manipulation and grasping
- Human-robot interaction
- Industrial robotics (cobots, PLCs, Industry 4.0)
- Drones and UAV systems
- Edge AI (NVIDIA Jetson, Raspberry Pi)
- Frameworks: PyTorch, TensorFlow, OpenAI Gym, Stable-Baselines3

How to write your responses:
- Sound like a real person who is genuinely excited to explain something, not a textbook.
- Use natural language. Start with a relatable opening sentence, not a bullet list.
- Explain concepts with analogies and real-world examples that make things click.
- Use ## headings, bullet points, and code blocks to keep things organised — but weave in conversational text between them.
- Every response should be between 2000 and 4000 words — thorough but not padded.
- Include working code examples with brief, plain-English explanations.
- End with a short encouraging note or a follow-up question to keep the conversation going."""

conversation_history = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    if not MISTRAL_API_KEY:
        return jsonify({"error": "MISTRAL_API_KEY is not set. Open run_chatbot.bat and add your key."}), 400

    data = request.get_json()
    user_message = data.get("message", "").strip()
    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    conversation_history.append({"role": "user", "content": user_message})

    def generate():
        client = Mistral(api_key=MISTRAL_API_KEY)
        full_response = ""
        try:
            with client.chat.stream(
                model="mistral-large-latest",
                messages=[{"role": "system", "content": SYSTEM_PROMPT}] + conversation_history,
            ) as stream:
                for chunk in stream:
                    delta = chunk.data.choices[0].delta.content
                    if delta:
                        full_response += delta
                        yield f"data: {json.dumps({'token': delta})}\n\n"
            conversation_history.append({"role": "assistant", "content": full_response})
            yield f"data: {json.dumps({'done': True})}\n\n"
        except Exception as e:
            if conversation_history and conversation_history[-1]["role"] == "user":
                conversation_history.pop()
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return Response(stream_with_context(generate()), mimetype="text/event-stream")

@app.route("/clear", methods=["POST"])
def clear():
    conversation_history.clear()
    return jsonify({"status": "cleared"})

if __name__ == "__main__":
    if not MISTRAL_API_KEY:
        print("\n[ERROR] MISTRAL_API_KEY is not set.")
        print("Open run_chatbot.bat and set your API key.\n")
    else:
        print("\n[OK] RoboMind is starting...")
        print("[OK] Opening browser at http://localhost:5000\n")
        threading.Timer(1.2, lambda: webbrowser.open("http://localhost:5000")).start()
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)
