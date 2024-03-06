import openai
import pyttsx3
import speech_recognition as sr
import time

# Set your OpenAI API key
openai.api_key = "api key"

#initialize the text to speech engine
engine = pyttsx3.init()

def transcribe_audio_to_text(filename):
    r = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = r.record(source)
    try:
        text = r.recognize_google(audio)
        return text
    except:
        print("skipping unknown error")

def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.5,
        max_tokens=4000,
        n=1,
        stop=4,
    )
    return response['choices'][0]['text']

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def main():
    #wait for the user to say Genius
    print("say genius  to start recording your question")
    with sr.Microphone(device_index=1) as source:
        recognizer = sr.Recognizer()
        # wait for a second to let the recognizer adjust the
        audio = recognizer.listen(source) 
        try:
            transcription = recognizer.recognize_google(audio)
            if transcription.lower == "genius":
                #record audio
                filename = "audio.wav"
                print("how can i help you")
                with sr.Microphone() as source:
                    recognizer = sr.recognizer()
                    source.pause_threshold = 1
                    audio = recognizer. Listen (source, phrase_time_limit=None, timeout=None)
                    with open(filename, "wb") as f:
                        f.write(audio.get_wav_data())

                #transcribe audio to text
                text = transcribe_audio_to_text(filename)
                if text:
                    print(f'you said: {text}')    

                    #generate response
                    response = generate_response(text)
                    print(f'your response: {response}')

                    #speak response
                    speak_text(response)
        except Exception as e:
            print("An error occurred: ()".format(e))            

if __name__ == "__main__":
    main()
