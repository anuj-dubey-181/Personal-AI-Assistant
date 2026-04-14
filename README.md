# 🎙️ Jarvis AI Assistant (GUI Version)
A sophisticated virtual assistant powered by **Python 3**, featuring a real-time **Tkinter** dashboard and **Google Gemini 2.0 lite** for intelligent natural language processing. Unlike traditional voice assistants, this version supports **Persistent Conversation Sessions**, allowing for seamless back-and-forth dialogue without repeated wake-word triggers.
## 🌟 Key Features
 * **Wake-Word Activation:** Listens in standby mode for "Jarvis" to trigger activity.
 * **Continuous Conversation:** Stays active after the first command until dismissed with *"Bye bye Jarvis"*.
 * **AI Intelligence:** Integrated with Google Generative AI for context-aware, concise responses.
 * **System Automation:**
   * Quick-launch commands for Google, YouTube, LinkedIn, and more.
   * Local music library integration for voice-controlled playback.
 * **Real-time Logging:** A dedicated terminal-style dashboard built with Tkinter to track system status and transcription.
 * **Multi-threaded Engine:** Ensures the voice recognition and TTS (Text-to-Speech) processes do not freeze the user interface.
## 🛠️ Tech Stack
 * **Language:** Python 3
 * **GUI:** Tkinter
 * **AI:** Google Gemini (Generative AI SDK)
 * **Speech-to-Text:** SpeechRecognition (Google Web Speech API)
 * **Text-to-Speech:** pyttsx3
 * **Threading:** Python Standard Threading & Queue
## 🚀 Getting Started
### Prerequisites
Ensure you have Python installed, then install the required dependencies:
```bash
pip install speechrecognition pyttsx3 google-generativeai

```
*Note: If you are on Linux, you may need to install portaudio and PyAudio via your package manager.*
### API Configuration
 1. Obtain an API Key from the Google AI Studio.
 2. Open main.py and replace the placeholder in genai.configure:
   ```python
   genai.configure(api_key="YOUR_API_KEY_HERE")
   
   ```
### Music Library Setup
Create a file named musicLibrary.py in the same directory to enable the "Play" feature:
```python
# musicLibrary.py
music = {
    "thunder": "https://www.youtube.com/watch?v=fKopy74weus",
    "skyfall": "https://www.youtube.com/watch?v=sTiJElmQHIs"
}

```
## 🎮 Usage
 1. **Launch:** Run python main.py.
 2. **Initialize:** Click **Start Jarvis** to begin the background listening thread.
 3. **Command:** Say **"Jarvis"** to wake him.
 4. **Interact:** Speak naturally. You can ask multiple questions in a row.
 5. **Dismiss:** Say **"Bye bye Jarvis"** to return the assistant to standby mode.
## ⚠️ Troubleshooting
 * **Mic Not Responding:** Ensure no other application (like Discord or Zoom) is exclusively using the microphone.
 * **GUI Freeze:** If the window stops responding, ensure pyttsx3 is being initialized inside the jarvis_thread_main function to avoid COM threading issues.
 * **API Timeouts:** Check your internet connection; the Google Speech API requires an active link.
## 📝 License
Distributed under the MIT License. See LICENSE for more information.
## 👤 Author
**Electronics Engineer & Programmer**
 * Project: Voice-Controlled AI Assistant (Jarvis)
 * Goal: Integrating AI with system-level automation.
