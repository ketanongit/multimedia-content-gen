# functions/videoGeneration.py
from PIL import Image
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip
from pydub import AudioSegment
from utils.query import query_music
from functions.subTitle import create_text_clip, transcribe_audio
import re

# video creation
def create_video_with_animated_subtitles(audio_file_path, image_paths, cleaned_text, num_images, music_prompt):
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', cleaned_text)
    audio_segment = AudioSegment.from_file(audio_file_path)
    image_duration = audio_segment.duration_seconds / num_images

    # Ensure we have exactly the required number of images
    if len(image_paths) > num_images:
        image_paths = image_paths[:num_images]
    
    # Create ImageClips for each image
    clips = []
    for image_path in image_paths:
        try:
            # Open the image file and create an ImageClip
            img = Image.open(image_path)
            img.save("assets/temp_image.png")  # Save it temporarily if needed
            clip = ImageClip("assets/temp_image.png", duration=image_duration)
            clips.append(clip)
        except Exception as e:
            print(f"Failed to load or save image from path '{image_path}': {e}")
    
    # Concatenate image clips
    video = concatenate_videoclips(clips, method="compose")
    
    # Set the audio of the video
    audio = AudioFileClip(audio_file_path)
    video = video.set_audio(audio)

    # Create the subtitle animation
    transcriptions, timestamps = transcribe_audio(audio_file_path)
    word_clips = []
    for i, (start, end) in enumerate(timestamps):
        words = transcriptions[i].split()
        word_start = start
        word_duration = (end - start) / len(words)
        for j, word in enumerate(words):
            word_clip = create_text_clip(word, font_size=70, color='white', stroke_color='black', stroke_width=2, duration=word_duration)
            word_clip = word_clip.set_position(('center', 'center')).set_start(word_start).crossfadein(0.1)
            word_clips.append(word_clip)
            word_start += word_duration
    
    subtitle_video = CompositeVideoClip([video] + word_clips)

    # Generate background music
    music_payload = {"inputs": music_prompt}
    music_content = query_music(music_payload)
    with open("assets/background_music.mp3", "wb") as music_file:
        music_file.write(music_content)

    # Load background music and adjust its volume
    background_music = AudioSegment.from_file("assets/background_music.mp3")
    background_music = background_music - 20  # Reduce volume by 20 dB
    
    # Combine speech and background music
    combined_audio = background_music.overlay(audio_segment)
    combined_audio_path = "assets/combined_audio.mp3"
    combined_audio.export(combined_audio_path, format="mp3")

    # Set the combined audio to the video
    combined_audio_clip = AudioFileClip(combined_audio_path)
    subtitle_video = subtitle_video.set_audio(combined_audio_clip)
    
    video_file_path = "multimedia_video_presentation.mp4"
    subtitle_video.write_videofile(video_file_path, codec="libx264", audio_codec="aac", fps=24)
    
    return video_file_path
