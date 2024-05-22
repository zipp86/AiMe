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
        with zipfile.ZipFile(filename, "r") aszip_ref:
            zip_ref.extractall()
        # Delete the downloaded zip file
        os.remove(filename)
        # Upgrade completed
        speak("Your AiMe system has been upgraded to the latest version.")
    else:
        speak("Your AiMe system is already up to date.")

def launch_application(application):
    try:
        os.startfile(application)
    except:
        speak("Sorry, I couldn't find that application.")

def exit_system():
    os.system('shutdown /s /t 1')

def help_commands():
    commands = [
        "Download file",
        "Open file",
        "System update",
        "System shutdown",
        "Network scan",
        "Execute command",
        "Self upgrade",
        "Launch application",
        "Help commands",
        "Exit system"
    ]
    for command in commands:
        print(command)

def get_system_info():
    system_info = psutil.get_system_info()
    speak(f"You are using a {system_info.system} operating system on a {system_info.machine} machine.")

def get_disk_info():
    disk_info = psutil.disk_usage('/')
    speak(f"You have {disk_info.percent} percent disk usage. {disk_info.free} bytes of disk space is free out of {disk_info.total} bytes total.")

def search_documents(query):
    results = index.search(query)
    for result in results:
        print(result.id)
        print(result.vector)
        print(result.data)

def find_word_synonyms(word):
    try:
        synonyms = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}").json()
        print(synonyms[0]['meanings'][0]['synonyms'])
    except:
        speak("Sorry, I couldn't find any synonyms for that word.")

def search_documents_synonyms(word):
    results = []
    for document in documents:
        if word in document.split():
            results.append(document)
    if results:
        speak("I found the following documents containing synonyms for that word:")
        for result in results:
            print(result)
    else:
        speak("I couldn't find any documents containing synonyms for that word.")

def process_query(query):
    # Lowercase the query for case insensitivity
    query = query.lower()
    # Search the LLAMA index for documents containing the query
    search_results = search_documents(query)
    # Search the LLAMA index for documents containing synonyms for the query
    search_synonyms_results = search_documents_synonyms(query)
    # Search for the weather in a given location
    if re.match(r"weather", query):
        get_weather(query.split(" ")[1])
    # Search for the current time
    elif re.match(r"time", query):
        get_time()
    # Search the web for the query
    elif re.match(r"search web", query):
        search_web(query.split(" ")[2])
    # Download a file from a given URL
    elif re.match(r"download file", query):
        download_file(query.split(" ")[2])
    # Open a file at a given filepath
    elif re.match(r"open file", query):
        open_file(query.split(" ")[2])
    # Update the system software
    elif re.match(r"system update", query):
        system_update()
    # Shutdown the system
    elif re.match(r"system shutdown", query):
        system_shutdown()
    # Scan the network for active devices
    elif re.match(r"network scan", query):
        network_scan()
    # Execute a command in the system terminal
    elif re.match(r"execute command", query):
        execute_command(query.split(" ")[2])
    # Upgrade AiMe to the latest version
    elif re.match(r"self upgrade", query):
        self_upgrade()
    # Launch an application from the system
    elif re.match(r"launch application", query):
        launch_application(query.split(" ")[2])
    # Print a list of all commands
    elif re.match(r"help commands", query):
        help_commands()
    # Exit the AiMe system
    elif re.match(r"exit system", query):
        exit_system()
    # Get system information
    elif re.match(r"system info", query):
        get_system_info()
    # Get disk information
    elif re.match(r"disk info", query):
        get_disk_info()
    # Search for synonyms for a given word
    elif re.match(r"find word synonyms", query):
        find_word_synonyms(query.split(" ")[2])

# Start the AiMe system
if __name__ == "__main__":
    print("Welcome to AiMe. Type 'exit system' to quit.")
    while True:
        try:
            query = input("What can I help you with? ")
            if query == "exit system":
                break
            process_query(query)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print("An error occurred:", str(e))
            break
    speak("Goodbye!")
    exit_system()
