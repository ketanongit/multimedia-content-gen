#functions/subTitle.py
from PIL import Image, ImageDraw, ImageFont
import whisper
from moviepy.editor import ImageClip
#subtitles placement
def create_text_clip(text, font_size, color, stroke_color, stroke_width, duration):
    font = ImageFont.truetype("arial.ttf", font_size)
    img = Image.new("RGBA", (1280, 720), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    bbox = draw.textbbox((0, 0), text, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((1280 - w) / 2, (720 - h) / 2), text, font=font, fill=color, stroke_width=stroke_width, stroke_fill=stroke_color)
    img.save("assets/temp_text.png")
    return ImageClip("assets/temp_text.png", duration=duration)
#transcribe audio
def transcribe_audio(audio_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    segments = result['segments']
    transcriptions = [seg['text'] for seg in segments]
    timestamps = [(seg['start'], seg['end']) for seg in segments]
    return transcriptions, timestamps