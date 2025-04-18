import argparse
import sys
from typing import List, Dict, Any
from generator import CodeGenerator
from tester import CodeTester
from metrics import CodeMetrics
from tqdm import tqdm

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
    parser.add_argument(
        "--runs",
        type=int,
        default=10,
        help="Number of code generations to run (default: 10)"
    )
    args = parser.parse_args()

    generator = CodeGenerator(model_name=args.model, temperature=args.temperature)
    tester = CodeTester()
    metrics_calculator = CodeMetrics()
    
    all_metrics: List[Dict[str, Any]] = []
    all_codes: List[str] = []
    all_test_outputs: List[str] = []
    
    print(f"Running {args.runs} generations for: {args.description}\n")
    print("=" * 80)  # Initial separator
    
    # Run multiple generations
    for i in tqdm(range(args.runs), desc="Generating and testing code"):
        print(f"\nGeneration {i+1}/{args.runs}:")
        
        # Generate and test code
        code_str, generation_time = generator.generate(args.description)
        success, test_output = tester.test_code(code_str)
        
        # Calculate metrics
        results = metrics_calculator.evaluate(code_str, success, generation_time)
        
        # Store results
        all_metrics.append(results)
        all_codes.append(code_str)
        all_test_outputs.append(test_output)
        
        # Print individual results
        print(f"Success: {success}")
        print("Individual metrics:", results)
        print("_" * 80)  # Separator between generations
    
    # Calculate and print averages
    avg_metrics = metrics_calculator.average_metrics(all_metrics)
    
    print("\n" + "=" * 80)
    print(f"\nSUMMARY FOR: {args.description}")
    print("=" * 80)
    print("\nAVERAGE METRICS ACROSS ALL RUNS:")
    print("-" * 40)
    for key, val in avg_metrics.items():
        print(f"{key:.<30} {val:.4f}")

if __name__ == "__main__":
    main()
