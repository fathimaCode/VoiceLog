import speech_recognition as sr

# Initialize the recognizer
recognizer = sr.Recognizer()

# Use the default microphone as the audio source
microphone = sr.Microphone()

# Function to convert speech to text
def speech_to_text():
    with microphone as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio)  # Recognize speech using Google Speech Recognition
        return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand what you said.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

# Continuously listen for speech and convert it to text
while True:
    text = speech_to_text()
    if text:
        print("You said:", text)
