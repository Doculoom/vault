# import os
# from sentence_transformers import SentenceTransformer
# from typing import List
# from app.core.config import settings
#
#
# def download_models(model_ids: List[str], save_path: str):
#     os.makedirs(save_path, exist_ok=True)
#     for model_id in model_ids:
#         print(f"Downloading model: {model_id}")
#         model = SentenceTransformer(model_id)
#         model_path = os.path.join(save_path, model_id.replace("/", "_"))
#         model.save(model_path)
#         print(f"Saved model {model_id} to {model_path}")
#
#
# if __name__ == "__main__":
#     model_ids = [settings.EMBEDDING_MODEL_ID]
#     save_path = settings.MODEL_SAVE_PATH
#     download_models(model_ids, save_path)
