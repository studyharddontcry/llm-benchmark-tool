import logging
import subprocess
import tempfile
import os
from typing import Dict, Any

class CodeMetrics:
    """
    A class to compute basic quality metrics for a generated Python code snippet.
    
    Metrics:
      1) success: 1 if tests passed, 0 otherwise
      2) pep8_violations: number of style violations (pycodestyle)
      3) avg_cyclomatic_complexity: average cyclomatic complexity across all functions (radon)
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        if not self.logger.handlers:
            logging.basicConfig(level=logging.INFO)

    def evaluate(self, code_str: str, test_success: bool) -> Dict[str, Any]:
        """
        Evaluates the given code string on several metrics.

        Args:
            code_str (str): The Python code to evaluate.
            test_success (bool): True if the code passed tests, False otherwise.

        Returns:
            Dict[str, Any]: A dictionary containing metric names and their values, e.g.:
                {
                  "success": 1,
                  "pep8_violations": 2,
                  "avg_cyclomatic_complexity": 1.5
                }
        """
        if not code_str.strip():
            raise ValueError("Cannot evaluate metrics on empty code.")

        metrics = {
            "success": 1 if test_success else 0,
            "pep8_violations": 0,
            "avg_cyclomatic_complexity": 0.0
        }

        # 1) PEP 8 (pycodestyle) Violations
        metrics["pep8_violations"] = self._check_pep8(code_str)

        # 2) Cyclomatic Complexity (radon)
        metrics["avg_cyclomatic_complexity"] = self._check_cyclomatic_complexity(code_str)

        return metrics

    def _check_pep8(self, code_str: str) -> int:
        """
        Runs pycodestyle on the code string and returns the number of style violations.
        If pycodestyle is not installed or there's an error, returns -1 as fallback.

        Args:
            code_str (str): The Python code to check.

        Returns:
            int: The count of PEP 8 violations.
        """
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode="w") as tmpfile:
            tmpfile.write(code_str)
            tmpfile_path = tmpfile.name

        try:
            cmd = ["pycodestyle", tmpfile_path]
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()

            # Each line in stdout typically corresponds to one violation
            # e.g. "<file_path>:<line>:<column>: <error_code> <message>"
            if stdout.strip():
                violations = stdout.strip().splitlines()
                count_violations = len(violations)
                self.logger.debug("pycodestyle output:\n%s", stdout)
            else:
                count_violations = 0

            return count_violations

        except FileNotFoundError:
            # pycodestyle not installed or not found in PATH
            self.logger.error("pycodestyle not found. Please install it via `pip install pycodestyle`.")
            return -1
        except Exception as e:
            self.logger.error("Error running pycodestyle: %s", e)
            return -1
        finally:
            # Clean up temporary file
            if os.path.exists(tmpfile_path):
                os.remove(tmpfile_path)

    def _check_cyclomatic_complexity(self, code_str: str) -> float:
        """
        Runs radon to compute cyclomatic complexity of all functions in the code.
        Returns the average complexity across all blocks.
        If radon isn't installed or there's an error, returns -1.

        Args:
            code_str (str): The Python code to check.

        Returns:
            float: The average cyclomatic complexity. If no functions found, returns 0.0.
        """
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode="w") as tmpfile:
            tmpfile.write(code_str)
            tmpfile_path = tmpfile.name

        try:
            # radon cc <file> -s -j  => short output, JSON format
            cmd = ["radon", "cc", tmpfile_path, "-s", "-j"]
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()

            # radon returns JSON with structure:
            # {
            #   "<file_path>": [
            #       {
            #           "type": "function",
            #           "name": "<function_name>",
            #           "lineno": 10,
            #           "col_offset": 0,
            #           "endline": 15,
            #           "clojures": [],
            #           "complexity": 5
            #       },
            #       ...
            #   ]
            # }
            import json
            data = json.loads(stdout)

            # The key is the file path, value is a list of function/class blocks
            blocks = data.get(tmpfile_path, [])
            if not blocks:
                return 0.0

            complexities = [b.get("complexity", 0) for b in blocks]
            avg_complexity = sum(complexities) / len(complexities)

            self.logger.debug("Radon output:\n%s", stdout)
            return avg_complexity

        except FileNotFoundError:
            self.logger.error("radon not found. Please install it via `pip install radon`.")
            return -1
        except Exception as e:
            self.logger.error("Error running radon: %s", e)
            return -1
        finally:
            if os.path.exists(tmpfile_path):
                os.remove(tmpfile_path)
