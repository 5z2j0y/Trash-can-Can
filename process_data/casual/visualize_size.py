import os
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from collections import defaultdict
import seaborn as sns
import csv

# 直接指定文件路径
NAMES_FILE = r"e:/github_projects/Trash-can-Can/trash.names"
LABELS_DIR = r"e:/github_projects/Trash-can-Can/images/renamed_labels"

def load_classes(names_file):
    """加载类别名称文件"""
    with open(names_file, 'r', encoding='utf-8') as f:
        classes = [line.strip() for line in f.readlines() if line.strip()]
    return classes

def collect_bbox_data(labels_dir, class_names):
    """收集边界框数据，包括中心点坐标和宽高"""
    data_by_class = defaultdict(lambda: {'cx': [], 'cy': [], 'widths': [], 'heights': []})
    label_files = list(Path(labels_dir).glob('*.txt'))
    
    print(f"找到 {len(label_files)} 个标签文件。")
    
    for label_file in label_files:
        with open(label_file, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 5:
                    try:
                        class_id = int(parts[0])
                        if class_id < len(class_names):
                            # YOLO格式: class_id, x_center, y_center, width, height (归一化)
                            cx = float(parts[1])
                            cy = float(parts[2])
                            width = float(parts[3])
                            height = float(parts[4])
                            class_name = class_names[class_id]
                            data_by_class[class_name]['cx'].append(cx)
                            data_by_class[class_name]['cy'].append(cy)
                            data_by_class[class_name]['widths'].append(width)
                            data_by_class[class_name]['heights'].append(height)
                    except (ValueError, IndexError) as e:
                        print(f"解析 {label_file} 中的行时出错: {line.strip()}, 错误: {e}")
    
    return data_by_class

def calculate_statistics(data_by_class):
    """计算各类别边界框的统计数据"""
    stats = {}
    for class_name, data in data_by_class.items():
        cx_values = np.array(data['cx'])
        cy_values = np.array(data['cy'])
        widths = np.array(data['widths'])
        heights = np.array(data['heights'])
        
        if len(widths) == 0 or len(heights) == 0:
            print(f"警告: 类别 {class_name} 没有数据")
            continue
            
        stats[class_name] = {
            'cx_mean': np.mean(cx_values),
            'cx_std': np.std(cx_values),
            'cy_mean': np.mean(cy_values),
            'cy_std': np.std(cy_values),
            'width_mean': np.mean(widths),
            'width_std': np.std(widths),
            'height_mean': np.mean(heights),
            'height_std': np.std(heights),
            'count': len(widths),
            'cx_1sigma': (
                np.mean(cx_values) - 1 * np.std(cx_values),
                np.mean(cx_values) + 1 * np.std(cx_values)
            ),
            'cy_1sigma': (
                np.mean(cy_values) - 1 * np.std(cy_values),
                np.mean(cy_values) + 1 * np.std(cy_values)
            ),
            'width_1sigma': (
                np.mean(widths) - 1 * np.std(widths),
                np.mean(widths) + 1 * np.std(widths)
            ),
            'height_1sigma': (
                np.mean(heights) - 1 * np.std(heights),
                np.mean(heights) + 1 * np.std(heights)
            )
        }
    return stats

def visualize_distributions(data_by_class, stats):
    """可视化边界框中心点和宽高的分布"""
    # 设置具有四个子图的图表
    plt.figure(figsize=(18, 14))
    
    # CX 分布
    plt.subplot(2, 2, 1)
    for class_name, data in data_by_class.items():
        if len(data['cx']) > 0:
            sns.kdeplot(data['cx'], label=f"{class_name} (n={len(data['cx'])})")
    plt.title('X Center Distribution by Class')
    plt.xlabel('Normalized X Center')
    plt.ylabel('Density')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # CY 分布
    plt.subplot(2, 2, 2)
    for class_name, data in data_by_class.items():
        if len(data['cy']) > 0:
            sns.kdeplot(data['cy'], label=f"{class_name} (n={len(data['cy'])})")
    plt.title('Y Center Distribution by Class')
    plt.xlabel('Normalized Y Center')
    plt.ylabel('Density')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # 宽度分布
    plt.subplot(2, 2, 3)
    for class_name, data in data_by_class.items():
        if len(data['widths']) > 0:
            sns.kdeplot(data['widths'], label=f"{class_name} (n={len(data['widths'])})")
    plt.title('Width Distribution by Class')
    plt.xlabel('Normalized Width')
    plt.ylabel('Density')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # 高度分布
    plt.subplot(2, 2, 4)
    for class_name, data in data_by_class.items():
        if len(data['heights']) > 0:
            sns.kdeplot(data['heights'], label=f"{class_name} (n={len(data['heights'])})")
    plt.title('Height Distribution by Class')
    plt.xlabel('Normalized Height')
    plt.ylabel('Density')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig('bbox_distribution_analysis.png', dpi=300)
    print(f"图表已保存为 bbox_distribution_analysis.png")
    plt.show()

def print_statistics(stats):
    """打印统计结果"""
    print("\n===== 边界框位置和尺寸统计 =====")
    headers = ['类别', '数量', 'CX均值', 'CX标准差', 'CY均值', 'CY标准差', '宽度均值', '宽度标准差', '高度均值', '高度标准差']
    print(f"{headers[0]:<15} {headers[1]:>8} {headers[2]:>10} {headers[3]:>10} {headers[4]:>10} {headers[5]:>10} {headers[6]:>10} {headers[7]:>10} {headers[8]:>10} {headers[9]:>10}")
    print("-" * 105)
    
    for class_name, stat in stats.items():
        print(f"{class_name:<15} {stat['count']:>8} {stat['cx_mean']:>10.4f} {stat['cx_std']:>10.4f} "
              f"{stat['cy_mean']:>10.4f} {stat['cy_std']:>10.4f} {stat['width_mean']:>10.4f} "
              f"{stat['width_std']:>10.4f} {stat['height_mean']:>10.4f} {stat['height_std']:>10.4f}")
    
    print("\n===== 1-Sigma 范围 (68.3% 的数据) =====")
    headers = ['类别', 'CX范围', 'CY范围', '宽度范围', '高度范围']
    print(f"{headers[0]:<15} {headers[1]:>25} {headers[2]:>25} {headers[3]:>25} {headers[4]:>25}")
    print("-" * 115)
    
    for class_name, stat in stats.items():
        cx_min, cx_max = stat['cx_1sigma']
        cy_min, cy_max = stat['cy_1sigma']
        w_min, w_max = stat['width_1sigma']
        h_min, h_max = stat['height_1sigma']
        
        cx_range = f"{cx_min:.4f} - {cx_max:.4f}"
        cy_range = f"{cy_min:.4f} - {cy_max:.4f}"
        width_range = f"{w_min:.4f} - {w_max:.4f}"
        height_range = f"{h_min:.4f} - {h_max:.4f}"
        
        print(f"{class_name:<15} {cx_range:>25} {cy_range:>25} {width_range:>25} {height_range:>25}")

def save_statistics(stats, output_file_prefix="bbox_stats"):
    """仅保存统计结果到CSV文件中"""
    # 保存1sigma范围为CSV格式，使用英文表头
    sigma_file = f"{output_file_prefix}_1sigma.csv"
    with open(sigma_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # 写入英文表头
        writer.writerow(['class', 'cx_min', 'cx_max', 'cy_min', 'cy_max', 'width_min', 'width_max', 'height_min', 'height_max'])
        
        # 写入每个类别的1sigma范围
        for class_name, stat in stats.items():
            cx_min, cx_max = stat['cx_1sigma']
            cy_min, cy_max = stat['cy_1sigma']
            width_min, width_max = stat['width_1sigma']
            height_min, height_max = stat['height_1sigma']
            
            writer.writerow([
                class_name, 
                f"{cx_min:.6f}", f"{cx_max:.6f}",
                f"{cy_min:.6f}", f"{cy_max:.6f}",
                f"{width_min:.6f}", f"{width_max:.6f}",
                f"{height_min:.6f}", f"{height_max:.6f}"
            ])
    
    print(f"1-Sigma范围数据已保存到 {sigma_file}")

def main():
    """主函数"""
    # 加载类别名称
    class_names = load_classes(NAMES_FILE)
    print(f"加载了 {len(class_names)} 个类别名称: {class_names}")
    
    # 收集边界框数据
    data_by_class = collect_bbox_data(LABELS_DIR, class_names)
    
    # 计算统计数据
    stats = calculate_statistics(data_by_class)
    
    # 打印统计结果
    print_statistics(stats)
    
    # 可视化分布
    visualize_distributions(data_by_class, stats)
    
    # 保存统计结果
    save_statistics(stats)

if __name__ == "__main__":
    main()
