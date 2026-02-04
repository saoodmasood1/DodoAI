import pyttsx3

def speak(text):
    engine = pyttsx3.init('sapi5')
    engine.say(text)
    engine.runAndWait()
    engine.stop()

speak("First")
speak("Second")
speak("Third")
speak("Fourth")
speak("Fifth")
speak("Sixth")