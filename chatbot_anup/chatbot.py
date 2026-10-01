import os
import sys
from mistralai import Mistral

MISTRAL_API_KEY = os.environ.get("MISTRAL_API_KEY", "")

SYSTEM_PROMPT = """You are RoboMind, an expert AI assistant specializing in AI integration in robotics.
You have deep knowledge in:
- Robot Operating System (ROS / ROS2)
- Computer vision for robots (YOLO, OpenCV, depth sensors)
- Motion planning and control (MoveIt, PID, trajectory planning)
- Sensor fusion (IMU, LiDAR, camera, ultrasonic)
- Machine learning for robotics (reinforcement learning, imitation learning)
- Autonomous navigation (SLAM, path planning, A*, Dijkstra)
- Manipulation and grasping
- Human-robot interaction
- Industrial robotics (cobots, PLCs, Industry 4.0)
- Drone and UAV systems
- Embedded AI (NVIDIA Jetson, Raspberry Pi, edge inference)
- Popular frameworks: PyTorch, TensorFlow, OpenAI Gym, Stable-Baselines3

For every response, write a detailed, well-structured answer of 2000 to 4000 words.
Structure your answers with clear headings (##), subheadings, bullet points, and code snippets where relevant.
Always relate your answers to practical robotics applications and real-world use cases.
Cover theory, implementation details, tools/frameworks, and best practices in each response."""

def print_banner():
    print("=" * 60)
    print("   RoboMind — AI Integration in Robotics Chatbot")
    print("   Powered by Mistral AI")
    print("=" * 60)
    print("Type 'exit' or 'quit' to end the session.")
    print("Type 'clear' to reset conversation history.")
    print("=" * 60)
    print()

def chat():
    if not MISTRAL_API_KEY:
        print("[ERROR] MISTRAL_API_KEY environment variable is not set.")
        print("Set it with:  set MISTRAL_API_KEY=your_key_here")
        sys.exit(1)

    client = Mistral(api_key=MISTRAL_API_KEY)
    model = "mistral-large-latest"
    history = []

    print_banner()
    print(f"Model: {model}")
    print()

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nGoodbye! Keep building robots!")
            break

        if not user_input:
            continue

        if user_input.lower() in ("exit", "quit"):
            print("\nGoodbye! Keep building robots!")
            break

        if user_input.lower() == "clear":
            history.clear()
            print("[Conversation history cleared]\n")
            continue

        history.append({"role": "user", "content": user_input})

        try:
            response = client.chat.complete(
                model=model,
                messages=[{"role": "system", "content": SYSTEM_PROMPT}] + history,
            )
            assistant_msg = response.choices[0].message.content
            history.append({"role": "assistant", "content": assistant_msg})
            print(f"\nRoboMind: {assistant_msg}\n")
        except Exception as e:
            print(f"\n[ERROR] Mistral API call failed: {e}\n")
            history.pop()

if __name__ == "__main__":
    chat()
