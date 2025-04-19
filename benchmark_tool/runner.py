import argparse
from typing import List, Dict, Any

from generator import CodeGenerator
from tester import CodeTester
from metrics import CodeMetrics, append_csv_row
from tqdm import tqdm


class BenchmarkRunner:
    """Programmatic wrapper around the end-to-end benchmarking pipeline."""

    def __init__(
        self,
        task: str,
        description: str,
        model: str = "qwen2.5-coder:3b",
        temperature: float = 0.3,
        runs: int = 10,
    ):
        self.task = task
        self.description = description
        self.model = model
        self.temperature = temperature
        self.runs = runs

        self.generator = CodeGenerator(model_name=model, temperature=temperature)
        self.tester = CodeTester()
        self.metrics = CodeMetrics()
        
        # compute & cache human reference once
        self.ref_raw = self.metrics.evaluate_reference(task)
        
    def _write_csv(self, run_ix: str | int,
                   gen_time: float,
                   ratio_dict: Dict[str, float]) -> None:
        row = {
            "model": self.model,
            "temperature": self.temperature,
            "task": self.task,
            "run_ix": run_ix,
            "generation_time_s": gen_time,
            **ratio_dict,
        }
        append_csv_row(row)

    def run(self) -> Dict[str, Any]:
        """Execute generation–test–metric cycles and log CSV rows."""
        all_raw:  List[Dict[str, Any]] = []
        all_code: List[str]             = []
        all_out:  List[str]             = []

        for i in tqdm(range(1, self.runs + 1), desc="Benchmarking runs"):
            code_str, gen_time = self.generator.generate(self.description)
            success, test_out  = self.tester.test_code(code_str)
            raw_metrics        = self.metrics.evaluate(code_str, success, gen_time)

            # ratios for this run
            ratio_dict = self.metrics.normalise(raw_metrics, self.ref_raw)
            self._write_csv(i, gen_time, ratio_dict)

            # collect
            all_raw.append(raw_metrics)
            all_code.append(code_str)
            all_out.append(test_out)

        # session average
        avg_raw   = self.metrics.average_metrics(all_raw)
        ratio_avg = self.metrics.normalise(avg_raw, self.ref_raw)
        self._write_csv("avg", avg_raw["generation_time_s"], ratio_avg)

        return {
            "metrics":       all_raw,
            "codes":         all_code,
            "test_outputs":  all_out,
            "avg":           avg_raw,
        }


# ----------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------
def main(argv: List[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Generate, test, evaluate and log normalised metrics."
    )
    parser.add_argument(
        "--task",
        required=True,
        help="Task ID – must match HumanWrittenCodes/<task>.py",
    )
    parser.add_argument(
        "--description",
        required=True,
        help="Prompt / description for the LLM.",
    )
    parser.add_argument("--model", default="qwen2.5-coder:3b")
    parser.add_argument("--temperature", type=float, default=0.3)
    parser.add_argument("--runs", type=int, default=10)

    args = parser.parse_args(argv)

    runner = BenchmarkRunner(
        task=args.task,
        description=args.description,
        model=args.model,
        temperature=args.temperature,
        runs=args.runs,
    )
    report = runner.run()

    # stdout summary of averaged *raw* metrics (unchanged behaviour)
    print("\n" + "=" * 80)
    print(f"SUMMARY FOR TASK: {args.task}")
    print("=" * 80)
    print("\nAVERAGE RAW METRICS ACROSS RUNS")
    print("-" * 40)
    for k, v in report["avg"].items():
        print(f"{k:.<35} {v:.4f}")


if __name__ == "__main__":
    main()