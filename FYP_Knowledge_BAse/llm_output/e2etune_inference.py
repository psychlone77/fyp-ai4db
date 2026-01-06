import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, "..", ".env")
load_dotenv(ENV_PATH)

# Enable new HF Inference API
os.environ.setdefault("HF_HUB_ENABLE_HF_INFERENCE", "1")

MODEL_NAME = "springhxm/E2ETune"

def get_client() -> InferenceClient:
    token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGINGFACEHUB_API_TOKEN")
    if not token:
        raise RuntimeError(f"HF_TOKEN is not set (tried .env at: {ENV_PATH})")
    return InferenceClient(
        model=MODEL_NAME,
        token=token,
        provider="hf-inference",  # explicitly use HF Inference API
    )

def get_inference(input_text: str) -> str:
    client = get_client()
    return client.text_generation(
        input_text,
        max_new_tokens=256,
        temperature=0.1,
        top_p=0.9,
        do_sample=False,
        repetition_penalty=1.05,
    )

if __name__ == "__main__":
    input_string = (
        'workload features: size of workload: 15.0; read ratio: 1.0; '
        'group by ratio: 0.8; order by ratio: 0.87; '
        '"You are an expert in database, you are to optimize the parameters of database..."'
    )
    print("Generated Text:\n", get_inference(input_string))
