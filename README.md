# AI Study Assistant 📚

An intelligent Python application that helps you study more effectively by processing text files and generating study materials using AI.

## Features

- **📝 Note Generation**: Extract and generate organized notes from text files
- **❓ Quiz Creation**: Automatically create quiz questions from study material
- **📖 Material Summarization**: Generate concise summaries of lengthy study content

## Requirements

- Python 3.8+
- See `requirements.txt` for dependencies

## Installation

1. Clone or download this project
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Project Structure

```
AI-Study-Assistant/
├── src/
│   ├── __init__.py
│   ├── note_generator.py      # Generate notes from text
│   ├── quiz_creator.py         # Create quiz questions
│   ├── summarizer.py           # Summarize study material
│   └── utils.py                # Helper functions
├── sample_data/
│   └── sample_study_material.txt
├── main.py                     # Main application
├── requirements.txt
└── README.md
```

## Usage

### Generate Notes
```python
from src.note_generator import NoteGenerator

generator = NoteGenerator()
notes = generator.generate_notes("path/to/text_file.txt")
```

### Create Quiz Questions
```python
from src.quiz_creator import QuizCreator

quiz = QuizCreator()
questions = quiz.create_questions("study_material.txt", num_questions=10)
```

### Summarize Material
```python
from src.summarizer import Summarizer

summarizer = Summarizer()
summary = summarizer.summarize("path/to/text_file.txt")
```

### Run the Complete Application
```bash
python main.py
```

## Configuration

Edit `config.py` to customize:
- AI model settings
- Output formats
- Question difficulty levels
- Summary length

## Examples

See `main.py` for complete usage examples.

## License

MIT License

## Contributing

Contributions are welcome! Feel free to submit issues and enhancement requests.
