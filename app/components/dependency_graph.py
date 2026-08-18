import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

from core.analysis.dependency_graph import DependencyGraph


def show_dependency_graph(project_folder):

    analyzer = DependencyGraph()

    result = analyzer.build(project_folder)

    graph = result["graph"]

    st.subheader("📦 Dependency Graph")

    if graph.number_of_nodes() == 0:

        st.info("No dependencies found.")

        return

    c1, c2, c3 = st.columns(3)

    c1.metric("Modules", result["modules"])

    c2.metric("Libraries", len(result["libraries"]))

    c3.metric("Connections", result["edges"])

    fig, ax = plt.subplots(figsize=(10, 8))

    pos = nx.spring_layout(graph, seed=42)

    nx.draw_networkx(
        graph,
        pos,
        ax=ax,
        with_labels=True,
        node_size=1200,
        font_size=8,
        arrows=True,
    )

    st.pyplot(fig)

    st.subheader("Top Imported Libraries")

    st.dataframe(
        analyzer.top_dependencies(result),
        use_container_width=True,
        hide_index=True,
    )

    cycles = analyzer.circular_dependencies(result)

    if cycles:

        st.warning("Circular Dependencies Detected")

        st.write(cycles)

    else:

        st.success("No Circular Dependencies")