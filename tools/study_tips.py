"""Study Tips Tool - Provides study strategies and tips."""

from langchain.tools import tool


@tool
def study_tips_tool(topic_or_subject: str) -> str:
    """Provides personalized study tips, strategies, and techniques for learning a specific topic or subject.
    
    Use this tool when a student asks for help with HOW to study, learn better, or
    improve their understanding of a subject.
    
    Args:
        topic_or_subject: The topic, subject, or skill the student wants study tips for
        
    Returns:
        Personalized study strategies and tips
    """
    
    tips_prompt = f"""
Provide study tips and strategies for learning: {topic_or_subject}

Include:
1. Effective study techniques specific to this subject
2. Common challenges students face and how to overcome them
3. Time management suggestions
4. Active learning strategies (practice problems, teaching others, etc.)
5. How to avoid common mistakes
6. Motivation and mindset tips

Make the advice practical, actionable, and encouraging!
"""
    
    return tips_prompt
