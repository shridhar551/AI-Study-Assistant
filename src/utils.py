"""
Utility functions for AI Study Assistant
"""

import os
from typing import Optional


def read_file(file_path: str) -> Optional[str]:
    """
    Read content from a text file.
    
    Args:
        file_path: Path to the file to read
        
    Returns:
        File content as string, or None if file doesn't exist
    """
    try:
        if not os.path.exists(file_path):
            print(f"Error: File '{file_path}' not found.")
            return None
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return None


def save_output(content: str, output_path: str, file_type: str = "txt") -> bool:
    """
    Save generated content to a file.
    
    Args:
        content: Content to save
        output_path: Path where to save the file
        file_type: File extension (txt, md, json, etc.)
        
    Returns:
        True if successful, False otherwise
    """
    try:
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ Output saved to: {output_path}")
        return True
    except Exception as e:
        print(f"Error saving file: {e}")
        return False


def truncate_text(text: str, max_length: int = 2000) -> str:
    """
    Truncate text to maximum length for API calls.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        Truncated text
    """
    if len(text) > max_length:
        return text[:max_length] + f"\n... (truncated, total length: {len(text)} chars)"
    return text


def format_output(title: str, content: str) -> str:
    """
    Format output with a title and content.
    
    Args:
        title: Title of the output
        content: Main content
        
    Returns:
        Formatted output string
    """
    separator = "=" * 60
    return f"\n{separator}\n{title}\n{separator}\n\n{content}\n"


def validate_api_key(api_key: Optional[str]) -> bool:
    """
    Validate if API key is present.
    
    Args:
        api_key: API key to validate
        
    Returns:
        True if API key is valid, False otherwise
    """
    if not api_key or api_key.strip() == "":
        print("Error: API key not configured. Please set your API key.")
        return False
    return True
