# Trash-can-Can

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/)
[![YOLO11](https://img.shields.io/badge/YOLO-11-green)](https://github.com/ultralytics/ultralytics)

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
│   ├── origin_img/   # Original images
│   ├── json_labels/  # Labelme JSON labels
│   └── yolo_labels/  # YOLO format labels
├── datasets/         # Training datasets
│   ├── train/        # Training set
│   └── valid/        # Validation set
└── process_data/     # Utils to process custom data
    └── box/          # Bounding box conversion tools
```

## 🎯 Data Processing Guide

Follow these steps to process your custom dataset:

1. **Prepare Original Images**
   - Place your original images in `images/origin_img/`

2. **Label Images**
   - Use Labelme or Label-studio to annotate images
   - Open images from `images/origin_img/`
   - Save JSON annotation files

3. **Clean Labels**
   ```bash
   python clear_not_labeled_img.py
   ```
   This removes JSON files for unlabeled images

4. **Organize Labels**
   - Move all JSON label files to `images/json_labels/`

5. **Convert to YOLO Format**
   ```bash
   python process_data/box/labelme2yolo.py
   ```
   This converts JSON labels to YOLO format in `images/yolo_labels/`

6. **Prepare Training Data**
   - Copy all files from `images/origin_img/` and `images/yolo_labels/` to `datasets/train/`

7. **Split Dataset**
   ```bash
   python divide_train_valid.py
   ```
   This automatically splits data into train/valid sets

8. **Data Augmentation**
   ```bash
   python augment_yolo.py
   ```
   This performs data augmentation on the training set

9. **Package for Training**
   - Ensure `mydata_kaggle.yaml` is properly configured
   - Compress the dataset using Bandizip
   - Upload to Kaggle for training

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

![Dataset Visualization](assets/images/dataset_visualize.png)

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

偷偷加了一句话，嘿嘿！