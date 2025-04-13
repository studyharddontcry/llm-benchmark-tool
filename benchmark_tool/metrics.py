# metrics.py

import logging
import subprocess
import tempfile
import os
import re
from typing import Dict, Any, Optional

# Additional libraries for style and complexity:
# pip install pycodestyle radon
# For memory measurement, we use tracemalloc built into Python 3.8+

import pycodestyle
import json
import time
import tracemalloc
import ast


class CodeMetrics:
    """
    A class to compute quality metrics for a generated Python code snippet.

    Metrics:
      1) success: 1 if tests passed, 0 otherwise
      2) pep8_violations: number of style violations (pycodestyle)
      3) avg_cyclomatic_complexity: average cyclomatic complexity across all functions (radon)
      4) memory_usage_kb: approximate memory usage (peak) in kilobytes
      5) generation_time_s: time spent generating code (passed from generator)
      6) runtime_time_s: time to import & call at least one function
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        if not self.logger.handlers:
            logging.basicConfig(level=logging.INFO)

    def evaluate(self, 
                 code_str: str, 
                 test_success: bool, 
                 generation_time: float) -> Dict[str, Any]:
        """
        Evaluates the given code string on multiple metrics.

        Args:
            code_str (str): The Python code to evaluate.
            test_success (bool): True if the code passed tests, False otherwise.
            generation_time (float): Time taken to generate the code (seconds).

        Returns:
            Dict[str, Any]: A dictionary containing metric names and their values.
        """
        if not code_str.strip():
            raise ValueError("Cannot evaluate metrics on empty code.")

        metrics = {
            # 1) Pass/fail from tests:
            "success": 1 if test_success else 0,
            # 2) Style violations:
            "pep8_violations": 0,
            # 3) Complexity:
            "avg_cyclomatic_complexity": 0.0,
            # 4) Memory usage (in KB):
            "memory_usage_kb": 0.0,
            # 5) Code generation time (seconds):
            "generation_time_s": generation_time,
            # 6) Code runtime time (seconds):
            "runtime_time_s": 0.0
        }

        # Measure style violations (PEP 8):
        metrics["pep8_violations"] = self._check_pep8(code_str)

        # Measure cyclomatic complexity (radon):
        metrics["avg_cyclomatic_complexity"] = self._check_cyclomatic_complexity(code_str)

        # Attempt to measure memory usage and runtime by calling the code in-process:
        mem_usage_kb, runtime_s = self._measure_memory_and_runtime(code_str)
        metrics["memory_usage_kb"] = mem_usage_kb
        metrics["runtime_time_s"] = runtime_s

        return metrics

    def _check_pep8(self, code_str: str) -> int:
        """
        Runs pycodestyle on the code string and returns the number of style violations.
        If pycodestyle is not installed or there's an error, returns -1 as fallback.
        """
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode="w") as tmpfile:
            tmpfile.write(code_str)
            tmpfile_path = tmpfile.name

        try:
            style_guide = pycodestyle.StyleGuide(quiet=True)
            report = style_guide.check_files([tmpfile_path])
            violations = report.total_errors  # Number of PEP 8 violations
            return violations
        except Exception as e:
            self.logger.error("Error running pycodestyle: %s", e)
            return -1
        finally:
            if os.path.exists(tmpfile_path):
                os.remove(tmpfile_path)

    def _check_cyclomatic_complexity(self, code_str: str) -> float:
        """
        Runs radon to compute cyclomatic complexity of all functions in the code.
        Returns the average complexity across all blocks.
        If radon isn't installed or there's an error, returns -1.
        """
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode="w") as tmpfile:
            tmpfile.write(code_str)
            tmpfile_path = tmpfile.name

        try:
            # radon cc <file> -s -j
            cmd = ["radon", "cc", tmpfile_path, "-s", "-j"]
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()

            data = json.loads(stdout)
            blocks = data.get(tmpfile_path, [])
            if not blocks:
                return 0.0

            complexities = [b.get("complexity", 0) for b in blocks]
            avg_complexity = sum(complexities) / len(complexities)
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

    def _measure_memory_and_runtime(self, code_str: str) -> (float, float):
        """
        Loads the generated code in-process, tries to call the first function found,
        and measures approximate memory usage (peak) plus execution time.

        Returns:
            memory_usage_kb (float): approximate peak memory usage in KB
            runtime_s (float): time in seconds to import and call the function

        If no function is found, we just import the code for measurement.
        """
        # Find a function name (similar logic to what's in tester.py)
        func_name = self._find_function_name(code_str)

        # We'll run in the current Python process using `exec`.
        # We'll measure with tracemalloc for memory, and time.time() for runtime.
        # This is a rough estimate – a more accurate approach would spawn a separate process.

        # Setup environment in which we will exec() the code
        local_vars = {}
        start_time = 0.0
        end_time = 0.0
        peak_mem_kb = 0.0

        tracemalloc.start()
        start_snapshot = tracemalloc.take_snapshot()
        start_time = time.time()

        try:
            # 1) Exec the code in local_vars
            exec(code_str, local_vars, local_vars)

            # 2) If we found a function, call it
            if func_name and func_name in local_vars:
                func = local_vars[func_name]
                # Call with no arguments if possible
                # (in real scenarios, pass some defaults if function requires arguments)
                try:
                    func()
                except TypeError:
                    pass  # If the function needs arguments, skip

        except Exception as e:
            self.logger.warning("Runtime error while measuring: %s", e)
        finally:
            end_time = time.time()
            end_snapshot = tracemalloc.take_snapshot()
            tracemalloc.stop()

        # Compute time
        runtime_s = end_time - start_time

        # Compute memory usage difference in KB
        stats = end_snapshot.compare_to(start_snapshot, 'lineno')
        # peak usage is not directly provided by default; we look at total allocated vs. freed
        # For a simple measure, let's sum up net allocations
        total_alloc = sum(stat.size_diff for stat in stats)
        # Convert bytes to KB
        peak_mem_kb = float(total_alloc) / 1024.0

        return (peak_mem_kb, runtime_s)

    def _find_function_name(self, code_str: str) -> Optional[str]:
        """
        Parses the code string to find the first function definition.
        Returns the name of the first function, or None if none found.
        """
        pattern = r'^\s*def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\('
        match = re.search(pattern, code_str, flags=re.MULTILINE)
        if match:
            return match.group(1)
        return None
