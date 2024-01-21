import os
import subprocess
import speech_recognition as sr
from gtts import gTTS
import replicate
from time import sleep
from clarifai.client.model import Model
from clarifai.client.input import Inputs
import os

os.environ["CLARIFAI_PAT"] = "aa7f0f2a2d354b7885870965f59e6961"


def record_audio():
    #for recording audio
    r = sr.Recognizer()
    print("Before Recording")
    with sr.Microphone() as source:
        print("Say something...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, timeout=5)
    print("After Recording")


    try:
        text = r.recognize_google(audio)
        print(text)
        return text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    tts.save("output.mp3")
    sleep(2)
    subprocess.run(["xdg-open","output.mp3"])



def capture_image(file_path='captured_image.png'):
    try:
        subprocess.run(['libcamera-still', '-e', 'png', '-o', file_path], check=True)
        print(f"Image captured and saved to {file_path}")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
def call_api():
    
    IMAGE_FILE_LOCATION = 'captured_image.png'
    with open(IMAGE_FILE_LOCATION, "rb") as f:
        file_bytes = f.read()
    prompt=""
    while (prompt != "stop"):
        prompt = record_audio()
        if (prompt == "stop"):
            break

    inference_params = dict(temperature=0.2, max_tokens=1000)

    model_prediction = Model("https://clarifai.com/openai/chat-completion/models/openai-gpt-4-vision").predict(inputs = [Inputs.get_multimodal_input(input_id="", image_bytes = file_bytes, raw_text=prompt)], inference_params=inference_params)
    text_to_speech(model_prediction.outputs[0].data.text.raw)

if __name__ == "__main__":
    while True:
        command = record_audio()
        if command and ("hey vision" in command.lower() or "hello vision" in command.lower() or "vision" in command.lower()):
            print("Capturing image...")
            subprocess.run(["xdg-open","CapturingImage.mp3"])
            capture_image()
            print("Recording prompt...")
            subprocess.run(["xdg-open","RecordingPrompt.mp3"])
            sleep(1)
            call_api()
            print("Deleting captured image...")
            os.remove('captured_image.png')
            print("Converting API output to speech...")
            sleep(2)  