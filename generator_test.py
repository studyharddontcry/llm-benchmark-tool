from benchmark_tool.generator import CodeGenerator

# Initialize the generator with your preferred model
generator = CodeGenerator(model_name="qwen2.5-coder:3b")

# Test with different function descriptions
examples = [
    "Function that calculates the factorial of a number",
    "Function that reverses a string without using built-in reverse functions",
    "Function that checks if a number is prime"
]

for desc in examples:
    generated_code = generator.generate(desc)
    print(generated_code)
    print("=" * 60)
    
# Porovnni s lidskym kodem - stejnym zpusobem jako kod LLM (stejné formatování)

"""
Metriky: jak je dobře formatován (prazdné řádky, atd).

Ve výsledcích: porovnat stejný model s různým počtem parametrů. !A porovnat různé modely.!

Pro+c vzvijiím nástroj: zkoušel jsem WEB UI -> je to velmi komplikované, proto třeba vyvíjet nástroj na automatickou analýzu kódu.

Předpokladaný závěr: zaleží na velikosti sítě, kvalita templatu, atd.  

DeepSearch od OpenAI (do diskuze).
"""
