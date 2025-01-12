from typing import Optional, List
import threading
import os

from sentence_transformers import SentenceTransformer
from app.core.config import settings


class EmbeddingsService:
    def __init__(self):
        self._model_cache = {}
        self._cache_lock = threading.Lock()

    def _get_model(self, model_id: str) -> SentenceTransformer:
        with self._cache_lock:
            if model_id in self._model_cache:
                print("Using cache")
                return self._model_cache[model_id]
            else:
                print("Using downloaded model")
                local_model_dir = model_id.replace("/", "_")
                local_path = os.path.join(settings.MODEL_SAVE_PATH, local_model_dir)

                if os.path.exists(local_path):
                    model = SentenceTransformer(local_path)
                else:
                    model = SentenceTransformer(model_id)

                self._model_cache[model_id] = model
                return model

    def generate_embedding(self, text: str, model_id: Optional[str] = None) -> List[float]:
        model_id = model_id or settings.EMBEDDING_MODEL_ID
        model = self._get_model(model_id)
        embedding = model.encode(text)
        return embedding.tolist()
