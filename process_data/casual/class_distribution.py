import os
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from collections import Counter
from tqdm import tqdm

# ====== 配置部分 - 在此处修改路径 ======
# 标签文件夹路径
LABELS_DIR = r"images\yolo_labels"
# 类别名称文件路径
NAMES_FILE = r"trash.names"
# 输出图像文件名（如果不需要保存，可以设置为None）
OUTPUT_FILE = None
# ======================================

def load_class_names(names_file):
    """Load class names from a file."""
    with open(names_file, 'r') as f:
        class_names = [line.strip() for line in f.readlines() if line.strip()]
    return class_names

def analyze_class_distribution(labels_dir, class_names):
    """Analyze the class distribution in YOLO format labels."""
    labels_path = Path(labels_dir)
    class_counts = Counter()
    
    # 获取所有txt文件
    txt_files = list(labels_path.glob('*.txt'))
    
    # 使用tqdm添加进度条
    for txt_file in tqdm(txt_files, desc="Processing label files", unit="file"):
        with open(txt_file, 'r') as f:
            for line in f:
                if line.strip():
                    # YOLO format: <class_id> <x_center> <y_center> <width> <height>
                    class_id = int(line.strip().split()[0])
                    if class_id < len(class_names):
                        class_counts[class_id] += 1
    
    return class_counts, len(txt_files)

def plot_distribution(class_counts, class_names):
    """Plot the class distribution using matplotlib."""
    # Prepare data for plotting
    classes = []
    counts = []
    
    for class_id in range(len(class_names)):
        classes.append(class_names[class_id])
        counts.append(class_counts[class_id])
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Create bars with a color gradient
    colors = plt.cm.viridis(np.linspace(0, 0.9, len(classes)))
    bars = ax.bar(classes, counts, color=colors, edgecolor='black', alpha=0.8)
    
    # Add values on top of bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{int(height)}', ha='center', va='bottom', fontweight='bold')
    
    # Customize plot
    ax.set_xlabel('Class Names', fontsize=12, fontweight='bold')
    ax.set_ylabel('Number of Objects', fontsize=12, fontweight='bold')
    ax.set_title('Distribution of Classes in Dataset', fontsize=16, fontweight='bold')
    
    # Rotate x-labels for better readability
    plt.xticks(rotation=45, ha='right')
    
    # Add grid for better readability
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Add a horizontal line for average
    if counts:
        avg = sum(counts) / len(counts)
        ax.axhline(y=avg, color='r', linestyle='--', alpha=0.7)
        ax.text(0, avg + 1, f'Average: {avg:.1f}', color='r', fontweight='bold')
    
    # Tight layout to ensure labels are visible
    plt.tight_layout()
    
    return fig

# 直接执行代码，不需要main函数
print(f"Analyzing class distribution in directory: {LABELS_DIR}")

# 加载类别名称
class_names = load_class_names(NAMES_FILE)
print(f"Loaded {len(class_names)} class names: {', '.join(class_names)}")

# 分析类别分布
class_counts, total_files = analyze_class_distribution(LABELS_DIR, class_names)
print(f"\nProcessed {total_files} label files.")

print("\nClass distribution:")
for class_id in range(len(class_names)):
    count = class_counts[class_id]
    print(f"  {class_names[class_id]}: {count}")

# 计算总数和百分比
total_objects = sum(class_counts.values())
print(f"\nTotal objects: {total_objects}")
print(f"Average objects per file: {total_objects/total_files:.2f}" if total_files > 0 else "No files processed")
print("\nClass percentages:")
for class_id in range(len(class_names)):
    count = class_counts[class_id]
    percentage = (count / total_objects * 100) if total_objects > 0 else 0
    print(f"  {class_names[class_id]}: {percentage:.2f}%")

# 绘制分布图
fig = plot_distribution(class_counts, class_names)

# 保存图像（如果指定了输出文件）
if OUTPUT_FILE:
    plt.savefig(OUTPUT_FILE, dpi=300, bbox_inches='tight')
    print(f"\nPlot saved to {OUTPUT_FILE}")

# 显示图像
plt.show()
