import pyttsx3
import speech_recognition as sr
import webbrowser
import os
import subprocess
import pywhatkit
import psutil

# Initialize the speech synthesis engine
engine = pyttsx3.init()

# Set the voice to a female voice
desired_voice = "Microsoft Zira Desktop - English (United States)"
voices = engine.getProperty('voices')
for voice in voices:
    if voice.name == desired_voice:
        engine.setProperty('voice', voice.id)
        break

# Initialize the speech recognition recognizer
recognizer = sr.Recognizer()

def exit_application():
    # Get the current process ID
    current_process = psutil.Process(os.getpid())
    # Terminate the current process and all its child processes
    current_process.terminate()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen_for_wake_word():
    while True:
        print("Listening for the wake word...")
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio)
            print(f"You: {text}")
            if "shravi" in text.lower():
                speak("Yes, I'm listening. How can I assist you?")
                process_command()
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that. Could you please say 'Shravi'?")
        except sr.RequestError as e:
            print(f"An error occurred: {str(e)}")

def listen():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print(f"You: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I didn't understand that.")
    except sr.RequestError as e:
        print(f"An error occurred: {str(e)}")

def process_command():
    command = listen()
    if command is not None:
        if "hello" in command.lower():
            speak("Hello! How can I assist you today?")
        elif "time" in command.lower():
            # Replace with your own logic to fetch the current time
            speak("The current time is 12:00 PM.")
        elif "date" in command.lower():
            # Replace with your own logic to fetch the current date
            speak("Today is May 17, 2023.")
        elif "search" in command.lower():
            query = command.split("search", 1)[1].strip()
            search(query)
        elif "open" in command.lower():
            app = command.split("open", 1)[1].strip()
            if app.lower() == "google keep":
                open_google_keep()
            else:
                open_application(app)
        elif "volume up" in command.lower():
            change_volume("up")
        elif "volume down" in command.lower():
            change_volume("down")
        elif "brightness up" in command.lower():
            change_brightness("up")
        elif "brightness down" in command.lower():
            change_brightness("down")
        elif "play" in command.lower():
            video = command.split("play", 1)[1].strip()
            play_video(video)
        elif "turn off" in command.lower():
            speak("okay")
            exit_application()
        else:
            speak("I'm sorry, I cannot perform that command.")

def search(query):
    if "search a song on video on youtube" in query.lower():
        song_name = query.split("search a song on video on YouTube", 1)[1].strip()
        play_song_on_youtube(song_name)
    else:
        url = "https://www.google.com/search?q=" + query.replace(" ", "+")
        webbrowser.open(url)
        speak(f"Here are the search results for {query}")

def play_song_on_youtube(song_name):
    pywhatkit.playonyt(song_name)    

def open_application(app):
    app_paths = {
        "notepad": "C:\\Windows\\System32\\notepad.exe",
        "calculator": "C:\\Windows\\System32\\calc.exe",
        "paint": "C:\\Windows\\System32\\mspaint.exe",
        "vs code": "C:\\Users\\Bhagwant Singh\\AppData\\Local\\Programs\\Visual Studio Code\\Code.exe"
    }
    try:
        os.startfile(app_paths.get(app, app))
        speak(f"Opening {app}")
    except OSError:
        speak(f"Sorry, I couldn't find {app}. Make sure it's installed or provide the full path.")

def open_google_keep():
    url = "https://keep.google.com/"
    webbrowser.open(url)
    speak("Opening Google Keep in your browser")

def change_volume(direction):
    if direction == "up":
        subprocess.call(["amixer", "-D", "pulse", "sset", "Master", "5%+"])
        speak("Volume increased")
    elif direction == "down":
        subprocess.call(["amixer", "-D", "pulse", "sset", "Master", "5%-"])
        speak("Volume decreased")

def change_brightness(direction):
    if direction == "up":
        subprocess.call("xbacklight -inc 10", shell=True)
        speak("Brightness increased")
    elif direction == "down":
        subprocess.call("xbacklight -dec 10", shell=True)
        speak("Brightness decreased")

def play_video(video):
    speak("Searching for videos...")
    pywhatkit.playonyt(video)

if __name__ == "__main__":
    speak("yess")
    
    while True:
        try:
            process_command()
        except KeyboardInterrupt:
            print("Program terminated by user.")
            break

        written_command = input("Enter a written command: ")
        if written_command.lower() == "exit":
            speak("Exiting the program. Goodbye!")
            break
        else:
            process_command(written_command)
