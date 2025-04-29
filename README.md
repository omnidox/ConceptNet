# Robo-CSK Organizer System

[![Project Demo](https://img.youtube.com/vi/guN1oEn4dWE/0.jpg)](https://www.youtube.com/watch?v=guN1oEn4dWE)

A sophisticated robotic system that combines computer vision, commonsense knowledge, and robotic manipulation to intelligently organize objects in various contexts.

## Project Overview

The Robo-CSK Organizer System is an advanced robotic platform that integrates:
- Real-time object detection and classification using DETIC
- Commonsense knowledge reasoning for context-aware decision making
- Precise robotic manipulation for object handling
- Multi-context understanding and adaptation

The system can intelligently identify, classify, and organize objects based on their semantic relationships and contextual relevance, making it particularly effective in environments like playrooms, offices, and kitchens.

## Key Features

### 1. Context-Aware Object Understanding
- Semantic relationship analysis using ConceptNet
- Multi-context support (playroom, kitchen, office, etc.)
- Weighted path analysis for decision making
- Focus-aware context adjustment

### 2. Advanced Computer Vision
- Real-time object detection using DETIC
- Support for multiple vocabularies (LVIS, COCO, custom)
- High-precision object classification
- Custom vocabulary support for specialized tasks

### 3. Intelligent Robotic Control
- Precise object manipulation
- Context-aware movement planning
- Real-time position adjustment
- Multi-degree-of-freedom control

### 4. Commonsense Knowledge Integration
- Knowledge graph construction and traversal
- Semantic relationship analysis
- Context-based path finding
- Weight and relevance scoring

## Installation Instructions

### Prerequisites
- Python 3.8+
- ROS (Robot Operating System)
- CUDA-capable GPU (recommended)
- MoveIt for robotic control

### Setup
1. Clone the repository:
```bash
git clone https://github.com/yourusername/robo-csk-organizer.git
cd robo-csk-organizer
```

2. Install dependencies:
```bash
cd robo_csk_organizer_system
pip install -r requirements.txt
```

3. Set up ROS environment:
```bash
source /opt/ros/<version>/setup.bash
```

4. Configure the system:
- Update `cog.yaml` with your specific settings
- Adjust `Rafael_setup.rviz` for your robot configuration

## Usage Examples

### Basic Object Organization
```bash
python Webcam_local_robo.py --config-file configs/Detic_LCOCOI21k_CLIP_SwinB_896b32_4x_ft4x_max-size.yaml --webcam 0 --vocabulary custom --custom_vocabulary toy,stuffed_animal,ball
```

### Context-Aware Organization
```bash
python demo6.py --context playroom --focus toys
```

## Technologies Used

### Core Technologies
- ROS (Robot Operating System)
- MoveIt for robotic control
- DETIC for object detection
- ConceptNet for commonsense knowledge
- PyTorch for deep learning

### Libraries and Frameworks
- Detectron2
- FiftyOne
- OpenCV
- NumPy
- Pandas

## Project Structure

```
.
├── robo_csk_organizer_system/     # Main robot implementation
│   ├── configs/                   # Configuration files
│   ├── datasets/                  # Dataset files
│   ├── detic/                     # DETIC implementation
│   └── ...                        # Implementation files
├── commonsense_builder/           # Commonsense components
│   ├── src/                       # Source code
│   ├── docs/                      # Documentation
│   └── data/                      # Data files
└── ...                            # Project files
```

## Contact Information

For questions, collaborations, or support, please contact:
- Email: [Your Email]
- GitHub: [Your GitHub Profile]

## License

This project is licensed under the MIT License - see the [LICENSE](robo_csk_organizer_system/LICENSE) file for details.

## Contributing

Please read [CONTRIBUTING.md](robo_csk_organizer_system/CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.
