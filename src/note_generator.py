"""
Note Generator Module - Generate organized notes from text files
"""

from typing import Optional, List
from .utils import read_file, validate_api_key
import os


class NoteGenerator:
    """Generate structured notes from study material using AI."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Note Generator.
        
        Args:
            api_key: Optional API key for AI service
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
    
    def generate_notes(self, file_path: str, style: str = "detailed") -> Optional[str]:
        """
        Generate organized notes from a text file.
        
        Args:
            file_path: Path to the study material file
            style: Note style - 'detailed', 'concise', or 'outline'
            
        Returns:
            Generated notes as string, or None if failed
        """
        # Read the file
        content = read_file(file_path)
        if not content:
            return None
        
        # Validate API key
        if not validate_api_key(self.api_key):
            return self._generate_notes_local(content, style)
        
        # Use AI to generate notes
        return self._generate_notes_ai(content, style)
    
    def _generate_notes_local(self, content: str, style: str) -> str:
        """
        Generate notes locally without AI (basic implementation).
        
        Args:
            content: Study material content
            style: Note style
            
        Returns:
            Generated notes
        """
        print("⚠ Operating in local mode (no API key). Using basic note extraction.\n")
        
        if style == "outline":
            return self._create_outline(content)
        elif style == "concise":
            return self._create_concise_notes(content)
        else:  # detailed
            return self._create_detailed_notes(content)
    
    def _create_outline(self, content: str) -> str:
        """Create an outline-style notes."""
        lines = content.split('\n')
        notes = "OUTLINE NOTES\n" + "=" * 50 + "\n\n"
        
        for i, line in enumerate(lines[:20]):  # Limit to first 20 lines
            line = line.strip()
            if line and len(line) > 10:
                notes += f"• {line}\n"
        
        return notes
    
    def _create_concise_notes(self, content: str) -> str:
        """Create concise notes."""
        sentences = [s.strip() for s in content.split('.') if len(s.strip()) > 20]
        notes = "CONCISE NOTES\n" + "=" * 50 + "\n\n"
        
        for sentence in sentences[:15]:  # Limit to 15 sentences
            notes += f"• {sentence}.\n"
        
        return notes
    
    def _create_detailed_notes(self, content: str) -> str:
        """Create detailed notes."""
        lines = content.split('\n')
        notes = "DETAILED NOTES\n" + "=" * 50 + "\n\n"
        
        # Group into sections
        section = "Main Content"
        notes += f"\n## {section}\n"
        
        for line in lines[:30]:
            line = line.strip()
            if line:
                notes += f"• {line}\n"
        
        return notes
    
    def _generate_notes_ai(self, content: str, style: str) -> str:
        """
        Generate notes using AI service.
        
        Args:
            content: Study material
            style: Note style
            
        Returns:
            AI-generated notes
        """
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=self.api_key)
            
            prompt = f"""Generate {style} study notes from the following material:

{content[:1500]}

Please create well-organized, easy-to-understand notes that capture the key concepts."""
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful study assistant that creates clear, organized notes."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating notes with AI: {e}")
            return self._generate_notes_local(content, style)
    
    def extract_key_concepts(self, file_path: str) -> Optional[List[str]]:
        """
        Extract key concepts from study material.
        
        Args:
            file_path: Path to the study material file
            
        Returns:
            List of key concepts
        """
        content = read_file(file_path)
        if not content:
            return None
        
        # Simple keyword extraction (can be enhanced with AI)
        words = content.lower().split()
        # Filter common words and short words
        concepts = [w for w in set(words) if len(w) > 5 and w.isalpha()]
        
        return sorted(concepts)[:20]  # Return top 20
