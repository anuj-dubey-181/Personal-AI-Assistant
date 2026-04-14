import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import google.generativeai as genai
import tkinter as tk
from tkinter import scrolledtext
import threading
import queue
import time
from config import GEMINI_API_KEY

# --- Jarvis Core Logic ---

def processCommand(c, chat_session, speak_func):
    """Processes commands. Returns True to continue conversation, False to end it."""
    log_queue.put(f"User: {c}")
    cmd = c.lower()
    
    # 1. Check for Exit Phrase
    if "bye bye jarvis" in cmd or "stop conversation" in cmd:
        speak_func("Goodbye! Let me know if you need anything else.")
        return False # This will break the session loop

    # 2. Handle System Tasks
    if "open google" in cmd:
        webbrowser.open("https://google.com")
        speak_func("Opening Google.")
    elif "open youtube" in cmd:
        webbrowser.open("https://youtube.com")
        speak_func("Opening YouTube.")
    elif "open linkedin" in cmd:
        webbrowser.open("https://linkedin.com")
        speak_func("Opening LinkedIn.")
    elif cmd.startswith("play"):
        song = cmd.split(" ", 1)[1].strip()
        if hasattr(musicLibrary, 'music') and song in musicLibrary.music:
            link = musicLibrary.music[song]
            webbrowser.open(link)
            speak_func(f"Playing {song}.")
        else:
            speak_func(f"Sorry, I couldn't find {song} in your library.")
    
    # 3. Default to AI Chat
    else:
        try:
            response = chat_session.send_message(c)
            cleaned_response = response.text.replace('*', '').strip()
            speak_func(cleaned_response)
        except Exception as e:
            speak_func(f"I ran into an AI error: {e}")
            
    return True # Continue the conversation

# --- Threaded Assistant Loop ---

def jarvis_thread_main():
    engine = pyttsx3.init()
    
    def speak(text):
        log_queue.put(f"Jarvis: {text}")
        engine.say(text)
        engine.runAndWait()

    # Configure Gemini once
    genai.configure(api_key=GEMINI_API_KEY) 
    model = genai.GenerativeModel("gemini-2.5-flash-lite")
    
    speak("Jarvis systems online.")
    r = sr.Recognizer()
    
    while not stop_jarvis_thread.is_set():
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.5)
                log_queue.put("Status: Waiting for wake word 'Jarvis'...")
                audio = r.listen(source, timeout=2, phrase_time_limit=3)
            
            word = r.recognize_google(audio)

            if word.lower() == "jarvis":
                speak("I'm listening. What's on your mind?")
                
                # --- START CONVERSATION SESSION ---
                # Create a new chat session history for this specific conversation
                chat_session = model.start_chat(history=[])
                in_conversation = True
                
                while in_conversation and not stop_jarvis_thread.is_set():
                    try:
                        with sr.Microphone() as session_source:
                            r.adjust_for_ambient_noise(session_source, duration=0.5)
                            log_queue.put("Status: [Session Active] Listening...")
                            session_audio = r.listen(session_source, timeout=5, phrase_time_limit=6)
                            
                        user_input = r.recognize_google(session_audio)
                        # Process command and check if we should keep going
                        in_conversation = processCommand(user_input, chat_session, speak)
                        
                    except sr.WaitTimeoutError:
                        # If you don't speak for 5 seconds, Jarvis asks if you're still there
                        log_queue.put("System: Silence detected...")
                        continue 
                    except sr.UnknownValueError:
                        speak("I didn't quite catch that. Could you repeat?")
                    except Exception as e:
                        log_queue.put(f"Session Error: {e}")
                        in_conversation = False
                # --- END CONVERSATION SESSION ---

        except (sr.WaitTimeoutError, sr.UnknownValueError):
            continue 
        except Exception as e:
            log_queue.put(f"Main Loop Error: {e}")
            time.sleep(1)

# --- GUI Controls (Same as before) ---

def update_log_display():
    while not log_queue.empty():
        message = log_queue.get()
        log_display.config(state=tk.NORMAL)
        log_display.insert(tk.END, message + "\n")
        log_display.see(tk.END)
        log_display.config(state=tk.DISABLED)
    root.after(100, update_log_display)

def start_jarvis():
    global jarvis_thread
    if jarvis_thread is None or not jarvis_thread.is_alive():
        stop_jarvis_thread.clear()
        jarvis_thread = threading.Thread(target=jarvis_thread_main, daemon=True)
        jarvis_thread.start()
        start_button.config(text="Jarvis Running", state=tk.DISABLED)
        stop_button.config(state=tk.NORMAL)

def stop_jarvis():
    stop_jarvis_thread.set()
    start_button.config(text="Start Jarvis", state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)

# --- Main App ---
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Jarvis AI Assistant")
    root.geometry("600x500")

    log_queue = queue.Queue()
    stop_jarvis_thread = threading.Event()
    jarvis_thread = None

    btn_frame = tk.Frame(root, pady=10)
    btn_frame.pack()

    start_button = tk.Button(btn_frame, text="Start Jarvis", command=start_jarvis, width=15)
    start_button.pack(side=tk.LEFT, padx=5)

    stop_button = tk.Button(btn_frame, text="Stop Jarvis", command=stop_jarvis, state=tk.DISABLED, width=15)
    stop_button.pack(side=tk.LEFT, padx=5)

    log_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED, bg="#1e1e1e", fg="#00ff00")
    log_display.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

    root.after(100, update_log_display)
    root.mainloop()