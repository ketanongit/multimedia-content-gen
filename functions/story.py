from utils.query import query_text, query_image, query_music
from utils.textPreprocessing import trim_incomplete_sentences, remove_text_in_parentheses_and_braces, extract_entities
from utils.textToSpeech import text_to_speech
from io import BytesIO
from PIL import Image

# image and text processing for generating a story
def generate_story(base_prompt, speed=1.0):
    prompt_template = f"Create a detailed story about {base_prompt}. The story should have a beginning, middle, and end, and should include compelling characters, vivid descriptions, and a strong narrative arc."
    
    # Create the query payload
    payload = {
        "inputs": prompt_template,
        "parameters": {
            "max_length": 1000,
            "min_length": 500,
            "temperature": 0.8,
            "top_p": 0.9,
            "top_k": 50
        }
    }

    # Get the generated story text
    response = query_text(payload)
    generated_text = response[0]["generated_text"]
    cleaned_text = generated_text.replace(prompt_template, "").strip()
    cleaned_text = trim_incomplete_sentences(generated_text.split(prompt_template)[-1].strip())
    cleaned_text = remove_text_in_parentheses_and_braces(cleaned_text)

    # Print generated and cleaned text for debugging
    print("Cleaned Text:", cleaned_text)

    # Extract entities from the story for generating images
    entities = extract_entities(cleaned_text)
    print("Entities:", entities)
    images = []

    # Generate images based on the entities in the story
    for entity in entities:
        image_prompt = f"{entity}"
        print("Image Prompt:", image_prompt)
        image_payload = {"inputs": image_prompt}
        image_content = query_image(image_payload)
        image = Image.open(BytesIO(image_content))
        images.append(image)
        if len(images) >= len(entities):
            break

    # Generate audio for the story text
    audio_bytes, audio_file_path, temp_audio_file_path = text_to_speech(cleaned_text, speed)

    return audio_file_path, temp_audio_file_path, images, cleaned_text
