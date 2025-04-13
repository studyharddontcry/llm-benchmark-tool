from generator import CodeGenerator
from tester import CodeTester
from metrics import CodeMetrics

def main():
    generator = CodeGenerator()
    tester = CodeTester()
    metrics_calculator = CodeMetrics()

    # Generate code
    code_str = generator.generate("Generate a function that returns square of a number minus it's root.")

    # Test code
    success, output = tester.test_code(code_str)
    test_success = success  # True/False

    # Evaluate metrics
    results = metrics_calculator.evaluate(code_str, test_success)
    print("Metrics:", results)
    # e.g. {'success': 1, 'pep8_violations': 2, 'avg_cyclomatic_complexity': 1.0}

if __name__ == "__main__":
    main()
