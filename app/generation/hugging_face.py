import requests
import os
from dotenv import load_dotenv

class HuggingFaceAPI:

    def __init__(self) -> None:
        load_dotenv()
        HUGGING_FACE_API_KEY = os.getenv("HUGGING_FACE_API_KEY")
        self.BASE_API_URL = "https://api-inference.huggingface.co/models/"
        self.headers = {"Authorization": f"Bearer {HUGGING_FACE_API_KEY}"}

    def query(self, filepath, model_path):
        API_URL = self.BASE_API_URL + model_path
        options = {"wait_for_model":True}
        with open(filepath, "rb") as f:
            data = f.read()
        response = requests.post(API_URL, headers=self.headers, data=data, json=options)
        response_json = response.json()
        # continue to query model until cold-start is finished
        if 'error' in response_json:
            print("error\n")
            return self.query(filepath)
        return response_json
    
    def classify_face(self, filepath):
        model_path = "dima806/facial_emotions_image_detection"
        result = self.query(filepath,model_path)
        happines_score = result[0]["score"]
        return happines_score
