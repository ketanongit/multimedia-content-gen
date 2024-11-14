#app.py
from flask import Flask, request, jsonify, render_template, send_from_directory
from functions.funFact import generate_fun_fact
from functions.story import generate_story
from functions.videoGeneration import create_video_with_animated_subtitles
import os

app = Flask(__name__)

# Serve the index page
@app.route('/')
def index():
    return render_template('fact.html')

@app.route('/story')
def story():
    return render_template('story.html')    

@app.route('/ad')
def add():
    return render_template('ad.html')    

# Serve the about page
@app.route('/ppt')
def ppt():
    return render_template('ppt.html')

# Video generation route for fun facts
@app.route('/generate_video', methods=['POST'])
def generate_video():
    base_prompt = request.json.get('keyword')
    num_images = int(request.json.get('num_images'))
    speed = float(request.json.get('speed'))
    music_prompt = request.json.get('music_prompt')

    # Generate fun fact, images, and audio
    audio_file_path, temp_audio_file_path, fun_fact_images, cleaned_text = generate_fun_fact(base_prompt, num_images, speed)

    # Create the video with animated subtitles
    video_file_path = create_video_with_animated_subtitles(temp_audio_file_path, fun_fact_images, cleaned_text, num_images, music_prompt)

    # Cleanup temporary files
    os.remove("assets/background_music.mp3")
    os.remove("assets/combined_audio.mp3")
    os.remove("assets/temp_image.png")
    os.remove("assets/temp_text.png")
    os.remove("assets/speech.mp3")

    return jsonify({"video_url": f"/videos/{os.path.basename(video_file_path)}"})

# Video generation route for stories
@app.route('/generate_story_video', methods=['POST'])
def generate_story_video():
    base_prompt = request.json.get('keyword')
    speed = float(request.json.get('speed'))
    music_prompt = request.json.get('music_prompt')
    story_script = request.json.get('story_script')

    # Generate story video with the provided script
    audio_file_path, temp_audio_file_path, story_images, cleaned_story_text = generate_story(base_prompt, story_script, speed)

    # Create the video with animated subtitles
    video_file_path = create_video_with_animated_subtitles(temp_audio_file_path, story_images, cleaned_story_text, len(story_images), music_prompt)

    # Cleanup temporary files
    os.remove("assets/background_music.mp3")
    os.remove("assets/combined_audio.mp3")
    os.remove("assets/temp_image.png")
    os.remove("assets/temp_text.png")
    os.remove("assets/speech.mp3")

    return jsonify({"video_url": f"/videos/{os.path.basename(video_file_path)}"})

# Serve generated videos
@app.route('/videos/<filename>')
def get_video(filename):
    return send_from_directory(directory=".", path=filename)

if __name__ == '__main__':
    app.run(debug=False)
