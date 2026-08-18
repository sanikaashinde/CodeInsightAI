import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

from core.analysis.call_graph import FunctionCallGraph


def show_call_graph(project_folder):

    analyzer = FunctionCallGraph()

    graph = analyzer.build(project_folder)

    summary = analyzer.summary(graph)

    st.subheader("📞 Function Call Graph")

    if graph.number_of_nodes() == 0:
        st.info("No functions detected.")
        return

    c1, c2, c3 = st.columns(3)

    c1.metric("Functions", summary["functions"])
    c2.metric("Calls", summary["calls"])
    c3.metric("Recursive", summary["recursive_functions"])

    fig, ax = plt.subplots(figsize=(12, 9))

    pos = nx.spring_layout(graph, seed=42)

    nx.draw_networkx(
        graph,
        pos,
        ax=ax,
        node_size=1200,
        font_size=8,
        arrows=True,
        with_labels=True,
    )

    st.pyplot(fig)

    st.subheader("🔥 Most Connected Functions")

    st.dataframe(
        analyzer.top_functions(graph),
        hide_index=True,
        use_container_width=True,
    )

    isolated = analyzer.isolated_functions(graph)

    if isolated:
        st.subheader("📌 Isolated Functions")
        st.write(isolated)

    recursive = analyzer.recursive_functions(graph)

    if recursive:
        st.warning("Recursive Functions Detected")
        st.write(recursive)
    else:
        st.success("No Recursive Functions")