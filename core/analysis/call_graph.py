import ast
from pathlib import Path
import networkx as nx


class FunctionCallGraph:

    def build(self, project_folder):

        project_folder = Path(project_folder)

        graph = nx.DiGraph()

        for file in project_folder.rglob("*.py"):

            try:

                source = file.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )

                tree = ast.parse(source)

                visitor = _CallVisitor(
                    graph,
                    file.relative_to(project_folder).as_posix()
                )

                visitor.visit(tree)

            except Exception:
                continue

        return graph

    # ==================================

    def summary(self, graph):

        return {

            "functions": graph.number_of_nodes(),

            "calls": graph.number_of_edges(),

            "recursive_functions": len(
                self.recursive_functions(graph)
            ),

        }

    # ==================================

    def top_functions(self, graph, limit=10):

        ranking = []

        for node in graph.nodes():

            ranking.append({

                "Function": node,

                "Fan In": graph.in_degree(node),

                "Fan Out": graph.out_degree(node),

                "Total Connections": graph.degree(node),

                "File": graph.nodes[node].get("file", ""),

            })

        ranking.sort(

            key=lambda x: x["Total Connections"],

            reverse=True,

        )

        return ranking[:limit]

    # ==================================

    def recursive_functions(self, graph):

        recursive = []

        for node in graph.nodes():

            if graph.has_edge(node, node):

                recursive.append(node)

        return recursive

    # ==================================

    def isolated_functions(self, graph):

        isolated = []

        for node in graph.nodes():

            if graph.degree(node) == 0:

                isolated.append(node)

        return isolated
    
class _CallVisitor(ast.NodeVisitor):

    def __init__(self, graph, filename):

        self.graph = graph
        self.filename = filename
        self.current_function = None

    # ---------------------------------

    def visit_FunctionDef(self, node):

        previous = self.current_function

        self.current_function = node.name

        self.graph.add_node(

            node.name,

            file=self.filename,

            line=node.lineno,

            async_function=False,

        )

        self.generic_visit(node)

        self.current_function = previous

    # ---------------------------------

    def visit_AsyncFunctionDef(self, node):

        previous = self.current_function

        self.current_function = node.name

        self.graph.add_node(

            node.name,

            file=self.filename,

            line=node.lineno,

            async_function=True,

        )

        self.generic_visit(node)

        self.current_function = previous

    # ---------------------------------

    def visit_Call(self, node):

        if self.current_function is None:

            self.generic_visit(node)

            return

        called = None

        if isinstance(node.func, ast.Name):

            called = node.func.id

        elif isinstance(node.func, ast.Attribute):

            called = node.func.attr

        if called:

            if not self.graph.has_node(called):

                self.graph.add_node(

                    called,

                    external=True,

                )

            self.graph.add_edge(

                self.current_function,

                called,

            )

        self.generic_visit(node)