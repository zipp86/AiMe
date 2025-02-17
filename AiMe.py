import os
import requests
import speech_recognition as sr
import pyttsx3
import wget
import webbrowser
import shutil
import psutil
import socket
import sqlite3
import re
import time
import subprocess
import ast
import inspect
import codeop
import zipfile
import platform
from llama_index import SimpleDirectoryReader, GPTSimpleVectorIndex

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Set the voice rate
engine.setProperty('rate', 150)

# Load the documents from a directory
documents = SimpleDirectoryReader('path/to/your/documents').load_data()

# Create a LLAMA index
index = GPTSimpleVectorIndex(documents)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
            return query
        except sr.UnknownValueError:
            print("Could not understand the audio.")
        except sr.RequestError:
            print("Speech recognition request failed.")
        return None

def get_weather(location):
    try:
        url = f"https://wttr.in/{location}?format=%t+%C"
        response = requests.get(url)
        if response.status_code == 200:
            weather_info = response.text.strip()
            speak(f"The current weather in {location} is {weather_info}.")
        else:
            speak("Sorry, I couldn't fetch the weather.")
    except requests.RequestException:
        speak("Network error while fetching the weather.")

def get_time():
    from datetime import datetime
    current_time = datetime.now().strftime("%H:%M:%S")
    speak(f"The current time is {current_time}.")

def search_web(query):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)

def download_file(url):
    try:
        filename = url.split("/")[-1]
        wget.download(url, filename)
        speak("Download completed.")
    except Exception as e:
        speak(f"Download failed: {str(e)}")

def open_file(filepath):
    if os.path.exists(filepath):
        os.startfile(filepath)
    else:
        speak("File not found.")

def system_update():
    os.system("sudo apt-get update && sudo apt-get upgrade -y")

def system_shutdown():
    os.system('shutdown /s /t 1')

def network_scan():
    ip = "192.168.1."
    for n in range(1, 255):
        addr = ip + str(n)
        try:
            socket.gethostbyname(addr)
            print(f"Host {addr} is up")
        except socket.gaierror:
            pass

def execute_command(command):
    os.system(command)

def self_upgrade():
    try:
        url = "https://github.com/your_username/AiMe/releases/latest"
        response = requests.get(url)
        latest_version = re.search(r"v(\d+\.\d+\.\d+)", response.text)
        if latest_version:
            latest_version = latest_version.group(1)
            current_version = subprocess.check_output(["git", "describe", "--tags"]).decode().strip()
            if latest_version > current_version:
                url = f"https://github.com/your_username/AiMe/releases/download/v{latest_version}/AiMe.zip"
                filename = "AiMe.zip"
                wget.download(url, filename)
                with zipfile.ZipFile(filename, "r") as zip_ref:
                    zip_ref.extractall()
                os.remove(filename)
                speak("Your AiMe system has been upgraded.")
            else:
                speak("Your AiMe system is up to date.")
        else:
            speak("Could not fetch the latest version.")
    except Exception as e:
        speak(f"Upgrade failed: {str(e)}")

def launch_application(application):
    try:
        os.startfile(application)
    except FileNotFoundError:
        speak("Application not found.")

def get_system_info():
    system = platform.system()
    machine = platform.machine()
    speak(f"You are using a {system} operating system on a {machine} machine.")

def get_disk_info():
    disk_info = psutil.disk_usage('/')
    speak(f"Disk usage is {disk_info.percent}% with {disk_info.free // (1024**3)} GB free.")

def search_documents(query):
    results = index.query(query)
    if results:
        for result in results:
            print(result)
    else:
        speak("No matching documents found.")

def process_query(query):
    if not query:
        return
    query = query.lower()
    words = query.split(" ")

    if query.startswith("weather"):
        if len(words) > 1:
            get_weather(words[1])
        else:
            speak("Please specify a location.")

    elif query.startswith("time"):
        get_time()

    elif query.startswith("search web"):
        if len(words) > 2:
            search_web(" ".join(words[2:]))
        else:
            speak("Please specify a search query.")

    elif query.startswith("download file"):
        if len(words) > 2:
            download_file(words[2])
        else:
            speak("Please provide a URL.")

    elif query.startswith("open file"):
        if len(words) > 2:
            open_file(" ".join(words[2:]))
        else:
            speak("Please provide a file path.")

    elif query.startswith("system update"):
        system_update()

    elif query.startswith("system shutdown"):
        system_shutdown()

    elif query.startswith("network scan"):
        network_scan()

    elif query.startswith("execute command"):
        if len(words) > 2:
            execute_command(" ".join(words[2:]))
        else:
            speak("Please specify a command.")

    elif query.startswith("self upgrade"):
        self_upgrade()

    elif query.startswith("launch application"):
        if len(words) > 2:
            launch_application(" ".join(words[2:]))
        else:
            speak("Please specify an application.")

    elif query.startswith("system info"):
        get_system_info()

    elif query.startswith("disk info"):
        get_disk_info()

    else:
        speak("Sorry, I didn't understand that command.")

if __name__ == "__main__":
    print("Welcome to AiMe. Type 'exit system' to quit.")
    while True:
        try:
            query = input("What can I help you with? ")
            if query.lower() == "exit system":
                break
            process_query(query)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print("An error occurred:", str(e))
            break

    speak("Goodbye!")
    system_shutdown()
