"""Concept Explainer Tool - Explains complex topics in simple terms."""

from langchain.tools import tool


@tool
def concept_explainer_tool(concept: str) -> str:
    """Explains a complex concept in simple, easy-to-understand language with examples and analogies.
    
    Use this tool when a student asks to understand or learn about a topic, concept, or idea.
    This tool breaks down complex topics into digestible explanations.
    
    Args:
        concept: The concept or topic the student wants to understand
        
    Returns:
        A clear, simple explanation with examples and analogies
    """
    
    # This is a structured prompt that the LLM will use to explain the concept
    explanation_prompt = f"""
Please explain the concept of "{concept}" in a way that's easy for a student to understand.

Include:
1. A simple definition
2. Why it's important or useful
3. A real-world analogy or example
4. Common misconceptions (if any)
5. How it relates to other concepts

Make it engaging and easy to follow!
"""
    
    return explanation_prompt
