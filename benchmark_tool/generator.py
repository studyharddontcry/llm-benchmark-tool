import time
import logging
from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_ollama import OllamaLLM
from langchain_core.runnables import RunnablePassthrough

import ast, textwrap, re

def _strip_trailing_prose(code: str) -> str:
    """
    Return the longest prefix of `code` that parses with `ast.parse`.
    Drop any trailing narrative text that would break syntax.
    """
    lines = code.splitlines()
    for i in range(len(lines), 0, -1):
        candidate = "\n".join(lines[:i])
        try:
            ast.parse(candidate)
            return candidate.strip()
        except SyntaxError:
            continue
    # if nothing parses, return original
    return code.strip()


class CodeGenerator:
    """
    A class to generate Python functions using a language model (with a fixed system prompt).

    Attributes:
        llm (OllamaLLM): The language model used for code generation.
        chain (Callable): The chain of operations for generating code.
    """

    def __init__(self, model_name: str = "qwen2.5-coder:3b", temperature: float = 0.3):
        """
        Initializes the CodeGenerator with a language model and a chat-based prompt template.

        Args:
            model_name (str): The name of the language model to use.
            temperature (float): The temperature for the language model.
        """

        default_system_message = """
You are an AI coding assistant. You must follow these rules at all costs:
1. Output only valid, standalone Python code, NO Markdown as "```python".
2. Output only function starting with 'def' and its body, NO test cases.
3. Absolutely no lines starting with '#' (in-line comments).
4. Put all explanations in the function Google-style docstring.
5. Include necessary imports if needed.
ANY violation makes the output INVALID.
"""

        default_user_prompt = """
Write a complete, standalone Python function based on the description below:
{function_description}

Constraints:
- The code must be fully executable.
- NO comments or explanations outside the docstring.
- No anything else, just the function code, NO test cases.
"""

        # Create ChatPromptTemplate from system and user messages
        system_message_prompt = SystemMessagePromptTemplate.from_template(default_system_message)
        user_message_prompt = HumanMessagePromptTemplate.from_template(default_user_prompt)
        chat_prompt_template = ChatPromptTemplate.from_messages([
            system_message_prompt,
            user_message_prompt
        ])

        # Set up the language model
        self.llm = OllamaLLM(
            model=model_name,
            temperature=temperature,
            top_k=20,
            # stop=["<END_OF_CODE>"]
        )

        # Build the chain (maps {function_description} → chat_prompt → LLM)
        self.chain = (
            {"function_description": RunnablePassthrough()}
            | chat_prompt_template
            | self.llm
        )

        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def generate(self, description: str) -> tuple[str, float]:
        """
        Generates a Python function based on the given description.

        Args:
            description (str): A description of the function to generate.

        Returns:
            str: The generated Python function.

        Raises:
            ValueError: If the description is empty or invalid.
            Exception: If the chain invocation fails.
        """
        if not description.strip():
            raise ValueError("Function description cannot be empty.")

        self.logger.info("Generating code for description: %s", description)

        start_time = time.time()
        try:
            result = self.chain.invoke(description)
        except Exception as e:
            self.logger.error("Code generation failed: %s", str(e))
            raise
        finally:
            end_time = time.time()
            self.generation_time = end_time - start_time
            self.logger.info("Code generation took %.4f seconds", self.generation_time)
            
        # Strip any markdown code block syntax
        result = result.strip().replace('```python', '').replace('```', '')

        # Remove inline comments while preserving docstrings
        lines = result.split('\n')
        cleaned_lines = []
        in_docstring = False
        docstring_delim = '"""'

        for line in lines:
            stripped = line.strip()
            
            # Toggle docstring state
            if stripped.startswith(docstring_delim) or stripped.endswith(docstring_delim):
                in_docstring = not in_docstring
                cleaned_lines.append(line)
                continue
                
            # Keep lines that aren't comments and are either in docstring or have content
            if in_docstring or (not stripped.startswith('#') and stripped):
                cleaned_lines.append(line)

        result = '\n'.join(cleaned_lines).strip()
        
        # code_lines = []
        # for line in result.splitlines():
        #     if line.strip().startswith("import ") or line.strip().startswith("def ") or line.startswith(" "):
        #         code_lines.append(line)
        #     else:
        #         # stop at the first narrative line
        #         break
        # result = "\n".join(code_lines).strip()
        
        result = _strip_trailing_prose(result)
    
        self.logger.info("Code generated successfully.\nGenerated code:\n%s", result)
        return result, self.generation_time
