# ConceptNet Robotic Control System

[![Project Demo](https://img.youtube.com/vi/guN1oEn4dWE/0.jpg)](https://www.youtube.com/watch?v=guN1oEn4dWE)

## Project Overview

The ConceptNet Robotic Control System is an innovative integration of semantic knowledge representation and robotic control. This system leverages ConceptNet, a semantic network of common-sense knowledge, to enhance robotic decision-making and object manipulation in various environments. The project demonstrates how semantic understanding can improve robotic adaptability and context-aware behavior.

## Key Features

- **Semantic Knowledge Integration**: Utilizes ConceptNet to understand relationships between objects and their contexts
- **Context-Aware Object Classification**: Intelligent classification of objects based on their semantic relationships and environmental context
- **Adaptive Path Finding**: Advanced algorithms for finding optimal paths between objects and locations
- **Focus-Based Context Selection**: Dynamic adjustment of robot focus based on environmental context
- **Multi-Modal Similarity Analysis**: Integration of various semantic similarity measures (Word2Vec, GloVe, FastText)
- **Interactive Context Management**: User-friendly interface for specifying and managing environmental contexts

## Installation Instructions

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ConceptNet.git
cd ConceptNet
```

2. Create and activate a virtual environment:
```bash
python -m venv concept_env
source concept_env/bin/activate  # On Windows: concept_env\Scripts\activate
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

4. Set up ConceptNet API:
- Install ConceptNet API server
- Configure the API endpoint in the configuration files

## Usage Examples

### Basic Object Context Classification
```python
from src.core.conceptnet_classifier import get_object_context

# Load your knowledge graph data
with open('paths_modified_6.json', 'r') as file:
    data = json.load(file)

# Get context for an object
context = get_object_context(data, "apple")
print(context)
```

### Advanced Context-Aware Classification
```python
from src.core.conceptnet_classifier_specified_tasked_toppaths import get_object_context

# Specify focus contexts
focus_contexts = ["kitchen", "dining_room"]

# Get context with focus
context = get_object_context(data, "apple", focus_contexts=focus_contexts)
print(context)
```

## Technologies Used

- **Python**: Core programming language
- **ConceptNet**: Semantic knowledge base
- **Word2Vec/GloVe/FastText**: Semantic similarity models
- **ROS (Robot Operating System)**: Robotic control framework
- **JSON**: Data storage and exchange format
- **NumPy/Pandas**: Data processing and analysis

## Project Structure

```
ConceptNet/
├── src/
│   ├── core/                 # Core implementation files
│   ├── data/                 # Data files and knowledge graphs
│   ├── scripts/              # Utility scripts
│   └── tests/                # Test files
├── docs/                     # Documentation
├── Papers and Thesis/        # Research papers and thesis
└── requirements.txt          # Project dependencies
```

## Contact Information

For questions or collaboration opportunities, please contact:
- Email: [Your Email]
- GitHub: [Your GitHub Profile]

## License

This project is licensed under the MIT License - see the LICENSE file for details.
