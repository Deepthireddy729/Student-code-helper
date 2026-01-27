"""Code Explainer Tool - Explains existing code line by line."""

from langchain.tools import tool


@tool
def code_explainer_tool(code: str) -> str:
    """Explains what a piece of code does, breaking it down line by line or section by section.
    
    Use this tool when a student has code they don't understand and wants it explained.
    This tool helps students learn by understanding existing code.
    
    Args:
        code: The code snippet that needs to be explained
        
    Returns:
        A detailed explanation of what the code does
    """
    
    explanation_prompt = f"""
Please explain this code in detail:

{code}

Provide:
1. An overview of what the code does
2. Line-by-line or section-by-section breakdown
3. Explanation of any key concepts or patterns used
4. Potential improvements or best practices
5. Common pitfalls to avoid

Make the explanation clear and educational for a student learning to code!
"""
    
    return explanation_prompt
