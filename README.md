# Trash-can-Can

工创赛垃圾分类项目

## 项目简介

Trash-can-Can 是一个基于 YOLO 模型的垃圾分类项目，旨在通过计算机视觉技术实现垃圾分类。该项目可以在 PC 和树莓派上运行，并且可以将检测结果发送到 Arduino 进行处理。

## 目录结构

```
.
├── .gitignore
├── detect_pc.py
├── detect_pi.py
├── detect_record.py
├── images/
│   ├── trash/
│   └── trash640/
├── LICENSE
├── models/
│   ├── trash_1.pt
│   ├── trash_320_1.pt
│   ├── trashcan.pt
│   └── yolov11s.pt
├── README.md
└── temp.py
```

## 安装与运行

### 环境依赖

- Python 3.x
- OpenCV
- Ultralytics YOLO

### 安装依赖

```sh
pip install -r requirements.txt
```

### 运行检测脚本

#### 在 PC 上运行

```sh
python detect_pc.py
```

#### 在树莓派上运行

```sh
python detect_pi.py
```

#### 运行并记录视频

```sh
python detect_record.py
```

## 文件说明

- `detect_pc.py`：在 PC 上运行的垃圾分类检测脚本。
- `detect_pi.py`：在树莓派上运行的垃圾分类检测脚本。
- `detect_record.py`：运行垃圾分类检测并记录视频的脚本。
- `models/`：存放训练好的 YOLO 模型文件。
- `images/`：存放测试图片的文件夹。
- `LICENSE`：项目的许可证文件。
- `README.md`：项目的说明文件。

## 数据集

```
datasets/
├── trashcan/
│   ├── train/    # 训练数据，包括图片和对应的txt标签
│   │   ├── image1.png
│   │   ├── image1.txt
│   │   ├── image2.png
│   │   ├── image2.txt
│   │   └── ...
│   ├── valid/    # 验证数据
│   │   ├── image1.png
│   │   ├── image1.txt
│   │   ├── image2.png
│   │   ├── image2.txt
│   │   └── ...
│   ├── mydata_kaggle.yaml   # Kaggle数据集配置文件
│   └── mydata_pc.yaml       # PC数据集配置文件
```

## 模型文件

- `models/trashcan.pt`：320尺寸，含蔬菜，建议使用。
- `models/trash_1.pt`：640尺寸，不含蔬菜。
- `models/trash_320_1.pt`：320尺寸，不含蔬菜.
- `models/yolov11s.pt`：YOLO 官方模型文件。

## 许可证

本项目采用 [Apache License 2.0](LICENSE) 许可证。(我也不知道是什么东西哈哈哈)

## 致谢

感谢给我做结构的卫思哲，给我做电控的陈祥瑞，给我做显示屏的卢松呈，还有**金主** 夏小水老师~，感谢我的“师傅”侯沅江学长，感谢同样赛道的贺一凡，周成龙，贾瑞通。希望能进国赛！🚀