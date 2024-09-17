import re

def parse_basic_response(response):
    """
    Parse a basic input-output response.

    Args:
        response (str): The raw response from the language model.

    Returns:
        tuple: A tuple containing nodes, edges, and the final answer.
    """
    # For basic responses, we simply return a static structure
    return [("Input", "Neutral"), ("Output", "Neutral")], [("Input", "Output")], response

def parse_cot_response(response):
    """
    Parse a Chain of Thought (CoT) response.

    Args:
        response (str): The raw response from the language model.

    Returns:
        tuple: A tuple containing nodes, edges, and the final answer.
    """
    # Extract steps from the response
    steps = re.findall(r'Step (\d+):\s*(.+?)\s*\((.+?)\)', response, re.DOTALL)

    # Extract final answer
    final_answer = re.search(r'Final Answer:\s*(.+?)$', response, re.DOTALL)
    final_answer = final_answer.group(1).strip() if final_answer else "No final answer provided."

    # Construct nodes list
    nodes = [("Input", "Neutral")] + [(f"Step {id}", content, sentiment) for id, content, sentiment in steps] + [("Output", "Neutral")]

    # Construct edges list
    edges = [("Input", "Step 1")]
    for i in range(1, len(steps)):
        edges.append((f"Step {i}", f"Step {i+1}"))
    edges.append((f"Step {len(steps)}", "Output"))

    return nodes, edges, final_answer

def parse_got_response(response):
    """
    Parse a Graph of Thoughts (GoT) response.

    Args:
        response (str): The raw response from the language model.

    Returns:
        tuple: A tuple containing nodes, edges, and the final answer.
    """
    # Extract nodes, edges, deleted nodes, and final answer from the response
    nodes = re.findall(r'Node (\d+):\s*(.+?)\s*\((.+?)\)', response, re.DOTALL)
    edges = re.findall(r'Edge:\s*Node (\d+) -> Node (\d+)', response)
    deleted_nodes = re.findall(r'Deleted Node:\s*(.+)', response, re.DOTALL)
    final_answer = re.search(r'Final Answer:\s*(.+?)$', response, re.DOTALL)
    final_answer = final_answer.group(1).strip() if final_answer else "No final answer provided."

    # Construct nodes list, excluding deleted nodes
    nodes = [("Input", "Neutral")] + [(f"Node {id}", content, sentiment) for id, content, sentiment in nodes if f"Node {id}" not in deleted_nodes] + [("Output", "Neutral")]

    # Construct edges list, excluding edges connected to deleted nodes
    edges = [("Input", "Node 1")] + [(f"Node {src}", f"Node {dst}") for src, dst in edges if f"Node {src}" not in deleted_nodes and f"Node {dst}" not in deleted_nodes]

    # Ensure the last node is connected to the output
    if nodes[-2][0] != "Output":
        edges.append((nodes[-2][0], "Output"))

    return nodes, edges, final_answer
