"""Code Writer Tool - Generates code based on requirements."""

from langchain.tools import tool


@tool
def code_writer_tool(requirements: str) -> str:
    """Writes clean, well-commented code based on the student's requirements.
    
    Use this tool when a student needs help writing code or implementing a solution.
    The tool generates code with proper comments and best practices.
    
    Args:
        requirements: Description of what the code should do, including language preference if specified
        
    Returns:
        Well-structured, commented code that meets the requirements
    """
    
    code_prompt = f"""
Write code based on these requirements: {requirements}

Please provide:
1. Clean, readable code with proper formatting
2. Helpful comments explaining what each section does
3. Best practices for the language being used
4. A brief explanation of how to use the code

If the language isn't specified, use Python as the default.
Make sure the code is beginner-friendly and educational!
"""
    
    return code_prompt
