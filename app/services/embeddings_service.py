from typing import Optional
import google.generativeai as genai
from google.cloud.firestore_v1.vector import Vector
import os


genai.configure(api_key=os.environ["GEMINI_API_KEY"])


class EmbeddingsService:
    @staticmethod
    def generate_embedding(text: str, model_id: Optional[str]) -> list[float]:
        result = genai.embed_content(model=model_id, content=text)
        return Vector(result['embedding'])
