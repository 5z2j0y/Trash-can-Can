# Trash-can-Can

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/)
[![YOLOv8](https://img.shields.io/badge/YOLO-v8-green)](https://github.com/ultralytics/ultralytics)

AI-powered garbage classification system utilizing computer vision technology, designed to run on both PC and Raspberry Pi platforms.

## ✨ Features

- Real-time garbage classification using YOLOv8
- Cross-platform support (PC and Raspberry Pi)
- Arduino integration for hardware control
- Video recording capabilities
- Multiple pre-trained models for different scenarios

## 🚀 Quick Start

### Prerequisites

- Eazy to run on CPU (for PC version)
- Raspberry Pi 4 (for Pi version)
- Arduino board (optional)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Trash-can-Can.git
cd Trash-can-Can
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Usage

#### PC Version
```bash
python detect_pc.py [--model models/trashcan.pt] [--source 0]
```

#### Raspberry Pi Version
```bash
python detect_pi.py [--model models/trashcan.pt] [--source 0]
```

#### Record Detection
```bash
python detect_record.py [--output output.mp4]
```

## 📁 Project Structure

```
.
├── detect_pc.py      # PC detection script
├── detect_pi.py      # Raspberry Pi detection script
├── detect_record.py  # Video recording script
├── models/           # Pre-trained models
├── images/           # Test images
├── datasets/         # Training datasets
└── process_data      # Utils to process custom data
```

## 🤖 Models

| Model Name | Size | Description | Best For |
|------------|------|-------------|----------|
| trashcan.pt | 320x320 | Includes vegetables | General use |
| trashcan_640.pt | 640x640 | Without vegetables | High accuracy |


## 📊 Dataset

Our dataset is organized as follows:

```
datasets/
├── train/
├── valid/
└── mydata_kaggle.yaml
```

Configuration files:
- `mydata_kaggle.yaml`: Kaggle training configuration

## 🛠️ Development

Want to contribute? Great! I'm currently looking for contributors to help with the following:
- Enhance robustness against various lighting conditions.
- It's funny but serious to classify a broken China piece from a white radish bar.


## 📝 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Ultralytics](https://github.com/ultralytics/ultralytics) for YOLO
- [Kaggle](https://www.kaggle.com) for GPU resources
- Special thanks to the hardware implementation team

## 📧 Contact

For questions and support, please open an issue or contact the maintainers.
