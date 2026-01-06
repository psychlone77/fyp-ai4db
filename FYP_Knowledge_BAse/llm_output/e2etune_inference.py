import os
from dotenv import load_dotenv
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, "..", ".env")
load_dotenv(ENV_PATH)

MODEL_NAME = "springhxm/E2ETune"

def load_model_and_tokenizer():
    """Load the model and tokenizer with authentication if needed."""
    token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGINGFACEHUB_API_TOKEN")
    
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, token=token)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        token=token,
        dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        device_map="auto" if torch.cuda.is_available() else None
    )
    
    return model, tokenizer

def get_inference(input_text: str, model, tokenizer) -> str:
    """Generate output from the model given input text."""
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    # Tokenize input
    inputs = tokenizer(input_text, return_tensors="pt").to(device)
    
    # Generate output
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=256,
            temperature=0.1,
            top_p=0.9,
            do_sample=False,
            repetition_penalty=1.05,
        )
    
    # Decode the output
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return generated_text

if __name__ == "__main__":
    # Define input features
    input_features = (
        "workload features: size of workload: 15.0; read ratio: 1.0; group by ratio: 0.8; order by ratio: 0.87; "
        "avg query length: 56.2; number of joins: 2; filter ratio: 0.5;\n"
        "query plans in workload: Aggregate(cost=1000.0)(Seq Scan(cost=650.0)); Nested Loop(cost=2000.0)(Index Scan(cost=1200.0); Seq Scan(cost=800.0));\n"
        "inner metrics: buffer hit ratio: 0.99; average response time: 120.4ms; lock wait: 0.02; rows returned: 1023; deadlocks: 0;"
    )
    
    # Load model and tokenizer
    print("Loading model and tokenizer...")
    model, tokenizer = load_model_and_tokenizer()
    
    # Get inference
    print("Generating output...")
    result = get_inference(input_features, model, tokenizer)
    print("\nGenerated Text:\n", result)
