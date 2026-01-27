"""Resource Finder Tool - Suggests learning resources for topics."""

from langchain.tools import tool


@tool
def resource_finder_tool(topic: str) -> str:
    """Suggests high-quality learning resources (tutorials, documentation, courses, books) for a specific topic.
    
    Use this tool when a student wants to find additional materials to learn a topic
    or needs recommendations for learning resources.
    
    Args:
        topic: The topic or subject to find learning resources for
        
    Returns:
        A curated list of recommended learning resources
    """
    
    resources_prompt = f"""
Suggest high-quality learning resources for: {topic}

Recommend:
1. Official documentation or authoritative sources
2. Beginner-friendly tutorials or courses (free and paid)
3. YouTube channels or video series
4. Books (both beginner and advanced)
5. Practice platforms or interactive learning sites
6. Communities or forums for getting help

Organize by difficulty level (Beginner → Intermediate → Advanced) and include
brief descriptions of why each resource is valuable!
"""
    
    return resources_prompt
