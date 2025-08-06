import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import requests
import json
import pyjokes

# Initialize the speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wish_me():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am your voice assistant. How can I help you today?")

def take_command():
    # It takes microphone input from the user and returns string output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Say that again please...")
        return "None"
    return query.lower()

def send_email(to, content):
    # You can configure your email and password here
    # This is a placeholder function and requires proper email setup
    pass

def get_weather(city):
    api_key = "your_openweathermap_api_key"  # You need to get your own API key from openweathermap.org
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + city + "&units=metric"
    response = requests.get(complete_url)
    x = response.json()
    if x["cod"] != "404":
        y = x["main"]
        current_temperature = y["temp"]
        current_humidity = y["humidity"]
        z = x["weather"]
        weather_description = z[0]["description"]
        weather_report = f"Temperature is {current_temperature} degree Celsius with {weather_description} and humidity of {current_humidity} percent."
        return weather_report
    else:
        return "City not found."

def main():
    wish_me()
    while True:
        query = take_command()

        if query == "none":
            continue

        # Logic for executing tasks based on query
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            try:
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                speak(results)
            except Exception as e:
                speak("Sorry, I could not find any results.")
        elif 'open youtube' in query:
            webbrowser.open("youtube.com")
        elif 'open google' in query:
            webbrowser.open("google.com")
        elif 'open stackoverflow' in query:
            webbrowser.open("stackoverflow.com")
        elif 'play music' in query:
            music_dir = "C:\\Users\\dani\\Music"  # Change this path to your music directory
            songs = os.listdir(music_dir)
            if songs:
                os.startfile(os.path.join(music_dir, songs[0]))
            else:
                speak("No music files found in the directory.")
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")
        elif 'open code' in query:
            code_path = "C:\\Users\\dani\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"  # Change this path if needed
            os.startfile(code_path)
        elif 'send email' in query:
            speak("Sorry, email functionality is not configured yet.")
        elif 'joke' in query:
            joke = pyjokes.get_joke()
            speak(joke)
        elif 'weather' in query:
            speak("Please tell me the city name.")
            city = take_command()
            if city != "none":
                weather_report = get_weather(city)
                speak(weather_report)
            else:
                speak("City name not recognized.")
        elif 'exit' in query or 'quit' in query or 'stop' in query:
            speak("Goodbye!")
            break
        else:
            speak("I am sorry, I don't understand that command.")

if __name__ == "__main__":
    main()
