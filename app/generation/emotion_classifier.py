import requests
import os
HUGGING_FACE_API_KEY = os.getenv("HUGGING_FACE_API_KEY")

API_URL = "https://api-inference.huggingface.co/models/dima806/facial_emotions_image_detection"
headers = {"Authorization": f"Bearer {HUGGING_FACE_API_KEY}"}

def query(filepath):
    options = {"wait_for_model":True}
    with open(filepath, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data, json=options)
    response_json = response.json()
    if 'error' in response_json:
        print("error\n")
        return query(filepath)
    return response_json

def classify_face(filepath):
    result = query(filepath)
    happines_score = result[0]["score"]
    return happines_score
