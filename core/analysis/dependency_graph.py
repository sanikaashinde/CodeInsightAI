from pathlib import Path
import ast
import networkx as nx


class DependencyGraph:

    def build(self, project_folder):

        project_folder = Path(project_folder)

        graph = nx.DiGraph()

        module_dependencies = {}
        external_modules = set()

        for file in project_folder.rglob("*.py"):

            if "__pycache__" in file.parts:
                continue

            module_name = file.stem

            graph.add_node(
                module_name,
                type="module"
            )

            module_dependencies[module_name] = []

            try:

                source = file.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )

                tree = ast.parse(source)

            except Exception:

                continue

            # =====================================
            # Imports
            # =====================================

            for node in ast.walk(tree):

                if isinstance(node, ast.Import):

                    for alias in node.names:

                        imported = alias.name.split(".")[0]

                        module_dependencies[module_name].append(imported)

                        external_modules.add(imported)

                        graph.add_node(
                            imported,
                            type="library"
                        )

                        graph.add_edge(
                            module_name,
                            imported,
                            relation="import"
                        )

                elif isinstance(node, ast.ImportFrom):

                    if node.module:

                        imported = node.module.split(".")[0]

                        module_dependencies[module_name].append(imported)

                        external_modules.add(imported)

                        graph.add_node(
                            imported,
                            type="library"
                        )

                        graph.add_edge(
                            module_name,
                            imported,
                            relation="from-import"
                        )

        return {

            "graph": graph,

            "nodes": graph.number_of_nodes(),

            "edges": graph.number_of_edges(),

            "modules": len(module_dependencies),

            "libraries": sorted(external_modules),

            "dependencies": module_dependencies

        }

    # ==========================================
    # Top Imported Libraries
    # ==========================================

    def top_dependencies(self, dependency_result):

        counter = {}

        for imports in dependency_result["dependencies"].values():

            for lib in imports:

                counter[lib] = counter.get(lib, 0) + 1

        return sorted(

            counter.items(),

            key=lambda x: x[1],

            reverse=True

        )

    # ==========================================
    # Circular Dependency Detection
    # ==========================================

    def circular_dependencies(self, dependency_result):

        graph = dependency_result["graph"]

        try:

            return list(
                nx.simple_cycles(graph)
            )

        except Exception:

            return []

    # ==========================================
    # Project Statistics
    # ==========================================

    def summary(self, dependency_result):

        return {

            "Modules":
                dependency_result["modules"],

            "Libraries":
                len(
                    dependency_result["libraries"]
                ),

            "Connections":
                dependency_result["edges"],

            "Graph Nodes":
                dependency_result["nodes"]

        }