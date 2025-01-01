import speech_recognition as sr
import webbrowser
import pyttsx3
import sys
from youtubesearchpython import VideosSearch

recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Function for text-to-speech using pyttsx3
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to search YouTube for a song
def search_youtube_song(song_name):
    search = VideosSearch(song_name, limit=1)  # Limit to 1 result
    results = search.result()['result']
    if results:
        video_url = results[0]['link']  # Get the first video link
        return video_url
    else:
        speak("Sorry, I couldn't find the song.")
        return None

# Function to process voice commands
def process_command(c):
    if "open google" in c:
        speak("Opening Google")
        webbrowser.open("https://google.com")
    elif "open youtube" in c:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")
    elif "open instagram" in c:
        speak("Opening Instagram")
        webbrowser.open("https://instagram.com")
    elif "play" in c:
        song_name = c.replace("play", "").strip()
        speak(f"Searching for {song_name} on YouTube")
        video_url = search_youtube_song(song_name)
        if video_url:
            webbrowser.open(video_url)
            speak(f"Playing {song_name} on YouTube.")
    elif "exit" in c:
        speak("Exiting...")
        sys.exit()  # Stop the program
    else:
        speak("Sorry, I don't understand that command.")

# Function to listen for a single command
def listen_for_command():
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)  # Adjust to background noise
            print("Listening for command...")
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio)  # Convert audio to text
            print(f"Recognized command: {command}")
            return command.lower()
   
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""

if __name__ == "__main__":
    speak("Jarvis initialized. Say 'Jarvis' to activate.")

    while True:
        # Step 1: Wait for the wake word "Jarvis"
        print("Waiting for wake word...")
        wake_word = listen_for_command()
        
        if "jarvis" in wake_word:
            speak("Yes, I'm listening.")
            
            # Step 2: After wake word, continuously listen for commands until "exit"
            while True:
                command = listen_for_command()

                if command == "exit":
                    process_command(command)  # Exit if "exit" is spoken
                    break
                elif command:
                    process_command(command)
