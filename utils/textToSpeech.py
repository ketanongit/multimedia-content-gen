from pydub import AudioSegment
from gtts import gTTS
import time

def text_to_speech(text, speed=1.0, retries=3, delay=2):
    for attempt in range(retries):
        try:
            tts = gTTS(text, lang='en',tld='co.uk')
            audio_file_path = "assets/speech.mp3"
            tts.save(audio_file_path)
            
            # Load the audio file with pydub and adjust the speed
            audio = AudioSegment.from_file(audio_file_path)
            audio_with_speed = audio.speedup(playback_speed=speed)
            temp_audio_file_path = "assets/temp_speech.mp3"
            audio_with_speed.export(temp_audio_file_path, format="mp3")
            
            with open(temp_audio_file_path, "rb") as audio_file:
                return audio_file.read(), audio_file_path, temp_audio_file_path
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                raise e