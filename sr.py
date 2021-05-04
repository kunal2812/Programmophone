import pyttsx3
import speech_recognition as sr


engine = pyttsx3.init()
recognizer = sr.Recognizer()

def Speak(text):
    engine.say(something)
    engine.runAndWait()

def Action()
    try:
        with sr.Microphone(device_index = 2) as source:
            print('Speak Now')
            recognizer.adjust_for_ambient_noise(source)
            voice = recognizer.listen(source,timeout=10)
            text = recognizer.recognize_google(voice)
            return text
    except:
        print("Can't hear")


