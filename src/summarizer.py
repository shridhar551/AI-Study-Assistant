"""
Summarizer Module - Summarize study material
"""

from typing import Optional
from .utils import read_file, validate_api_key
import os


class Summarizer:
    """Generate summaries of study material using AI."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Summarizer.
        
        Args:
            api_key: Optional API key for AI service
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
    
    def summarize(
        self,
        file_path: str,
        summary_length: str = "medium"
    ) -> Optional[str]:
        """
        Generate a summary of study material.
        
        Args:
            file_path: Path to the study material file
            summary_length: Length of summary - 'short', 'medium', or 'long'
            
        Returns:
            Summary as string, or None if failed
        """
        # Read the file
        content = read_file(file_path)
        if not content:
            return None
        
        # Validate API key
        if not validate_api_key(self.api_key):
            return self._summarize_local(content, summary_length)
        
        # Use AI to summarize
        return self._summarize_ai(content, summary_length)
    
    def _summarize_local(self, content: str, summary_length: str) -> str:
        """
        Generate summary locally without AI (basic implementation).
        
        Args:
            content: Study material
            summary_length: Length of summary
            
        Returns:
            Generated summary
        """
        print("⚠ Operating in local mode (no API key). Using basic summarization.\n")
        
        # Extract first N sentences based on summary length
        length_map = {
            "short": 3,
            "medium": 6,
            "long": 10
        }
        
        num_sentences = length_map.get(summary_length, 5)
        
        sentences = [s.strip() for s in content.split('.') if len(s.strip()) > 10]
        selected_sentences = sentences[:num_sentences]
        
        summary = "SUMMARY\n" + "=" * 50 + "\n\n"
        summary += ". ".join(selected_sentences) + "."
        
        return summary
    
    def _summarize_ai(self, content: str, summary_length: str) -> str:
        """
        Generate summary using AI service.
        
        Args:
            content: Study material
            summary_length: Length of summary
            
        Returns:
            AI-generated summary
        """
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=self.api_key)
            
            length_instructions = {
                "short": "2-3 paragraphs",
                "medium": "3-4 paragraphs",
                "long": "5-6 paragraphs"
            }
            
            prompt = f"""Create a {summary_length} summary ({length_instructions.get(summary_length)}) of the following study material:

{content[:2000]}

The summary should:
- Be clear and concise
- Capture main concepts and key points
- Be suitable for quick review
- Include important details without being verbose"""
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert at creating clear, educational summaries of study material."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            print(f"Error generating summary with AI: {e}")
            return self._summarize_local(content, summary_length)
    
    def create_bullet_summary(self, file_path: str) -> Optional[str]:
        """
        Create a bullet-point summary of study material.
        
        Args:
            file_path: Path to the study material file
            
        Returns:
            Bullet-point summary
        """
        content = read_file(file_path)
        if not content:
            return None
        
        if not validate_api_key(self.api_key):
            return self._create_bullet_summary_local(content)
        
        return self._create_bullet_summary_ai(content)
    
    def _create_bullet_summary_local(self, content: str) -> str:
        """Create bullet summary locally."""
        lines = content.split('\n')
        summary = "BULLET SUMMARY\n" + "=" * 50 + "\n\n"
        
        for line in lines[:15]:
            line = line.strip()
            if line and len(line) > 10:
                summary += f"• {line}\n"
        
        return summary
    
    def _create_bullet_summary_ai(self, content: str) -> str:
        """Create bullet summary using AI."""
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=self.api_key)
            
            prompt = f"""Create a bullet-point summary of the key concepts from:

{content[:1500]}

Format as bullet points with main concepts and brief explanations."""
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You create clear bullet-point summaries of educational material."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            print(f"Error: {e}")
            return self._create_bullet_summary_local(content)
