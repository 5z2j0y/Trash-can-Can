import os
import cv2
import json
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

# 从trash.names文件读取类别名称
def load_class_names(names_file):
    with open(names_file, 'r') as f:
        class_names = [line.strip() for line in f.readlines() if line.strip()]
    return class_names

# 获取项目根目录的trash.names文件路径 
project_root = r'E:\github_projects\Trash-can-Can'
names_file_path = os.path.join(project_root, 'trash.names')

# 加载类别名称
CLASS_NAMES = load_class_names(names_file_path)

# 定义类别颜色映射 - 自动生成
COLORS = ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 
          'pink', 'cyan', 'brown', 'gray', 'lime', 'magenta', 
          'olive', 'teal', 'navy', 'coral']

# 创建标签到颜色和名称的映射
LABEL_COLORS = {name: COLORS[i % len(COLORS)] for i, name in enumerate(CLASS_NAMES)}
LABEL_NAMES = {name: name for name in CLASS_NAMES}  # 直接使用名称作为标识符

# 将颜色名称转换为RGB值的函数
def color_name_to_rgb(color_name):
    color_map = {
        'red': [255, 0, 0],
        'blue': [0, 0, 255],
        'green': [0, 255, 0],
        'yellow': [255, 255, 0],
        'purple': [128, 0, 128],
        'orange': [255, 165, 0],
        'pink': [255, 192, 203],
        'cyan': [0, 255, 255],
        'brown': [165, 42, 42],
        'gray': [128, 128, 128],
        'lime': [50, 205, 50],
        'magenta': [255, 0, 255],
        'olive': [128, 128, 0],
        'teal': [0, 128, 128],
        'navy': [0, 0, 128],
        'coral': [255, 127, 80]
    }
    return color_map.get(color_name, [255, 255, 0])  # 默认黄色

def load_and_draw(img_path, json_path):
    """加载图片和JSON标注，并在图片上绘制多边形或蒙版"""
    # 读取图片
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # 读取JSON标注
    with open(json_path, 'r') as f:
        json_data = json.load(f)
    
    return img, json_data['shapes']

def visualize_mask_annotations(input_dir, num_images=20):
    """可视化指定数量的随机图片及其蒙版标注"""
    # 获取所有图片文件
    image_files = [f for f in os.listdir(input_dir) 
                   if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    # 随机抽取指定数量的图片
    if len(image_files) > num_images:
        image_files = random.sample(image_files, num_images)
    num_images = len(image_files)
    
    # 创建4x5的子图布局
    fig, axes = plt.subplots(4, 5, figsize=(20, 16))
    fig.suptitle('Random Sample Mask Annotation Visualization', fontsize=16)
    
    # 添加图例 - 改进与YOLO风格一致
    legend_elements = [plt.Line2D([0], [0], color=LABEL_COLORS.get(label, 'yellow'), 
                      label=f'{label}', linewidth=2)
                      for label in CLASS_NAMES]
    fig.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.99, 0.98))
    
    # 展平axes数组以便遍历
    axes_flat = axes.flatten()
    
    # 处理每张图片
    for idx, img_file in enumerate(image_files):
        img_path = os.path.join(input_dir, img_file)
        json_path = os.path.join(input_dir, os.path.splitext(img_file)[0] + '.json')
        
        if not os.path.exists(json_path):
            continue
            
        # 加载图片和标注
        img, shapes = load_and_draw(img_path, json_path)
        
        # 在当前子图上显示图片
        ax = axes_flat[idx]
        ax.imshow(img)
        
        # 绘制所有多边形或蒙版
        for shape in shapes:
            if shape['shape_type'] == 'polygon':
                points = np.array(shape['points'])
                label = shape['label']
                
                # 获取类别对应的颜色
                color = LABEL_COLORS.get(label, 'yellow')  # 默认黄色
                
                # 创建多边形补丁
                poly = Polygon(points, 
                             fill=True, 
                             alpha=0.4,
                             facecolor=color, 
                             edgecolor=color, 
                             linewidth=2)
                ax.add_patch(poly)
                
                # 添加标签文本 - 与YOLO风格一致
                x_min, y_min = points.min(axis=0)
                ax.text(x_min, y_min-5, f'{label}',
                       color=color, fontsize=8,
                       bbox=dict(facecolor='white', alpha=0.7))
            
            elif shape['shape_type'] == 'rectangle':
                points = shape['points']
                x1, y1 = points[0]
                x2, y2 = points[1]
                label = shape['label']
                
                # 获取类别对应的颜色
                color = LABEL_COLORS.get(label, 'yellow')  # 默认黄色
                
                # 将矩形转换为多边形点
                rect_points = np.array([[x1, y1], [x2, y1], [x2, y2], [x1, y2]])
                
                # 创建多边形补丁
                poly = Polygon(rect_points, 
                             fill=True, 
                             alpha=0.4,
                             facecolor=color, 
                             edgecolor=color, 
                             linewidth=2)
                ax.add_patch(poly)
                
                # 添加标签文本 - 与YOLO风格一致
                ax.text(x1, y1-5, f'{label}',
                       color=color, fontsize=8,
                       bbox=dict(facecolor='white', alpha=0.7))
        
        # 设置子图标题
        ax.set_title(f'{img_file}', fontsize=8)
        ax.axis('off')
    
    # 隐藏空白子图
    for idx in range(num_images, 20):
        axes_flat[idx].axis('off')
    
    # 调整子图之间的间距
    plt.tight_layout()
    plt.subplots_adjust(top=0.95)
    
    # 显示图片
    plt.show()

