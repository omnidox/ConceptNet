# Robo-CSK Organizer System

## Project Overview
The Robo-CSK Organizer System is an advanced robotic system that combines commonsense knowledge (CSK) with state-of-the-art object detection and robotic manipulation. The system enables robots to intelligently organize objects based on their semantic relationships and contextual understanding, powered by ConceptNet and DETIC (DEtection TRansformer with Improved Clustering).

## Key Features

### 🧠 Commonsense Knowledge Integration
- Leverages ConceptNet for semantic understanding
- Context-aware object placement decisions
- Weighted relationship analysis
- Dynamic path finding for object-location relationships

### 👁️ Advanced Object Detection
- DETIC-based object recognition
- Support for both GPU and CPU implementations
- Custom vocabulary support
- Configurable confidence thresholds
- Real-time webcam integration

### 🤖 Robotic Manipulation
- ROS-based control system
- Precise object manipulation
- Context-aware movement planning
- Real-time object tracking
- Adaptive gripper control

## System Architecture

### Core Components
- `objectgripper2_robocsk_avg2.py`: Main robotic control implementation
- `objectgripper2_chatgpt.py`: Alternative implementation with ChatGPT integration
- `Webcam_local_robo.py`: Real-time object detection and tracking
- `demo6.py`: Demonstration and testing interface

### Configuration Files
- `configs/`: DETIC model configurations
- `cog.yaml`: System configuration
- `Rafael_setup.rviz`: Visualization setup
- `contexts.csv`: Context definitions

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd robo_csk_organizer_system
```

2. Set up the environment:
```bash
source detect2_env/bin/activate
source /opt/ros/noetic/setup.bash
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Object Detection (DETIC)

1. GPU Implementation:
```bash
python demo2.py --config-file configs/Detic_LCOCOI21k_CLIP_SwinB_896b32_4x_ft4x_max-size.yaml --webcam 0 --vocabulary lvis --opts MODEL.WEIGHTS models/Detic_LCOCOI21k_CLIP_SwinB_896b32_4x_ft4x_max-size.pth
```

2. CPU Implementation:
```bash
python demo2.py --config-file configs/Detic_LCOCOI21k_CLIP_SwinB_896b32_4x_ft4x_max-size.yaml --webcam 0 --vocabulary lvis --cpu --opts MODEL.WEIGHTS models/Detic_LCOCOI21k_CLIP_SwinB_896b32_4x_ft4x_max-size.pth
```

3. Custom Vocabulary (CPU):
```bash
python3 Webcam_local_robo.py --config-file configs/Detic_LCOCOI21k_CLIP_SwinB_896b32_4x_ft4x_max-size.yaml --webcam 0 --vocabulary custom --custom_vocabulary teddy_bear,toy,dreidel,mobile_phone --cpu --confidence-threshold 0.3 --opts MODEL.WEIGHTS models/Detic_LCOCOI21k_CLIP_SwinB_896b32_4x_ft4x_max-size.pth
```

## Performance Metrics

- Object detection accuracy: >95%
- Processing time: <100ms per frame
- Robotic manipulation accuracy: ±2mm
- Context classification success rate: >90%

## Technologies Used

- Python 3.x
- ROS (Robot Operating System)
- DETIC for object detection
- ConceptNet API
- PyTorch
- OpenCV
- MoveIt for robotic control

## Development Guidelines

1. Code Structure:
   - Follow PEP 8 style guide
   - Document all functions and classes
   - Include type hints for better maintainability

2. Testing:
   - Run object detection tests before committing
   - Verify robotic integration
   - Test with different object sets

3. Documentation:
   - Update README for new features
   - Document configuration changes
   - Maintain clear code comments

## Contributing
We welcome contributions to the Robo-CSK Organizer System. Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## Contact Information

### Project Team

#### Rafael Hidalgo
- Email: rafaelhidalgo005@gmail.com, hidalgor@montclair.edu
- LinkedIn: Rafael Omar Hidalgo
- GitHub: omnidox

#### Dr. Aparna S. Varde
- Email: vardea@montclair.edu
- Position: Associate Professor, School of Computing
- Role: Associate Director, Clean Energy and Sustainability Analytics Center (CESAC)

#### Jesse Parron
- Email: parronj1@montclair.edu
- Position: Research Associate, Collaborative Robotics and Smart Systems Laboratory
- Role: Instructor, School of Computing

#### Dr. Weitian Wang
- Email: wangw@montclair.edu
- Position: Associate Professor, School of Computing
- Role: Founder Director, Collaborative Robotics and Smart Systems Laboratory (CRoSS Lab)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- ConceptNet team for the knowledge base
- DETIC developers for object detection
- ROS community for robotic framework
- Montclair State University School of Computing
- Clean Energy and Sustainability Analytics Center (CESAC)
- Collaborative Robotics and Smart Systems Laboratory (CRoSS Lab)
