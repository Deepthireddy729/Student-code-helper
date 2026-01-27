"""Math Solver Tool - Solves mathematical problems with step-by-step explanations."""

from langchain.tools import tool


@tool
def math_solver_tool(problem: str) -> str:
    """Solves mathematical problems with detailed step-by-step explanations.
    
    Use this tool when a student needs help solving a math problem. This tool not only
    provides the answer but teaches the process of solving it.
    
    Args:
        problem: The mathematical problem to solve
        
    Returns:
        A detailed solution with step-by-step explanation
    """
    
    solution_prompt = f"""
Please solve this mathematical problem: {problem}

Provide:
1. The problem statement clearly restated
2. Step-by-step solution with explanations for each step
3. The final answer clearly highlighted
4. Tips or tricks related to this type of problem
5. Similar concepts the student should understand

Focus on teaching the student HOW to solve it, not just giving the answer!
"""
    
    return solution_prompt
