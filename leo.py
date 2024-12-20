import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import subprocess

print("Initializing your AI Assistant...")
MASTER = "Aditya"

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def openCamera():
    try:
        subprocess.run("start microsoft.windows.camera:", shell=True)  # Opens the Camera app on Windows
        speak("Opening the camera.")
    except Exception as e:
        print(e)
        speak("Sorry, I was unable to open the camera.")

def wishMe():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak(f"Good Morning {MASTER}")
    elif 12 <= hour < 18:
        speak(f"Good Afternoon {MASTER}")
    else:
        speak(f"Good Evening {MASTER}")

def search_youtube(query):
    # Format the query for a YouTube search URL
    query = query.replace(' ', '+')  # Replace spaces with '+'
    url = f"https://www.youtube.com/results?search_query={query}"
    
    # Open the URL in the web browser
    webbrowser.open(url)
    speak("Here are the search results on YouTube.")

def search_google(query):
    query = query.replace(' ', '+')  # Replace spaces with '+'
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    speak("Here are the search results on Google.")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 300
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        return query

    except Exception as e:
        print(e)
        speak("Can you please repeat that?")
        return None

def handleQuery(query):
    basic_questions = {
        "who are you": "I am Leo, an AI assistant created to help you.",
        "who created you": "I was created by a developer who loves to build intelligent systems.",
        "what is your purpose": "My purpose is to assist you with tasks and provide information to make your life easier.",
        "thank you": "You're welcome!",
        "thanks": "You're welcome!",
        "thank you very much": "You're welcome!",
        "thanks a lot": "You're welcome!",
        "sorry": "No problem!",
        "i'm sorry": "That's okay!",
        "my apologies": "No worries!",
        "apologies": "No worries!"
    }
    
    query_lower = query.lower()
    if query_lower in basic_questions:
        speak(basic_questions[query_lower])
        return False  # Continue listening for other commands

    if 'wikipedia' in query_lower:
        speak('Searching Wikipedia...')
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        print(results)
        speak(results)

    elif 'video' in query_lower or 'videos' in query_lower:
        speak("What video would you like to watch?")
        video_query = takeCommand()
        if not video_query:
            speak("I didn't catch that. Please try again.")
            return False
        
        speak(f"Searching for {video_query} on YouTube.")
        search_youtube(video_query)


    elif 'google' in query_lower:
        speak("What do you want to search on Google?")
        search_query = takeCommand()
        if not search_query:
            speak("I didn't catch that. Please try again.")
            return False

        speak(f"Searching for {search_query} on Google.")
        search_google(search_query)

    elif 'youtube' in query_lower:
        speak("Opening YouTube...")
        print("Opening YouTube...")
        webbrowser.open("https://www.youtube.com/")

    elif 'chrome' in query_lower:
        speak("Opening Chrome...")
        print("Opening Chrome...")
        webbrowser.open("https://www.google.com/")

    elif 'vtu portal' in query_lower:
        speak("Opening VTU Portal...")
        print("Opening VTU Portal...")
        webbrowser.open("https://vtu.ac.in/en/")

    elif 'portal' in query_lower:
        speak("Opening GNDEC Portal...")
        print("Opening GNDEC Portal...")
        webbrowser.open("https://www.gndecb.ac.in/")

    elif any(word in query_lower for word in ['music', 'song']):
        music_dir = "C:\\Users\\Aditya\\Downloads\\LEO"  # Update with your music directory
        songs = os.listdir(music_dir)
        if songs:
            print("Playing music")
            print(songs)
            os.startfile(os.path.join(music_dir, songs[0]))
        else:
            speak("No music files found in the directory.")

    elif 'time' in query_lower:
        strTime = datetime.datetime.now().strftime("%H:%M")
        print(f"{MASTER} now it's {strTime}")
        speak(f"{MASTER} now it's {strTime}")

    elif 'camera' in query_lower:
        openCamera()
        print("Opening camera")

    elif 'stop' in query_lower or 'exit' in query_lower:
        speak("Exiting the AI Assistant. Thank you!")
        print("Thank You")
        return True  # Return True to indicate that the assistant should stop

    return False

def runAssistant():
    while True:
        query = takeCommand()
        if query:
            should_stop = handleQuery(query)
            if should_stop:
                return  # Exit the loop and return control to listenForWakeWord

def listenForWakeWord():
    wake_word = "leo"  # Define your wake word
    while True:
        print("Listening for wake word...")
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.pause_threshold = 1
            r.energy_threshold = 300
            audio = r.listen(source)

        try:
            print("Recognizing...")
            command = r.recognize_google(audio, language='en-in').lower()
            print(f"Detected: {command}")
            if wake_word in command:
                wishMe()
                speak("How can I assist you?")
                runAssistant()  # Start handling commands
        except Exception as e:
            print(e)

listenForWakeWord()
