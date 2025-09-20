import argparse
# from adapters import EchoAdapter
from runner import evaluate

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", required=True)
    parser.add_argument("--task", required=True)
    parser.add_argument("--adapter", default="echo")
    args = parser.parse_args()

    # Only EchoAdapter here, but you can extend
    # adapter = EchoAdapter()
    summary = evaluate(args.dataset, args.task)

    print("=== Evaluation Summary ===")
    print(summary)
    # for task, metrics in summary.items():
    #     print(f"[{task}]")
    #     for m, v in metrics.items():
    #         print(f"  {m}: {v:.4f}")

if __name__ == "__main__":
    main()
