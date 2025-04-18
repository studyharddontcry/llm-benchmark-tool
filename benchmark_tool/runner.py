import argparse
from typing import List, Dict, Any

from generator import CodeGenerator
from tester import CodeTester
from metrics import CodeMetrics
from tqdm import tqdm


class BenchmarkRunner:
    """Programmatic wrapper around the end‑to‑end benchmarking pipeline."""

    def __init__(
        self,
        description: str,
        model: str = "qwen2.5-coder:3b",
        temperature: float = 0.3,
        runs: int = 10,
    ):
        self.description = description
        self.model = model
        self.temperature = temperature
        self.runs = runs

        self.generator = CodeGenerator(model_name=model, temperature=temperature)
        self.tester = CodeTester()
        self.metrics_calculator = CodeMetrics()

    def run(self) -> Dict[str, Any]:
        """Execute the configured number of generation–test–metric cycles.

        Returns
        -------
        Dict[str, Any]
            A dictionary with keys:
            - "metrics": list[dict]   raw metrics for each run
            - "codes":   list[str]    generated code strings
            - "test_outputs": list[str] pytest output for each run
            - "avg": dict             averaged metrics across runs
        """
        all_metrics: List[Dict[str, Any]] = []
        all_codes: List[str] = []
        all_test_outputs: List[str] = []

        for _ in tqdm(range(self.runs), desc="Benchmarking runs"):
            code_str, gen_time = self.generator.generate(self.description)
            success, test_output = self.tester.test_code(code_str)
            metrics = self.metrics_calculator.evaluate(
                code_str, success, gen_time
            )

            all_metrics.append(metrics)
            all_codes.append(code_str)
            all_test_outputs.append(test_output)

        return {
            "metrics": all_metrics,
            "codes": all_codes,
            "test_outputs": all_test_outputs,
            "avg": self.metrics_calculator.average_metrics(all_metrics),
        }


def main(argv: List[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description=(
            "End‑to‑end runner for generating, testing and evaluating code "
            "produced by an LLM."
        )
    )
    parser.add_argument(
        "--model",
        type=str,
        default="qwen2.5-coder:3b",
        help="Name of the model to use (default: qwen2.5-coder:3b).",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.3,
        help="Temperature for the model (default: 0.3).",
    )
    parser.add_argument(
        "--description",
        type=str,
        required=True,
        help="Short description of the function or code to generate.",
    )
    parser.add_argument(
        "--runs",
        type=int,
        default=10,
        help="Number of code generations to run (default: 10).",
    )

    args = parser.parse_args(argv)

    runner = BenchmarkRunner(
        description=args.description,
        model=args.model,
        temperature=args.temperature,
        runs=args.runs,
    )
    report = runner.run()

    print("\n" + "=" * 80)
    print(f"SUMMARY FOR: {args.description}")
    print("=" * 80)
    print("\nAVERAGE METRICS ACROSS ALL RUNS")
    print("-" * 40)
    for key, val in report["avg"].items():
        print(f"{key:.<30} {val:.4f}")


if __name__ == "__main__":
    main()
