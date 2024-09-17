import streamlit as st
from llm_setup import get_llm, basic_chain, cot_chain, got_chain
from parsing import parse_basic_response, parse_cot_response, parse_got_response
from visualization import create_graph_visualization, create_force_directed_layout
import networkx as nx

# Set up the Streamlit page configuration
st.set_page_config(layout="wide")

st.title("x-of-Thought: Advanced Reasoning Visualization")

# User input area
user_question = st.text_area("Question", "")

def resubmit():
    """Force resubmission of the form."""
    st.session_state.submit = True

# Reasoning type selection
reasoning_type = st.selectbox(
    "Select Reasoning Type",
    ["Basic Input-Output", "Chain of Thought", "Graph of Thoughts"],
    on_change=resubmit,
)

philosophy = 1  # Default value for Basic Input-Output

# Generate response when the button is clicked or form is submitted
if st.session_state.get("submit", False) or st.button("Generate Response"):
    st.session_state.submit = False
    with st.spinner("Generating response..."):
        try:
            # Generate response based on selected reasoning type
            if reasoning_type == "Basic Input-Output":
                response = basic_chain.run(question=user_question)
                nodes, edges, final_answer = parse_basic_response(response)
            elif reasoning_type == "Chain of Thought":
                response = cot_chain.run(question=user_question)
                nodes, edges, final_answer = parse_cot_response(response)
            else:  # Graph of Thoughts
                response = got_chain.run(question=user_question)
                nodes, edges, final_answer = parse_got_response(response)

            # Store results in session state
            st.session_state["nodes"] = nodes
            st.session_state["edges"] = edges
            st.session_state["final_answer"] = final_answer
            st.session_state["reasoning_type"] = reasoning_type
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Display results if available
if "nodes" in st.session_state:
    reasoning_type = st.session_state["reasoning_type"]
    nodes = st.session_state["nodes"]
    edges = st.session_state["edges"]
    final_answer = st.session_state["final_answer"]

    # Create graph
    G = nx.DiGraph()
    for node in nodes:
        if len(node) == 2:  # Input/Output nodes
            G.add_node(node[0], description=node[0], sentiment=node[1])
        else:
            G.add_node(node[0], description=node[1], sentiment=node[2])
    G.add_edges_from(edges)

    # Generate layout and visualization
    pos = create_force_directed_layout(G)
    fig = create_graph_visualization(G, pos, reasoning_type)

    # Display visualization and details
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("Visualization")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Final Answer")
        st.text_area("final_answer", value=final_answer, height=150, disabled=True)

        st.subheader("Node Details")
        selected_node = st.selectbox("Select a node:", list(G.nodes()))
        if selected_node:
            node_content = G.nodes[selected_node]["description"]
            st.text_area(f"node_{selected_node}", value=node_content, height=150, disabled=True)

# Sidebar information
st.sidebar.header("About")
st.sidebar.info(
    "This app demonstrates advanced reasoning visualization techniques including Basic Input-Output, Chain of Thought, and Graph of Thoughts using Llama 3.1 (8b-instruct-q4_K_M) via Ollama."
)
