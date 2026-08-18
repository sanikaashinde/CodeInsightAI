import ast
from pathlib import Path


class SecurityAnalyzer:

    def analyze(self, filepath):

        filepath = Path(filepath)

        try:

            source = filepath.read_text(
                encoding="utf-8",
                errors="ignore"
            )

            tree = ast.parse(source)

        except Exception:

            return {
                "score": 100,
                "issues": []
            }

        issues = []

        # =====================================================
        # Dangerous Functions
        # =====================================================

        dangerous_functions = {
            "eval": "Critical",
            "exec": "Critical",
            "compile": "High",
            "__import__": "High",
            "input": "Low",
        }

        dangerous_imports = {
            "pickle",
            "marshal",
            "subprocess",
        }

        weak_hashes = {
            "md5",
            "sha1",
        }

        secret_keywords = {

            "password",
            "passwd",
            "secret",
            "token",
            "apikey",
            "api_key",
            "access_key",
            "private_key",

        }

        # =====================================================
        # AST Scan
        # =====================================================

        for node in ast.walk(tree):

            # --------------------------------------------
            # Imports
            # --------------------------------------------

            if isinstance(node, ast.Import):

                for alias in node.names:

                    if alias.name in dangerous_imports:

                        issues.append({

                            "type": "Dangerous Import",

                            "severity": "Medium",

                            "line": node.lineno,

                            "message": alias.name

                        })

            elif isinstance(node, ast.ImportFrom):

                if node.module in dangerous_imports:

                    issues.append({

                        "type": "Dangerous Import",

                        "severity": "Medium",

                        "line": node.lineno,

                        "message": node.module

                    })

            # --------------------------------------------
            # Function Calls
            # --------------------------------------------

            elif isinstance(node, ast.Call):

                if isinstance(node.func, ast.Name):

                    name = node.func.id

                    if name in dangerous_functions:

                        issues.append({

                            "type": "Dangerous Function",

                            "severity": dangerous_functions[name],

                            "line": node.lineno,

                            "message": f"{name}() detected"

                        })

                elif isinstance(node.func, ast.Attribute):

                    # os.system()

                    if (

                        isinstance(node.func.value, ast.Name)

                        and node.func.value.id == "os"

                        and node.func.attr == "system"

                    ):

                        issues.append({

                            "type": "OS Command",

                            "severity": "Critical",

                            "line": node.lineno,

                            "message": "os.system() detected"

                        })

                    # subprocess.*

                    if (

                        isinstance(node.func.value, ast.Name)

                        and node.func.value.id == "subprocess"

                    ):

                        issues.append({

                            "type": "Subprocess",

                            "severity": "High",

                            "line": node.lineno,

                            "message": f"subprocess.{node.func.attr}()"

                        })

                    # hashlib.md5 / sha1

                    if (

                        isinstance(node.func.value, ast.Name)

                        and node.func.value.id == "hashlib"

                        and node.func.attr in weak_hashes

                    ):

                        issues.append({

                            "type": "Weak Hash",

                            "severity": "Medium",

                            "line": node.lineno,

                            "message": node.func.attr

                        })

                    # random.random()

                    if (

                        isinstance(node.func.value, ast.Name)

                        and node.func.value.id == "random"

                    ):

                        issues.append({

                            "type": "Insecure Random",

                            "severity": "Low",

                            "line": node.lineno,

                            "message": node.func.attr

                        })

            # --------------------------------------------
            # Hardcoded Secrets
            # --------------------------------------------

            elif isinstance(node, ast.Assign):

                for target in node.targets:

                    if isinstance(target, ast.Name):

                        name = target.id.lower()

                        if any(k in name for k in secret_keywords):

                            issues.append({

                                "type": "Hardcoded Secret",

                                "severity": "Critical",

                                "line": node.lineno,

                                "message": target.id

                            })

        # =====================================================
        # Pickle Usage
        # =====================================================

        if "pickle.loads" in source:

            issues.append({

                "type": "Unsafe Deserialization",

                "severity": "Critical",

                "line": "-",

                "message": "pickle.loads() detected"

            })

        # =====================================================
        # Score
        # =====================================================

        score = 100

        penalty = {

            "Critical": 20,

            "High": 10,

            "Medium": 5,

            "Low": 2,

        }

        for issue in issues:

            score -= penalty.get(

                issue["severity"],

                2

            )

        score = max(score, 0)

        return {

            "score": score,

            "issues": issues

        }