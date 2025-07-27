
from transformers import pipeline

# 경량 모델 파이프라인 준비
small_pipe = pipeline("text2text-generation", model="google/flan-t5-small")
base_pipe = pipeline("text2text-generation", model="google/flan-t5-base")

def choose_model(user_message: str) -> str:
    if any(word in user_message.lower() for word in ["분석", "비교", "차이", "왜"]):
        return "google/flan-t5-base"
    else:
        return "google/flan-t5-small"

def estimate_tokens(text: str) -> int:
    return len(text.split())

def auto_route_response(query: str):
    model_id = choose_model(query)
    if model_id == "google/flan-t5-base":
        result = base_pipe(query, max_new_tokens=256)
        response = result[0]['generated_text']
    else:
        result = small_pipe(query, max_new_tokens=256)
        response = result[0]['generated_text']
    token_count = estimate_tokens(response)
    return response, model_id, token_count
