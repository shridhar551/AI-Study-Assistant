"""
AI Study Assistant - Main Application
Complete example of using the study assistant features
"""

import os
from pathlib import Path
from src import NoteGenerator, QuizCreator, Summarizer
from src.utils import save_output, format_output


def create_sample_study_material():
    """Create a sample study material file for demonstration."""
    sample_content = """
Photosynthesis Overview

Photosynthesis is the process by which plants, algae, and some bacteria convert light energy 
from the sun into chemical energy stored in glucose. This process is essential for life on Earth 
as it produces oxygen and forms the base of most food chains.

Key Components of Photosynthesis:

1. Light Reactions (Light-Dependent Reactions)
   - Occur in the thylakoid membrane of chloroplasts
   - Require light energy from the sun
   - Produce ATP and NADPH (energy carriers)
   - Release oxygen as a byproduct
   - Involve photosystem I and II
   - Water molecules are split to provide electrons

2. Calvin Cycle (Light-Independent Reactions)
   - Occur in the stroma of chloroplasts
   - Do not directly require light
   - Use ATP and NADPH from light reactions
   - Convert CO2 into glucose
   - Include three main phases: carbon fixation, reduction, and regeneration

3. Chloroplast Structure
   - Double membrane envelope
   - Thylakoids: stacked membrane structures containing chlorophyll
   - Grana: stacks of thylakoids
   - Stroma: fluid-filled space surrounding thylakoids
   - Contains its own DNA and ribosomes

Factors Affecting Photosynthesis:
- Light intensity: More light increases photosynthesis rate until saturation point
- Carbon dioxide concentration: Essential substrate for the Calvin cycle
- Temperature: Affects enzyme activity in photosynthesis
- Water availability: Required as electron source and for osmotic balance
- Chlorophyll concentration: Absorbs light energy

Historical Development:
- 1600s: Jan Baptista van Helmont demonstrated that plants gain mass from water
- 1771: Joseph Priestley discovered oxygen production
- 1842: Julius Robert von Mayer proposed that plants convert light to chemical energy
- 1961: Melvin Calvin elucidated the Calvin cycle mechanism

Importance of Photosynthesis:
- Produces approximately 99% of Earth's oxygen
- Forms the base of most food chains and food webs
- Removes carbon dioxide from the atmosphere
- Provides renewable energy source potential
- Sustains global biological productivity

Applications and Future Research:
- Artificial photosynthesis technology
- Crop improvement and genetic engineering
- Biofuel production
- Climate change mitigation strategies
- Solar energy harvesting inspiration
"""
    
    os.makedirs("sample_data", exist_ok=True)
    with open("sample_data/sample_study_material.txt", "w") as f:
        f.write(sample_content)
    
    print("✓ Sample study material created: sample_data/sample_study_material.txt\n")


def main():
    """Main application demonstrating all features."""
    
    print("\n" + "="*60)
    print("AI STUDY ASSISTANT 📚")
    print("="*60 + "\n")
    
    # Create sample data
    create_sample_study_material()
    material_path = "sample_data/sample_study_material.txt"
    
    # Initialize components
    note_gen = NoteGenerator()
    quiz_creator = QuizCreator()
    summarizer = Summarizer()
    
    print("Features Available:")
    print("1. Generate Study Notes")
    print("2. Create Quiz Questions")
    print("3. Summarize Material")
    print("4. All Features (Complete Processing)")
    print("\n" + "-"*60 + "\n")
    
    # Feature 1: Generate Notes
    print("📝 GENERATING NOTES...\n")
    notes_detailed = note_gen.generate_notes(material_path, style="detailed")
    if notes_detailed:
        print(notes_detailed)
        save_output(notes_detailed, "output/notes_detailed.txt")
    
    notes_outline = note_gen.generate_notes(material_path, style="outline")
    if notes_outline:
        print(notes_outline)
        save_output(notes_outline, "output/notes_outline.txt")
    
    # Extract key concepts
    print("\n📌 KEY CONCEPTS EXTRACTION\n")
    concepts = note_gen.extract_key_concepts(material_path)
    if concepts:
        print("Top Key Concepts:")
        for i, concept in enumerate(concepts[:10], 1):
            print(f"  {i}. {concept}")
        save_output("\n".join(concepts), "output/key_concepts.txt")
    
    # Feature 2: Create Quiz
    print("\n\n❓ CREATING QUIZ QUESTIONS...\n")
    questions = quiz_creator.create_questions(
        material_path,
        num_questions=5,
        question_type="multiple_choice"
    )
    
    if questions:
        # Display quiz without answers
        quiz_display = quiz_creator.format_quiz(questions)
        print(quiz_display)
        save_output(quiz_display, "output/quiz.txt")
        
        # Save quiz with answers
        quiz_with_answers = quiz_creator.display_quiz_with_answers(questions)
        save_output(quiz_with_answers, "output/quiz_with_answers.txt")
    
    # Feature 3: Summarize Material
    print("\n📖 SUMMARIZING MATERIAL...\n")
    summary_short = summarizer.summarize(material_path, summary_length="short")
    if summary_short:
        print("SHORT SUMMARY:")
        print(summary_short)
        save_output(summary_short, "output/summary_short.txt")
    
    summary_medium = summarizer.summarize(material_path, summary_length="medium")
    if summary_medium:
        print("\n\nMEDIUM SUMMARY:")
        print(summary_medium)
        save_output(summary_medium, "output/summary_medium.txt")
    
    # Bullet summary
    bullet_summary = summarizer.create_bullet_summary(material_path)
    if bullet_summary:
        print("\n\nBULLET SUMMARY:")
        print(bullet_summary)
        save_output(bullet_summary, "output/bullet_summary.txt")
    
    # Final message
    print("\n" + "="*60)
    print("✓ Processing Complete!")
    print("  Check the 'output' folder for all generated materials")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
