from api_config import init_clients
from exp import run_exp_1a, run_exp_1b, run_exp_2a, run_exp_2b, run_exp_2c
from prompt_utils import get_bloom


def main():
    print("[INFO] Initializing LLM clients...")
    try:
        clients = init_clients()
    except ValueError as e:
        print(f"[ERROR] Failed to initialize clients: {e}")
        print("[ERROR] Please ensure your .env file is correctly set up with API keys.")
        return

    print("[INFO] Pre-loading Bloom data...")
    get_bloom()

    print("[INFO] Starting experiments...")
    run_exp_1a(clients)
    run_exp_1b(clients)
    run_exp_2a(clients)
    run_exp_2b(clients)
    run_exp_2c(clients)

    print("\n[INFO] All experiments completed.")


if __name__ == "__main__":
    main()
