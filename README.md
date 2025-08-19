# AI-Powered Video Generation Pipeline

This project is a Flask-based web application that automatically generates short, engaging videos from user prompts. It combines several AI models and technologies to create videos with narration, images, background music, and animated subtitles.

## Features

- **Automatic Video Generation:** Creates videos from a simple text prompt.
- **Multiple Content Modes:** Can generate videos in two styles: "Fun Fact" or "Story".
- **AI-Powered Content:**
    - **Text:** Uses a large language model to generate scripts.
    - **Images:** Generates relevant images based on the script's content.
    - **Music:** Creates background music that matches the prompt.
- **Text-to-Speech:** Converts the generated script into natural-sounding speech.
- **Animated Subtitles:** Transcribes the audio and creates word-by-word animated subtitles.
- **Web Interface:** Simple and easy-to-use web interface to generate videos.

## How it Works

The video generation process is a pipeline of several steps:

1.  **Prompting:** The user provides a prompt (e.g., "a fun fact about the Roman Empire") through the web interface.
2.  **Text Generation:** The application sends a detailed prompt to a Hugging Face language model (`mistralai/Mistral-7B-Instruct-v0.3`) to generate a script.
3.  **Text-to-Speech:** The generated script is converted to an MP3 audio file using Google Text-to-Speech (`gTTS`). The speed of the speech can be adjusted.
4.  **Image Generation:**
    -   The script is analyzed using `spacy` to extract named entities (e.g., people, places, objects).
    -   These entities are used as prompts for a Hugging Face image generation model (`black-forest-labs/FLUX.1-dev`) to create a set of relevant images.
5.  **Music Generation:** A prompt is sent to a Hugging Face music generation model (`facebook/musicgen-small`) to create background music.
6.  **Subtitle Generation:** The speech audio is transcribed using OpenAI's `whisper` model to get the text and timings for each word.
7.  **Video Assembly:**
    -   The generated images are combined into a sequence using `moviepy`.
    -   The speech audio and background music are mixed together using `pydub`.
    -   Animated text clips for each word are created using `Pillow` and `moviepy`, and overlaid on the video according to the transcription timings.
    -   The final video is rendered with the combined audio and subtitles.

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Install Python dependencies:**
    It is recommended to use a virtual environment.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```
    *(Note: A `requirements.txt` file is not provided. You will need to create one based on the dependencies listed below.)*

3.  **Download SpaCy Model:**
    You need to download the `en_core_web_sm` model for `spacy`:
    ```bash
    python -m spacy download en_core_web_sm
    ```

4.  **Install FFmpeg:**
    `moviepy` requires FFmpeg for video processing. You can install it using your system's package manager.
    -   **On macOS (using Homebrew):**
        ```bash
        brew install ffmpeg
        ```
    -   **On Debian/Ubuntu:**
        ```bash
        sudo apt-get install ffmpeg
        ```
    -   **On Windows:**
        Download the FFmpeg binaries from the [official website](https://ffmpeg.org/download.html) and add the `bin` directory to your system's PATH.

## Usage

1.  **Set up your Hugging Face API Key** (see Configuration section below).

2.  **Run the Flask application:**
    ```bash
    python app.py
    ```

3.  **Open your web browser** and navigate to `http://127.0.0.1:5000`.

4.  **Select a video mode** (Fun Fact or Story), enter your prompt and other options, and click "Generate Video".

## Configuration

The application requires a Hugging Face API key to use the text, image, and music generation models.

1.  **Get a Hugging Face API Key:**
    -   Go to the [Hugging Face website](https://huggingface.co/).
    -   Create an account or log in.
    -   Navigate to your profile settings and find the "Access Tokens" section.
    -   Create a new token with "read" permissions.

2.  **Set the API Key:**
    Open the `utils/query.py` file and replace `"Bearer YOUR_HUGGINGFACE_KEY"` with your actual API key:
    ```python
    # utils/query.py
    ...
    HEADERS = {"Authorization": "Bearer hf_YourActualApiKeyHere"}
    ...
    ```

## Dependencies

This project relies on the following Python libraries:

- `Flask`
- `requests`
- `pydub`
- `gTTS`
- `Pillow`
- `spacy`
- `moviepy`
- `openai-whisper`
- `torch` (often a dependency for ML models)
- `torchaudio`
- `transformers`

You will also need:
- The `en_core_web_sm` model for `spacy`.
- `ffmpeg` for video processing.
- The `arial.ttf` font (usually pre-installed, but may be required for subtitle generation).