#utils/query.py
import requests

TEXT_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
IMAGE_API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev"
MUSIC_URL = "https://api-inference.huggingface.co/models/facebook/musicgen-small"
DOMAIN_API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"  # For zero-shot classification

HEADERS = {"Authorization": "Bearer YOUR_HUGGINGFACE_KEY"}

def query_text(payload):
    response = requests.post(TEXT_API_URL, headers=HEADERS, json=payload)
    return response.json()

def query_image(payload):
    response = requests.post(IMAGE_API_URL, headers=HEADERS, json=payload)
    return response.content

def query_music(payload):
    response = requests.post(MUSIC_URL, headers=HEADERS, json=payload)
    return response.content

# New function for zero-shot classification
def query_domain(payload):
    response = requests.post(DOMAIN_API_URL, headers=HEADERS, json=payload)
    return response.json()
