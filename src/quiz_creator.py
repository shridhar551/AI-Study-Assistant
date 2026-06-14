"""
Quiz Creator Module - Create quiz questions from study material
"""

from typing import Optional, List, Dict
from .utils import read_file, validate_api_key
import os
import json


class QuizCreator:
    """Create quiz questions from study material using AI."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Quiz Creator.
        
        Args:
            api_key: Optional API key for AI service
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
    
    def create_questions(
        self,
        file_path: str,
        num_questions: int = 5,
        question_type: str = "multiple_choice"
    ) -> Optional[List[Dict]]:
        """
        Create quiz questions from study material.
        
        Args:
            file_path: Path to the study material file
            num_questions: Number of questions to generate
            question_type: Type of questions - 'multiple_choice', 'short_answer', 'true_false'
            
        Returns:
            List of quiz questions, or None if failed
        """
        # Read the file
        content = read_file(file_path)
        if not content:
            return None
        
        # Validate API key
        if not validate_api_key(self.api_key):
            return self._create_questions_local(content, num_questions, question_type)
        
        # Use AI to create questions
        return self._create_questions_ai(content, num_questions, question_type)
    
    def _create_questions_local(
        self,
        content: str,
        num_questions: int,
        question_type: str
    ) -> List[Dict]:
        """
        Create questions locally without AI (basic implementation).
        
        Args:
            content: Study material
            num_questions: Number of questions
            question_type: Type of questions
            
        Returns:
            Generated questions
        """
        print("⚠ Operating in local mode (no API key). Using basic question generation.\n")
        
        sentences = [s.strip() for s in content.split('.') if len(s.strip()) > 20]
        questions = []
        
        for i, sentence in enumerate(sentences[:num_questions]):
            if question_type == "true_false":
                questions.append({
                    "id": i + 1,
                    "type": "true_false",
                    "question": f"True or False: {sentence}?",
                    "correct_answer": "True"
                })
            elif question_type == "short_answer":
                questions.append({
                    "id": i + 1,
                    "type": "short_answer",
                    "question": f"Explain: {sentence}",
                    "answer_hint": "Based on the study material"
                })
            else:  # multiple_choice
                questions.append({
                    "id": i + 1,
                    "type": "multiple_choice",
                    "question": f"Which statement best describes: {sentence[:100]}?",
                    "options": ["Option A", "Option B", "Option C", "Option D"],
                    "correct_answer": "Option A"
                })
        
        return questions
    
    def _create_questions_ai(
        self,
        content: str,
        num_questions: int,
        question_type: str
    ) -> List[Dict]:
        """
        Create questions using AI service.
        
        Args:
            content: Study material
            num_questions: Number of questions
            question_type: Type of questions
            
        Returns:
            AI-generated questions
        """
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=self.api_key)
            
            type_description = {
                "multiple_choice": "multiple choice questions with 4 options each",
                "short_answer": "short answer questions",
                "true_false": "true/false questions"
            }
            
            prompt = f"""Generate {num_questions} {type_description.get(question_type, 'multiple choice')} 
from this study material:

{content[:1500]}

Format the response as JSON with the following structure for each question:
- id: question number
- type: question type
- question: the question text
- options: (for multiple choice) list of 4 options
- correct_answer: the correct answer
- explanation: brief explanation

Return ONLY valid JSON array."""
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert teacher creating fair and educational quiz questions."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            response_text = response.choices[0].message.content
            
            # Try to parse JSON response
            try:
                questions = json.loads(response_text)
                return questions if isinstance(questions, list) else [questions]
            except json.JSONDecodeError:
                # Fallback to local generation if JSON parsing fails
                return self._create_questions_local(content, num_questions, question_type)
        
        except Exception as e:
            print(f"Error generating questions with AI: {e}")
            return self._create_questions_local(content, num_questions, question_type)
    
    def format_quiz(self, questions: List[Dict]) -> str:
        """
        Format quiz questions for display.
        
        Args:
            questions: List of quiz questions
            
        Returns:
            Formatted quiz string
        """
        output = "QUIZ\n" + "=" * 60 + "\n\n"
        
        for q in questions:
            output += f"Question {q.get('id', '?')}: {q.get('question', '')}\n"
            
            if q.get('type') == 'multiple_choice' and 'options' in q:
                for i, opt in enumerate(q['options'], 1):
                    output += f"  {chr(64+i)}) {opt}\n"
            
            output += "\n"
        
        return output
    
    def display_quiz_with_answers(self, questions: List[Dict]) -> str:
        """
        Display quiz with answers and explanations.
        
        Args:
            questions: List of quiz questions
            
        Returns:
            Formatted quiz with answers
        """
        output = "QUIZ WITH ANSWERS\n" + "=" * 60 + "\n\n"
        
        for q in questions:
            output += f"Question {q.get('id', '?')}: {q.get('question', '')}\n"
            
            if q.get('type') == 'multiple_choice' and 'options' in q:
                for i, opt in enumerate(q['options'], 1):
                    output += f"  {chr(64+i)}) {opt}\n"
            
            output += f"\n✓ Answer: {q.get('correct_answer', 'N/A')}\n"
            
            if 'explanation' in q:
                output += f"Explanation: {q['explanation']}\n"
            
            output += "\n"
        
        return output
