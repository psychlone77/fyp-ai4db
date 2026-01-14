import os
import time
from dotenv import load_dotenv
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, "..", ".env")
load_dotenv(ENV_PATH)

# Use local inference-optimized model if available
INFERENCE_MODEL_PATH = os.path.join(BASE_DIR, "hf_offload", "gguf_models", "inference_model")
MODEL_NAME = INFERENCE_MODEL_PATH if os.path.exists(INFERENCE_MODEL_PATH) else "springhxm/E2ETune"

def load_model_and_tokenizer_quantized():
    """Load model with 8-bit quantization for CPU."""
    token = os.environ.get("HF_TOKEN")
    
    print(f"Loading quantized model from: {MODEL_NAME}")
    
    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME,
        token=token,
        local_files_only=os.path.exists(INFERENCE_MODEL_PATH)
    )

    # Option 1: Load with 8-bit quantization (requires bitsandbytes)
    try:
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            token=token,
            load_in_8bit=True,
            device_map="auto",
            low_cpu_mem_usage=True,
            local_files_only=os.path.exists(INFERENCE_MODEL_PATH)
        )
        print("Loaded with 8-bit quantization")
    except Exception as e:
        print(f"8-bit loading failed: {e}")
        print("Falling back to CPU with reduced precision...")
        
        # Option 2: Load with CPU offloading and disk offload
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            token=token,
            torch_dtype=torch.float32,  # Use float32 for CPU
            device_map="auto",
            low_cpu_mem_usage=True,
            offload_folder="offload",  # Offload to disk if needed
            offload_state_dict=True,
            local_files_only=os.path.exists(INFERENCE_MODEL_PATH)
        )
    
    model.eval()
    return model, tokenizer

def load_model_with_cpu_offload():
    """Load model with aggressive CPU offloading."""
    token = os.environ.get("HF_TOKEN")
    
    print(f"Loading model with CPU offload from: {MODEL_NAME}")
    
    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME,
        token=token,
        local_files_only=os.path.exists(INFERENCE_MODEL_PATH)
    )

    # Create offload folder
    offload_dir = os.path.join(BASE_DIR, "offload")
    os.makedirs(offload_dir, exist_ok=True)

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        token=token,
        torch_dtype=torch.float32,
        device_map="auto",
        low_cpu_mem_usage=True,
        offload_folder=offload_dir,
        offload_state_dict=True,
        max_memory={"cpu": "12GB"},  # Adjust based on your RAM
        local_files_only=os.path.exists(INFERENCE_MODEL_PATH)
    )
    
    model.eval()
    return model, tokenizer

def get_inference(input_text: str, model, tokenizer, max_new_tokens=512) -> dict:
    """Generate output from the model given input text and return with timing info."""
    
    print(f"\n{'='*60}")
    print(f"Starting inference with max_new_tokens={max_new_tokens}")
    print(f"{'='*60}\n")
    
    # Start timing - tokenization
    tokenization_start = time.time()
    inputs = tokenizer(
        input_text, 
        return_tensors="pt",
        max_length=512,  # Increased input length
        truncation=True
    )
    tokenization_time = time.time() - tokenization_start
    
    # Move to same device as model
    device = next(model.parameters()).device
    inputs = {k: v.to(device) for k, v in inputs.items()}
    
    # Start timing - generation
    generation_start = time.time()
    
    # Generate output with no_grad for inference
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,  # Increased output size
            temperature=0.1,
            top_p=0.9,
            do_sample=False,
            num_beams=1,  # Disable beam search for speed
            repetition_penalty=1.05,
        )
    
    generation_time = time.time() - generation_start
    
    # Start timing - decoding
    decoding_start = time.time()
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    decoding_time = time.time() - decoding_start
    
    # Remove input from output
    input_length = len(tokenizer.decode(inputs['input_ids'][0], skip_special_tokens=True))
    output_text = generated_text[input_length:].strip()
    
    # Calculate tokens per second
    output_tokens = len(outputs[0]) - len(inputs['input_ids'][0])
    tokens_per_second = output_tokens / generation_time if generation_time > 0 else 0
    
    # Total time
    total_time = tokenization_time + generation_time + decoding_time
    
    # Return results with timing info
    return {
        "output": output_text,
        "timing": {
            "tokenization_time": tokenization_time,
            "generation_time": generation_time,
            "decoding_time": decoding_time,
            "total_time": total_time,
            "tokens_generated": output_tokens,
            "tokens_per_second": tokens_per_second
        }
    }

if __name__ == "__main__":
    # Define input features
    input_features = (
        "workload features: size of workload: 15.0; read ratio: 1.0; group by ratio: 0.8; order by ratio: 0.87; "
        "avg query length: 56.2; number of joins: 2; filter ratio: 0.5;\n"
        "query plans in workload: Aggregate(cost=1000.0)(Seq Scan(cost=650.0)); Nested Loop(cost=2000.0)(Index Scan(cost=1200.0); Seq Scan(cost=800.0));\n"
        "inner metrics: buffer hit ratio: 0.99; average response time: 120.4ms; lock wait: 0.02; rows returned: 1023; deadlocks: 0;"
    )
    
    print("="*60)
    print("Attempting to load model with CPU optimizations...")
    print("="*60)
    
    # Start timing model loading
    load_start = time.time()
    
    try:
        # Try quantized loading first
        print("\nTrying 8-bit quantization...")
        model, tokenizer = load_model_and_tokenizer_quantized()
    except Exception as e:
        print(f"Quantized loading failed: {e}")
        print("\nTrying CPU offload...")
        model, tokenizer = load_model_with_cpu_offload()
    
    load_time = time.time() - load_start
    print(f"\n✓ Model loaded in {load_time:.2f} seconds")
    
    # Get inference with timing
    print("\nGenerating output...")
    result = get_inference(input_features, model, tokenizer, max_new_tokens=1000)
    
    # Display results
    print("\n" + "="*60)
    print("GENERATED OUTPUT:")
    print("="*60)
    print(result["output"])
    
    print("\n" + "="*60)
    print("TIMING STATISTICS:")
    print("="*60)
    print(f"Model Loading Time:    {load_time:.4f} seconds")
    print(f"Tokenization Time:     {result['timing']['tokenization_time']:.4f} seconds")
    print(f"Generation Time:       {result['timing']['generation_time']:.4f} seconds")
    print(f"Decoding Time:         {result['timing']['decoding_time']:.4f} seconds")
    print(f"Total Inference Time:  {result['timing']['total_time']:.4f} seconds")
    print(f"Tokens Generated:      {result['timing']['tokens_generated']}")
    print(f"Tokens per Second:     {result['timing']['tokens_per_second']:.2f}")
    print("="*60)
