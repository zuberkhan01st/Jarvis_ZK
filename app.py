from dotenv import load_dotenv
import os
import pyttsx3
import speech_recognition as sr
import psutil  # For system operations
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure the generative AI model (Gemini API)
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# List all available voices
voices = engine.getProperty('voices')

# Set the voice to the desired one (e.g., female voice)
# Set the voice to the desired one (e.g., Microsoft David, Microsoft Zira, or Microsoft Mark)
for voice in voices:
    if "David" in voice.name:  # Check if the voice contains "Zira"
        engine.setProperty('voice', voice.id)
        break
    elif "Mark" in voice.name:  # Check if the voice contains "Mark"
        engine.setProperty('voice', voice.id)
        break


# Set speech rate (speed) and volume
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 0.9)  # Volume level

# Function to initialize chat
def initialize_chat():
    """Initialize the generative AI model chat."""
    model = genai.GenerativeModel("gemini-pro")
    return model.start_chat(history=[])

# Function to get Gemini's response
def get_gemini_response(question):
    """Fetch response from the Gemini Pro model."""
    model = initialize_chat()  # Initialize the model
    response = model.send_message(question, stream=True)
    response_text = ""
    for chunk in response:
        response_text += chunk.text
    return response_text

# Function to convert text to speech
def text_to_speech(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

# Function to listen to the user's voice input
def listen_to_user():
    """Capture voice input from the user."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5)
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand that."
        except sr.RequestError as e:
            return f"Could not request results; {e}"
        except sr.WaitTimeoutError:
            return "Listening timed out."

# Perform system tasks if necessary
def perform_system_task(command):
    """Execute system-related commands."""
    if "open notepad" in command:
        os.system("notepad.exe")
        return "Opening Notepad."
    elif "open calculator" in command:
        os.system("calc.exe")
        return "Opening Calculator."
    elif "check battery" in command:
        battery = psutil.sensors_battery()
        if battery:
            return f"Your system is at {battery.percent}% battery."
        return "Unable to retrieve battery information."
    elif "check disk space" in command:
        usage = psutil.disk_usage('/')
        return f"Your disk is {usage.percent}% full with {usage.free // (1024 ** 3)} GB free space."
    elif "shutdown" in command:
        os.system("shutdown /s /t 1")
        return "Shutting down the system."
    elif "restart" in command:
        os.system("shutdown /r /t 1")
        return "Restarting the system."
    else:
        return None

# Process the user input and determine appropriate response
def process_and_respond(user_command):
    """Process the user command and determine the appropriate response."""
    # Check for system commands first
    system_response = perform_system_task(user_command)
    if system_response:
        return system_response

    # If it's a query, send it to Gemini for an answer
    return get_gemini_response(user_command)

# Main loop for Jarvis AI
def main():
    """Main loop for Jarvis AI."""
    text_to_speech("Hello! I am Jarvis. How can I assist you today?")
    while True:
        try:
            # Get user input via voice
            user_command = listen_to_user().lower()
            print(f"You said: {user_command}")

            if user_command in ["exit", "quit", "bye"]:
                text_to_speech("Goodbye! Have a great day!")
                break

            # Process and respond (System task or query for Gemini)
            response = process_and_respond(user_command)
            print(f"Jarvis: {response}")
            text_to_speech(response)

        except KeyboardInterrupt:
            text_to_speech("Goodbye! Have a great day!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            text_to_speech("Sorry, something went wrong.")

if __name__ == "__main__":
    main()
