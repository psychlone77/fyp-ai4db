import os
import time
from statistics import mean
from huggingface_hub import hf_hub_download
from llama_cpp import Llama

# --- Config ---
# MODEL_REPO = "Qwen/Qwen2.5-Coder-3B-Instruct-GGUF"
# MODEL_FILE = "qwen2.5-coder-3b-instruct-q4_k_m.gguf"

MODEL_REPO = "Qwen/Qwen2.5-Coder-7B-Instruct-GGUF"
MODEL_FILE = "qwen2.5-coder-7b-instruct-q4_k_m.gguf"

N_CTX = 2048
N_THREADS = int(os.getenv("LLAMA_THREADS", str(os.cpu_count() or 4)))
MAX_TOKENS = 1024
STOP_TOKENS = ["<|im_end|>"]

# Queries to run
QUERIES = [
    "I have a PostgreSQL database handling a heavy OLAP workload. "
    "The query plans show expensive sort operations. "
    "Suggest 3 specific knob configurations to improve performance.",

    "We have a write-heavy OLTP workload with frequent small transactions. "
    "Recommend WAL and checkpoint settings to minimize latency and avoid stalls.",

    "Mixed workload with both analytical queries and concurrent updates. "
    "Advise on indexing strategy and memory knobs (e.g., work_mem, shared_buffers).",
]

def build_prompt(user_text: str) -> str:
    return f"""
<|im_start|>system
You are a database expert.
<|im_end|>
<|im_start|>user
{user_text}
<|im_end|>
<|im_start|>assistant
""".strip()

def main():
    # --- Step 1: Download the model ---
    print(f"Downloading {MODEL_REPO}...")
    model_path = hf_hub_download(repo_id=MODEL_REPO, filename=MODEL_FILE)
    print(f"Model saved to: {model_path}")

    # --- Step 2: Load model ---
    print("Loading model into memory...")
    llm = Llama(
        model_path=model_path,
        n_ctx=N_CTX,
        n_threads=N_THREADS,
        verbose=False,
    )

    latencies = []
    token_counts = []
    speeds = []
    responses = []

    print("\n--- Running Queries ---")
    for idx, q in enumerate(QUERIES, start=1):
        prompt = build_prompt(q)
        print(f"\n[Query {idx}] Generating response...")
        start = time.perf_counter()
        output = llm(prompt, max_tokens=MAX_TOKENS, stop=STOP_TOKENS, echo=False)
        elapsed = time.perf_counter() - start

        text = output["choices"][0]["text"]
        usage = output.get("usage", {})
        completion_tokens = usage.get("completion_tokens")
        speed = (completion_tokens / elapsed) if completion_tokens else None

        latencies.append(elapsed)
        token_counts.append(completion_tokens if completion_tokens is not None else 0)
        speeds.append(speed if speed is not None else 0.0)
        responses.append(text)

        print(f"Latency: {elapsed:.2f}s | Tokens: {completion_tokens} | Speed: {speed:.2f} tok/s" if speed is not None
              else f"Latency: {elapsed:.2f}s | Tokens: {completion_tokens}")

    avg_latency = mean(latencies) if latencies else 0.0
    avg_tokens = mean([t for t in token_counts if t is not None]) if token_counts else 0.0
    avg_speed = mean([s for s in speeds if s is not None]) if speeds else 0.0

    print("\n--- Summary ---")
    print(f"Average Latency: {avg_latency:.2f} seconds over {len(QUERIES)} queries")
    print(f"Average Tokens: {avg_tokens:.2f}")
    print(f"Average Speed: {avg_speed:.2f} tokens/second")

    # --- Write results to file ---
    out_path = os.path.join(os.path.dirname(__file__), "qwen_7B_latency_results.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(f"Model: {MODEL_REPO}/{MODEL_FILE}\n")
        f.write(f"n_ctx: {N_CTX}, n_threads: {N_THREADS}, max_tokens: {MAX_TOKENS}\n")
        f.write(f"Queries run: {len(QUERIES)}\n\n")

        for i, (lat, tok, spd, resp) in enumerate(zip(latencies, token_counts, speeds, responses), start=1):
            f.write(f"Query {i} Latency: {lat:.4f}s | Tokens: {tok} | Speed: {spd:.4f} tok/s\n")
            f.write("Response:\n")
            f.write(resp.strip() + "\n")
            f.write("-" * 60 + "\n")

        f.write("\nSummary:\n")
        f.write(f"Average Latency: {avg_latency:.4f}s\n")
        f.write(f"Average Tokens: {avg_tokens:.2f}\n")
        f.write(f"Average Speed: {avg_speed:.2f} tok/s\n")

    print(f"\nResults written to: {out_path}")

if __name__ == "__main__":
    main()
