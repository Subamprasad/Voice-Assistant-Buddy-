import speech_recognition as sr
import webbrowser
import pyttsx3
import time
import wikipedia
import pywhatkit
import random
from datetime import datetime
import pytz
import sys
import pyautogui

recognizer = sr.Recognizer()
engine = pyttsx3.init()

# === Speak ===
def speak(text):
    print("Buddy:", text)
    engine.say(text)
    engine.runAndWait()

# === Listen for voice ===
def listen_command():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio)
            print("You said:", command)
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
        except sr.RequestError:
            speak("Sorry, I'm having trouble connecting to the service.")
        return ""

# === Get time ===
def get_current_time():
    tz = pytz.timezone("Asia/Kolkata")
    now = datetime.now(tz)
    time_str = now.strftime("%I:%M %p")
    date_str = now.strftime("%A, %d %B %Y")
    return f"It's {time_str}, {date_str}, IST."

# === Open known websites ===
def open_website_from_command(command):
    sites = {
        "youtube": "https://youtube.com",
        "amazon": "https://amazon.in",
        "gmail": "https://mail.google.com",
        "google": "https://google.com",
        "facebook": "https://facebook.com",
        "instagram": "https://instagram.com",
    }

    for name in sites:
        if name in command:
            speak(f"Opening {name.capitalize()}, boss!")
            webbrowser.open(sites[name])
            return True
    return False

# === Wikipedia-style AI answer ===
def answer_like_ai_overview(query):
    try:
        summary = wikipedia.summary(query, sentences=2)
        print("Search Result:", summary)
        speak(summary)
    except wikipedia.DisambiguationError as e:
        speak(f"That could mean multiple things, like {e.options[0]} or {e.options[1]}.")
    except:
        pywhatkit.search(query)
        speak("I found something on Google.")

# === Joke generator ===
def tell_a_joke():
    jokes = [
        "Why don't programmers like nature? Too many bugs!",
        "I told my computer I needed a break, and now it won’t stop sending me KitKat ads.",
        "Why did the developer go broke? Because he used up all his cache.",
        "Why do Java developers wear glasses? Because they can't C#.",
        "Debugging: Being the detective in a crime movie where you are also the murderer."
    ]
    speak(random.choice(jokes))

# === Play YouTube song ===
def play_music(command):
    speak("Playing it on YouTube!")
    pywhatkit.playonyt(command)

# === Close current YouTube tab ===
def close_current_tab():
    speak("Stopping the song, boss!")
    pyautogui.hotkey('ctrl', 'w')  # Close active tab

# === Change song ===
def change_song():
    close_current_tab()
    suggestions = ["lofi beats", "motivational songs", "latest Bollywood", "romantic songs", "hip hop India"]
    next_song = random.choice(suggestions)
    speak(f"Changing to {next_song}")
    pywhatkit.playonyt(next_song)

# === Command handling ===
def process_command(command):
    if "ok done" in command or "exit" in command or "bye" in command:
        speak("Goodbye boss!")
        sys.exit()

    elif "stop the song" in command or "stop music" in command or "stop song" in command or "stop" in command:
        close_current_tab()

    elif "change" in command:
        change_song()

    elif "time" in command or "date" in command:
        speak(get_current_time())

    elif "music" in command or "play" in command:
        play_music(command)

    elif "google it and tell me a joke" in command:
        speak("Searching Google for a joke, boss!")
        pywhatkit.search("tell me a joke")
        tell_a_joke()

    elif "joke" in command:
        tell_a_joke()

    elif open_website_from_command(command):
        return

    else:
        speak(f"Searching Google for: {command}")
        pywhatkit.search(command)
        answer_like_ai_overview(command)

# === Main loop ===
if __name__ == "__main__":
    speak("Initializing Buddy...")
    time.sleep(1)
    speak("Say 'Hey Buddy' to wake me up or 'OK done' to shut me down.")

    while True:
        command = listen_command()

        if "ok done" in command:
            speak("Okay boss, shutting down now.")
            break

        elif "hey buddy" in command:
            speak("Hello, I am Buddy. How can I assist you?")
            while True:
                command = listen_command()
                if "ok done" in command:
                    speak("Goodbye boss!")
                    sys.exit()
                elif command:
                    process_command(command)

