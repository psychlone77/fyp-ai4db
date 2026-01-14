import os
import shutil
from dotenv import load_dotenv
from huggingface_hub import snapshot_download
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, "..", "..", ".env")
load_dotenv(ENV_PATH)

MODEL_NAME = "springhxm/E2ETune"
GGUF_OUTPUT_DIR = os.path.join(BASE_DIR, "gguf_models")

def download_model():
    """Download model from HuggingFace."""
    token = os.environ.get("HF_TOKEN")
    
    print("Downloading model...")
    model_path = snapshot_download(
        repo_id=MODEL_NAME,
        token=token,
        local_dir=os.path.join(BASE_DIR, "downloaded_model")
    )
    
    print(f"Model downloaded to: {model_path}")
    return model_path

def save_for_inference(model_path):
    """Load and save model in a format optimized for inference."""
    token = os.environ.get("HF_TOKEN")
    
    print("Loading model and tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(
        model_path,
        token=token,
        local_files_only=True
    )
    
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        token=token,
        torch_dtype=torch.float16,
        device_map="cpu",
        low_cpu_mem_usage=True,
        local_files_only=True
    )
    
    # Set to eval mode for inference only
    model.eval()
    
    # Create output directory
    os.makedirs(GGUF_OUTPUT_DIR, exist_ok=True)
    inference_model_path = os.path.join(GGUF_OUTPUT_DIR, "inference_model")
    
    print(f"Saving inference-optimized model to: {inference_model_path}")
    
    # Save model and tokenizer
    model.save_pretrained(
        inference_model_path,
        safe_serialization=True,
        max_shard_size="2GB"
    )
    tokenizer.save_pretrained(inference_model_path)
    
    # Copy config files
    config_files = ["config.json", "generation_config.json", "tokenizer_config.json"]
    for config_file in config_files:
        src = os.path.join(model_path, config_file)
        if os.path.exists(src):
            shutil.copy(src, inference_model_path)
    
    print(f"Model saved successfully to: {inference_model_path}")
    print("\nModel is now ready for inference-only usage.")
    print(f"Load it with: AutoModelForCausalLM.from_pretrained('{inference_model_path}')")
    
    return inference_model_path

if __name__ == "__main__":
    try:
        # Download model
        model_path = download_model()
        
        # Save optimized version for inference
        inference_path = save_for_inference(model_path)
        
        print("\n" + "="*60)
        print("SUCCESS: Model is ready for inference!")
        print(f"Location: {inference_path}")
        print("="*60)
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()