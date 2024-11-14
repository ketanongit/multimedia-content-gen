#utils/textPreprocessing.py
import re
import spacy
from utils.query import query_domain  

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

def trim_incomplete_sentences(text):
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    if not sentences[-1].endswith(('.', '?', '!')):
        sentences = sentences[:-1]
    return ' '.join(sentences)

def remove_text_in_parentheses_and_braces(text):
    text = re.sub(r'\(.*?\)', '', text)
    text = re.sub(r'\{.*?\}', '', text)
    return text

def extract_entities(text):
    # Expanded list of image-friendly labels
    image_friendly_labels = (
        "PERSON", "ORG", "GPE", "LOC", "PRODUCT", "EVENT", "ANIMAL", 
        "FOOD", "FRUIT", "VEGETABLE", "OBJECT", "SCENE", "COLOR", 
        "WEATHER", "ACTION", "TRANSPORT", "BUILDING","BRAND LOGO"
    )

    # Use spaCy to extract entities along with their positions
    doc = nlp(text)
    entities_with_positions = [
        (ent.text, ent.start_char) 
        for ent in doc.ents if ent.label_ in image_friendly_labels
    ]

    # Sort the entities by their position in the text to maintain sequential order
    sorted_entities = [entity[0] for entity in sorted(entities_with_positions, key=lambda x: x[1])]

    # If no entities are found, use a fallback list for zero-shot classification
    if not sorted_entities:
        fallback_entities = ["object", "scene", "animal", "food", "action", "location"]
        zero_shot_result = query_domain({
            "inputs": text,
            "parameters": {
                "candidate_labels": fallback_entities
            }
        })
        # Extract classified entities from the zero-shot result
        classified_entities = zero_shot_result.get("labels", [])
        return list(set(classified_entities))

    # Return the sequentially ordered entities
    return sorted_entities
