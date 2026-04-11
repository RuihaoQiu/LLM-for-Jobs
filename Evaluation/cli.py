import argparse
import os
from .runner import evaluate

def main():
    parser = argparse.ArgumentParser(
        description="Evaluation CLI: score predictions against gold data."
    )
    parser.add_argument(
        "--data",
        required=True,
        help=(
            "Path to predictions CSV. Required columns: min_salary, max_salary, currency, period"
        ),
    )
    parser.add_argument(
        "--task",
        required=True,
        choices=["salary", "skills", "title"],
        help="Task to evaluate (currently: salary)",
    )
    parser.add_argument(
        "--adapter",
        default="echo",
        help="Adapter to generate predictions (reserved; not used)",
    )
    args = parser.parse_args()

    if not os.path.exists(args.data):
        parser.error(f"--data file not found: {args.data}")

    # Only EchoAdapter here, but you can extend
    summary = evaluate(args.data, args.task)

    print("=== Evaluation Summary ===")
    print(summary)
    # for task, metrics in summary.items():
    #     print(f"[{task}]")
    #     for m, v in metrics.items():
    #         print(f"  {m}: {v:.4f}")

if __name__ == "__main__":
    main()
