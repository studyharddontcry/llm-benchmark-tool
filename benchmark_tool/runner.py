import argparse
import sys
from generator import CodeGenerator
from tester import CodeTester
from metrics import CodeMetrics

def main():
    parser = argparse.ArgumentParser(
        description="End-to-end runner for generating, testing, and evaluating code from an LLM."
    )
    parser.add_argument(
        "--model",
        type=str,
        default="qwen2.5-coder:3b",
        help="Name of the model to use (default: qwen2.5-coder:3b)."
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.3,
        help="Temperature for the model (default: 0.3)."
    )
    parser.add_argument(
        "--description",
        type=str,
        required=True,
        help="A short description of the function or code you want to generate."
    )
    args = parser.parse_args()

    # 1) Instantiate the Generator with user-specified or default model
    generator = CodeGenerator(model_name=args.model, temperature=args.temperature)

    # 2) Generate code based on the user's description and capture time
    code_str, generation_time = generator.generate(args.description)

    # 3) Test the generated code
    tester = CodeTester()
    success, test_output = tester.test_code(code_str)
    test_success = success  # True/False

    # 4) Compute metrics (e.g., pass/fail, style, complexity) and pass generation_time to evaluate
    metrics_calculator = CodeMetrics()
    results = metrics_calculator.evaluate(code_str, test_success, generation_time)

    # 5) Print output
    print("=== Generated Code ===")
    print(code_str)
    print("\n=== Test Output ===")
    print(test_output)
    print("\n=== Metrics ===")
    for key, val in results.items():
        print(f"{key}: {val}")

    # Optional: Return non-zero exit code if tests failed
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
