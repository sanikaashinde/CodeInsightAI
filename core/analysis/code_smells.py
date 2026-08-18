import ast


class CodeSmellDetector:

    def analyze(self, code: str):

        smells = []

        try:
            tree = ast.parse(code)

        except SyntaxError:

            return [

                {
                    "type": "Syntax Error",
                    "severity": "Critical",
                    "message": "Unable to analyze file."
                }

            ]

        for node in ast.walk(tree):

            # =====================================
            # Functions
            # =====================================

            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):

                # Long Function

                if len(node.body) > 50:

                    smells.append({

                        "type": "Long Function",

                        "severity": "High",

                        "function": node.name,

                        "line": node.lineno,

                        "message": "Function contains more than 50 statements."

                    })

                # Too Many Parameters

                if len(node.args.args) > 5:

                    smells.append({

                        "type": "Too Many Parameters",

                        "severity": "Medium",

                        "function": node.name,

                        "line": node.lineno,

                        "message": "Function has more than 5 parameters."

                    })

                # Missing Docstring

                if ast.get_docstring(node) is None:

                    smells.append({

                        "type": "Missing Docstring",

                        "severity": "Low",

                        "function": node.name,

                        "line": node.lineno,

                        "message": "Function has no documentation."

                    })

                # Deep Nesting

                depth = self._max_depth(node)

                if depth > 4:

                    smells.append({

                        "type": "Deep Nesting",

                        "severity": "Medium",

                        "function": node.name,

                        "line": node.lineno,

                        "message": f"Nesting depth = {depth}"

                    })

            # =====================================
            # Classes
            # =====================================

            elif isinstance(node, ast.ClassDef):

                methods = [

                    n

                    for n in node.body

                    if isinstance(

                        n,

                        (ast.FunctionDef, ast.AsyncFunctionDef)

                    )

                ]

                if len(methods) > 20:

                    smells.append({

                        "type": "Large Class",

                        "severity": "High",

                        "class": node.name,

                        "line": node.lineno,

                        "message": "Class contains too many methods."

                    })

        return smells

    # ============================================
    # Calculate Nesting Depth
    # ============================================

    def _max_depth(self, node):

        depth = 0

        for child in ast.iter_child_nodes(node):

            if isinstance(

                child,

                (

                    ast.If,

                    ast.For,

                    ast.While,

                    ast.With,

                    ast.Try,

                    ast.Match,

                ),

            ):

                depth = max(

                    depth,

                    1 + self._max_depth(child)

                )

            else:

                depth = max(

                    depth,

                    self._max_depth(child)

                )

        return depth


def detect_code_smells(code: str):

    return CodeSmellDetector().analyze(code)

def detect_code_smells(code):
    """
    Backward-compatible wrapper.
    """
    return CodeSmellDetector().analyze(code)