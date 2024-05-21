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
        except Exception as e:
            print("Say that again please...")
            return "None"
        return query

def get_weather(location):
    url = f"https://www.google.com/search?q=weather+{location}"
    response = requests.get(url)
    data = response.text
    weather_pattern = re.compile(r"Weather: (.*?)\s+-\s+(\d+)\s+(\w+)")
    match = weather_pattern.search(data)
    if match:
        temperature = match.group(2)
        description = match.group(1)
        speak(f"The current weather in {location} is {temperature} degrees Celsius with {description}.")
    else:
        speak("Sorry, I couldn't find the weather for that location.")

def get_time():
    import datetime
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    speak(f"The current time is {current_time}.")

def search_web(query):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)

def download_file(url):
    filename = url.split("/")[-1]
    wget.download(url, filename)

def open_file(filepath):
    os.startfile(filepath)

def system_update():
    os.system("sudo apt-get update")
    os.system("sudo apt-get upgrade")

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
            print(f"Host {addr} is down")

def execute_command(command):
    os.system(command)

def self_upgrade():
    # Check for updates
    url = "https://github.com/your_username/AiMe/releases/latest"
    response = requests.get(url)
    latest_version = re.search(r"v(\d+\.\d+\.\d+)", response.text).group(1)
    current_version = subprocess.check_output(["git", "describe", "--tags"]).decode().strip()
    if latest_version > current_version:
        # Download the latest version
        url = f"https://github.com/your_username/AiMe/releases/download/v{latest_version}/AiMe.zip"
        filename = "AiMe.zip"
        wget.download(url, filename)
        # Unzip the downloaded file
        with zipfile.ZipFile(filename, "r") as zip_ref:
            zip_ref.extractall()
        # Install the new version
subprocess.call(["sudo", "python3", "setup.py", "install"])
        # Remove the downloaded file
        os.remove(filename)
        os.remove("AiMe.zip")
        speak("AiMe has been upgraded to the latest version.")
    else:
        speak("AiMe is already up-to-date.")

def get_information(topic):
    # Here you would add the code to access the information and skill storage system using LLAMA
    try:
    response = index.query(f"Tell me about {topic}")
    if response:
        speak(response)
    else:
        speak("Sorry, I don't have any information about that topic.")
except Exception as e:
    speak("Sorry, I encountered an error while processing your request.")
    print(e)
       
def examine_code(code):
    try:
        ast.parse(code)
        speak("The code is syntactically correct.")
    except Exception as e:
        speak("The code is syntactically incorrect.")

def generate_code(language, query):
    if language == "python":
        try:
            result = eval(query)
            code = inspect.getsource(result)
            speak("Here is the generated code:")
            speak(code)
        except Exception as e:
            speak("Sorry, I couldn't generate the code for that query.")
    else:
        speak("Sorry, I can only generate Python code at the moment.")

def AiMe():
    # Check for updates
    self_upgrade()
    # Start the AiMe AI assistant
    speak("Hello, I'm AiMe, a world-class AI Assistant. How can I assist you today?")
    query = listen().lower()

    if 'weather' in query:
        location = query.replace("what's the weather in", "").strip()
        get_weather(location)

    elif 'time' in query:
        get_time()

    elif 'search' in query:
        query = query.replace("search for", "").strip()
        search_web(query)

    elif 'download' in query:
        query = query.replace("download", "").strip()
        url = query
        download_file(url)

    elif 'file' in query and 'open' in query:
        query = query.replace("open", "").strip()
        filepath = query
        open_file(filepath)

    elif 'system update' in query:
        system_update()

    elif 'shutdown' in query:
        system_shutdown()

    elif 'scan network' in query:
        network_scan()

    elif 'run' in query:
        query = query.replace("run", "").strip()
        command = query
        execute_command(command)

    elif 'upgrade' in query:
        self_upgrade()

    elif 'information' in query:
        topic = query.replace("get information about", "").strip()
        get_information(topic)

    elif 'examine' in query and 'code' in query:
        query = query.replace("examine", "").strip()
        code = query
        examine_code(code)

    elif 'generate' in query and 'code' in query:
        query = query.replace("generate", "").strip()
        language, query = query.split("for")
        language = language.strip()
        query = query.strip()
        generate_code(language, query)

    else:
        speak("Sorry, I couldn't understand that command. Can you please repeat?")
        AiMe()

AiMe()
