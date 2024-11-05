from utils.query import query_text, query_image, query_music
from utils.textPreprocessing import trim_incomplete_sentences, remove_text_in_parentheses_and_braces, extract_entities
from utils.textToSpeech import text_to_speech
from io import BytesIO
from PIL import Image, UnidentifiedImageError

# image and text processing
def generate_fun_fact(base_prompt, num_images, speed=1.0):
    prompt_template = f"Provide a fun fact about {base_prompt}. The generated text should either start with the term 'Did you know?' or contain 'Did you know?'. The information generated should always be true and rare."
    
    # Create the query payload
    for i in range(num_images):
        payload = {
            "inputs": prompt_template,
            "parameters": {
                "num_return_sequences": i + 1,
                "max_length": 700,
                "min_length": 200,
                "temperature": 0.9,
                "top_p": 0.9,
                "top_k": 50
            }
        }
    
    # Get the generated text
    response = query_text(payload)
    generated_text = response[0]["generated_text"]
    cleaned_text = generated_text.replace(prompt_template, "").strip()
    cleaned_text = trim_incomplete_sentences(generated_text.split(prompt_template)[-1].strip())
    cleaned_text = remove_text_in_parentheses_and_braces(cleaned_text)

    # Print generated and cleaned text for debugging
    print("Cleaned Text:", cleaned_text)

    # Extract entities from the generated text
    entities = extract_entities(cleaned_text)
    print("Entities:", entities)
    images = []

    # For each entity, generate an image
    for entity in entities:
        try:
            image_prompt = f"{entity}"
            print("Image Prompt:", image_prompt)
            image_payload = {"inputs": image_prompt}
            image_content = query_image(image_payload)
            image = Image.open(BytesIO(image_content))
            images.append(image)
        except UnidentifiedImageError as e:
            print(f"Failed to generate image for '{entity}': {str(e)}")
        if len(images) >= num_images:
            break

    # If not enough entities were found, dynamically generate image prompts using query_text
    if len(images) < num_images:
        n = num_images - len(images)
        for i in range(n):
            try:
                # Dynamically generate variations of the base prompt for images using query_text
                for entity in entities:
                    variation_payload = {
                        "inputs": f"Create different variations of the following: {entity}",
                        "parameters": {
                            "num_return_sequences": i + 1,
                            "max_length": 100,
                            "min_length": 50,
                            "temperature": 0.8,
                            "top_p": 0.9,
                            "top_k": 40
                        }
                    }
                    variation_response = query_text(variation_payload)
                    variation_prompt = variation_response[0]["generated_text"]

                # Clean the variation prompt in the same manner
                cleaned_variation_prompt = variation_prompt.replace(f"Create different artistic styles or variations of the following: {base_prompt}", "").strip()
                cleaned_variation_prompt = trim_incomplete_sentences(cleaned_variation_prompt.split(f"Create different artistic styles or variations of the following: {base_prompt}")[-1].strip())
                cleaned_variation_prompt = remove_text_in_parentheses_and_braces(cleaned_variation_prompt)

                # Use the cleaned variation prompt for generating images
                image_prompt = f"{base_prompt} {cleaned_variation_prompt}"
                print("Dynamic Image Prompt:", cleaned_variation_prompt)
                image_payload = {"inputs": image_prompt}
                image_content = query_image(image_payload)
                image = Image.open(BytesIO(image_content))
                images.append(image)
            except UnidentifiedImageError as e:
                print(f"Failed to generate dynamic image: {str(e)}")
            if len(images) >= num_images:
                break

    # Generate the audio based on the cleaned text
    audio_bytes, audio_file_path, temp_audio_file_path = text_to_speech(cleaned_text, speed)

    return audio_file_path, temp_audio_file_path, images, cleaned_text