def create_binary_mask(img_shape, points):
    """从多边形点创建二进制蒙版"""
    mask = np.zeros(img_shape[:2], dtype=np.uint8)
    points_array = np.array(points, dtype=np.int32)
    cv2.fillPoly(mask, [points_array], 1)
    return mask

def visualize_single_mask(input_dir, img_file):
    """可视化单个图片的蒙版，展示原图、蒙版和覆盖效果"""
    img_path = os.path.join(input_dir, img_file)
    json_path = os.path.join(input_dir, os.path.splitext(img_file)[0] + '.json')
    
    if not os.path.exists(json_path) or not os.path.exists(img_path):
        print(f"找不到图片或JSON文件: {img_file}")
        return
    
    # 加载图片和标注
    img, shapes = load_and_draw(img_path, json_path)
    
    # 创建一个图像，包含3个子图：原图、蒙版、覆盖效果
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # 显示原图
    axes[0].imshow(img)
    axes[0].set_title("原图")
    axes[0].axis('off')
    
    # 创建并显示蒙版
    mask_overlay = np.zeros_like(img)
    binary_mask = np.zeros(img.shape[:2], dtype=np.uint8)
    
    for shape in shapes:
        if shape['shape_type'] == 'polygon' or shape['shape_type'] == 'rectangle':
            if shape['shape_type'] == 'rectangle':
                points = shape['points']
                x1, y1 = points[0]
                x2, y2 = points[1]
                points = [[x1, y1], [x2, y1], [x2, y2], [x1, y2]]
            else:
                points = shape['points']
            
            # 创建单个蒙版
            shape_mask = create_binary_mask(img.shape, points)
            binary_mask = np.logical_or(binary_mask, shape_mask).astype(np.uint8)
            
            # 为蒙版添加颜色
            color_name = LABEL_COLORS.get(shape['label'], 'yellow')
            # 将颜色名称转换为RGB值
            color = color_name_to_rgb(color_name)
                
            for c in range(3):
                mask_overlay[:, :, c] = np.where(
                    shape_mask == 1, 
                    mask_overlay[:, :, c] * 0.5 + color[c] * 0.5, 
                    mask_overlay[:, :, c]
                )
    
    # 显示蒙版
    axes[1].imshow(mask_overlay)
    axes[1].set_title("标注蒙版")
    axes[1].axis('off')
    
    # 显示覆盖效果
    overlay = img.copy()
    for c in range(3):
        overlay[:, :, c] = np.where(
            binary_mask == 1, 
            img[:, :, c] * 0.7 + mask_overlay[:, :, c] * 0.3, 
            img[:, :, c]
        )
    
    axes[2].imshow(overlay)
    axes[2].set_title("蒙版覆盖效果")
    axes[2].axis('off')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    input_directory = r"images\test\extracted_trash_cropped"
    # 可视化多张随机图片的蒙版标注
    visualize_mask_annotations(input_directory)
    
    # 如果您想查看单个图片的详细蒙版效果，可以取消下面的注释并指定图片名称
    # visualize_single_mask(input_directory, "某张图片.jpg")
    
    print("可视化蒙版检查完成！")