from langchain.prompts import PromptTemplate

# Basic prompt for simple question-answer interactions
basic_prompt = PromptTemplate(
    input_variables=["question"],
    template="Question: {question}\n\nAnswer:",
)

# Chain of Thought (CoT) prompt for structured reasoning
cot_prompt = PromptTemplate(
    input_variables=["question"],
    template="""
Provide a detailed chain of thought to answer the following question:

Question: {question}

Respond with steps in this format only, exactly as shown:
Step 1: [Brief description] (Positive/Negative/Neutral)
Step 2: [Brief description] (Positive/Negative/Neutral)
...
Final Answer: [Concise answer based on the steps within 150 words. Do not refer the graph.]

You may include branching thoughts or remove steps that seem irrelevant as you progress.
""",
)

# Graph of Thoughts (GoT) prompt for complex reasoning with nodes and edges
got_prompt = PromptTemplate(
    input_variables=["question"],
    template="""
Create a detailed graph of thought to answer the following question.
Question: {question}

Respond in this format, exactly as shown:
Node 1: [Brief description] (Positive/Negative/Neutral)
Node 2: [Brief description] (Positive/Negative/Neutral)
...
Edge: Node X -> Node Y
Edge: Node A -> Node B
...
Deleted Node: [Node number and brief reason for deletion]
...
Final Answer: [Concise answer based on the steps within 150 words. Do not refer the graph.]

Create a complex graph with multiple connections and potential branches. You may delete nodes that become irrelevant as the graph develops.
""",
)
