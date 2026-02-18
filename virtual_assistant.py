import speech_recognition as sr
import pyttsx3
import wikipedia
import datetime
import json
import os

# -------------------------------
# Text-to-Speech Engine
# -------------------------------
engine = pyttsx3.init()
engine.setProperty('rate', 170)

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

# -------------------------------
# Speech Recognition
# -------------------------------
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print("You:", command)
        return command.lower()
    except:
        speak("Sorry, I did not understand.")
        return ""

# -------------------------------
# Memory (Continuous Learning)
# -------------------------------
MEMORY_FILE = "assistant_memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as file:
            return json.load(file)
    return {}

def save_memory(memory):
    with open(MEMORY_FILE, "w") as file:
        json.dump(memory, file, indent=4)

memory = load_memory()

# -------------------------------
# Core Functions
# -------------------------------

def tell_time():
    now = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The time is {now}")

def set_reminder(command):
    reminder = command.replace("set reminder", "").strip()
    if "reminders" not in memory:
        memory["reminders"] = []
    memory["reminders"].append(reminder)
    save_memory(memory)
    speak(f"Reminder saved: {reminder}")

def show_reminders():
    reminders = memory.get("reminders", [])
    if reminders:
        speak("Here are your reminders:")
        for r in reminders:
            speak(r)
    else:
        speak("You have no reminders.")

def search_wikipedia(query):
    try:
        result = wikipedia.summary(query, sentences=2)
        speak(result)
    except:
        speak("I couldn't find information on that.")

def save_name(command):
    name = command.replace("my name is", "").strip()
    memory["username"] = name
    save_memory(memory)
    speak(f"Nice to meet you {name}")

def greet_user():
    name = memory.get("username", "")
    if name:
        speak(f"Welcome back {name}")
    else:
        speak("Hello! What is your name?")

# -------------------------------
# Main Assistant Loop
# -------------------------------

def run_assistant():
    greet_user()

    while True:
        command = listen()

        if "exit" in command or "stop" in command:
            speak("Goodbye!")
            break

        elif "time" in command:
            tell_time()

        elif "set reminder" in command:
            set_reminder(command)

        elif "show reminders" in command:
            show_reminders()

        elif "my name is" in command:
            save_name(command)

        elif "who is" in command or "what is" in command:
            query = command.replace("who is", "").replace("what is", "")
            search_wikipedia(query)

        else:
            speak("I am still learning. Please try another command.")

# -------------------------------
# Run
# -------------------------------
if __name__ == "__main__":
    run_assistant()
