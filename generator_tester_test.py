# runner.py - 1st version of the code

from benchmark_tool.generator import CodeGenerator
from benchmark_tool.tester import CodeTester

def main():
    generator = CodeGenerator()
    tester = CodeTester()

    # 1. Generate code
    code = generator.generate("Generate a function that returns square of a number minus it's root.")

    # 2. Test code
    success, output = tester.test_code(code)

    # 3. Print results
    print("Test success:", success)
    print("Pytest Output:\n", output)

if __name__ == "__main__":
    main()
