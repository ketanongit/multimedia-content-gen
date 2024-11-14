from concurrent.futures import ThreadPoolExecutor, as_completed
import os
from tempfile import mktemp
from utils.query import query_text, query_image, query_music
from utils.textPreprocessing import trim_incomplete_sentences, remove_text_in_parentheses_and_braces, extract_entities
from utils.textToSpeech import text_to_speech
from PIL import Image, UnidentifiedImageError

# functions/funFact.py
def generate_fun_fact(base_prompt, num_images, speed=1.0):
    prompt_template = f"Provide a single fun fact about {base_prompt}. The generated text should atleast be of length 2000 words and should either start with the term 'Did you know?' or contain 'Did you know?'. The information generated should always be true and rare."

    # Parallelize the text generation API request
    text_payload = {
        "inputs": prompt_template,
        "parameters": {
            "num_return_sequences": 1,
            "max_length": 700,
            "min_length": 200,
            "temperature": 0.9,
            "top_p": 0.9,
            "top_k": 50
        }
    }

    # Create an executor for parallel tasks
    with ThreadPoolExecutor() as executor:
        # Submit the text generation task
        text_future = executor.submit(query_text, text_payload)
        
        # Wait for the text response
        generated_text = text_future.result()[0]["generated_text"]
        cleaned_text = generated_text.replace(prompt_template, "").strip()
        cleaned_text = trim_incomplete_sentences(generated_text.split(prompt_template)[-1].strip())
        cleaned_text = remove_text_in_parentheses_and_braces(cleaned_text)
        
        print("Cleaned Text:", cleaned_text)
        
        # Extract entities for image generation
        entities = extract_entities(cleaned_text)
        print("Entities:", entities)

        # Parallelize image generation tasks
        image_futures = [
            executor.submit(query_image, {"inputs": entity})
            for entity in entities[:num_images]
        ]

        # Collect image results
        image_files = []
        for future in as_completed(image_futures):
            try:
                image_content = future.result()
                temp_image_path = mktemp(suffix=".png")
                with open(temp_image_path, "wb") as image_file:
                    image_file.write(image_content)
                image_files.append(temp_image_path)
            except UnidentifiedImageError as e:
                print(f"Failed to generate image: {str(e)}")
            if len(image_files) >= num_images:
                break

        # If not enough entities were found, dynamically generate image prompts using query_text
        if len(image_files) < num_images:
            n = num_images - len(image_files)
            variation_futures = []

            # Dynamically generate variations of entities
            for i in range(n):
                for entity in entities:
                    variation_payload = {
                        "inputs": f"provide an image prompt for {entity}",
                        "parameters": {
                            "num_return_sequences": i,
                            "max_length": 100,
                            "min_length": 50,
                            "temperature": 0.8,
                            "top_p": 0.9,
                            "top_k": 40
                        }
                    }
                    variation_futures.append(executor.submit(query_text, variation_payload))

            # Process generated variations
            for future in as_completed(variation_futures):
                try:
                    variation_response = future.result()
                    variation_prompt = variation_response[0]["generated_text"]
                    
                    # Remove the phrase from the variation prompt
                    variation_prompt = variation_prompt.replace("provide an image prompt for", "").strip()
                    
                    # Clean the variation prompt
                    cleaned_variation_prompt = trim_incomplete_sentences(
                        remove_text_in_parentheses_and_braces(variation_prompt)
                    )
                    print("Dynamic Image Prompt:", cleaned_variation_prompt)

                    # Generate an image based on the cleaned variation prompt
                    image_payload = {"inputs": cleaned_variation_prompt}
                    image_content = query_image(image_payload)
                    temp_image_path = mktemp(suffix=".png")
                    with open(temp_image_path, "wb") as image_file:
                        image_file.write(image_content)
                    image_files.append(temp_image_path)
                except UnidentifiedImageError as e:
                    print(f"Failed to generate dynamic image: {str(e)}")
                if len(image_files) >= num_images:
                    break

        # Submit the text-to-speech task in parallel
        audio_future = executor.submit(text_to_speech, cleaned_text, speed)
        audio_bytes, audio_file_path, temp_audio_file_path = audio_future.result()

    return audio_file_path, temp_audio_file_path, image_files, cleaned_text
