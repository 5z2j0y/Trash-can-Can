import os
import random
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from PIL import Image

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

# 创建从0开始的标签映射
LABEL_COLORS = {i: COLORS[i % len(COLORS)] for i in range(len(CLASS_NAMES))}
LABEL_NAMES = {i: name for i, name in enumerate(CLASS_NAMES)}

def visualize_yolo(images_dir, labels_dir, num_images=20):
    """可视化指定数量的随机图片及其YOLO格式标注"""
    image_files = [f for f in os.listdir(images_dir) if f.endswith('.jpg') or f.endswith('.png')]
    
    if len(image_files) > num_images:
        image_files = random.sample(image_files, num_images)
    num_images = len(image_files)

    # 创建4x5的子图布局
    fig, axes = plt.subplots(4, 5, figsize=(20, 16))
    fig.suptitle('Random Sample YOLO Annotation Visualization', fontsize=16)

    # 修改图例显示
    legend_elements = [plt.Line2D([0], [0], color=LABEL_COLORS[label], 
                      label=f'{label}:{LABEL_NAMES[label]}', linewidth=2)
                      for label in LABEL_NAMES]
    fig.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.99, 0.98))

    # 展平axes数组以便遍历
    axes_flat = axes.flatten()

    for idx, image_file in enumerate(image_files):
        image_path = os.path.join(images_dir, image_file)
        label_path = os.path.join(labels_dir, os.path.splitext(image_file)[0] + '.txt')

        # 显示图片
        img = Image.open(image_path)
        ax = axes_flat[idx]
        ax.imshow(img)
        width, height = img.size

        # 绘制标注框
        if os.path.exists(label_path):
            with open(label_path, 'r') as f:
                for line in f:
                    category_id, x_center, y_center, w, h = map(float, line.strip().split())
                    
                    # 转换YOLO坐标为像素坐标
                    x_center *= width
                    y_center *= height
                    w *= width
                    h *= height
                    x = x_center - w/2
                    y = y_center - h/2

                    # 获取类别对应的颜色
                    class_id = int(category_id)
                    color = LABEL_COLORS.get(class_id, 'yellow')

                    # 创建矩形patch
                    rect = Rectangle((x, y), w, h,
                                  fill=False, edgecolor=color, linewidth=2)
                    ax.add_patch(rect)

                    # 显示类别名称和ID
                    class_name = LABEL_NAMES.get(class_id, 'unknown')
                    ax.text(x, y-5, f'{class_id}:{class_name}',
                           color=color, fontsize=8,
                           bbox=dict(facecolor='white', alpha=0.7))

        # 设置子图标题和关闭坐标轴
        ax.set_title(f'{image_file}', fontsize=8)
        ax.axis('off')

    # 隐藏空白子图
    for idx in range(num_images, 20):
        axes_flat[idx].axis('off')

    # 调整子图之间的间距
    plt.tight_layout()
    plt.subplots_adjust(top=0.95)

    # 显示图片
    plt.show()

if __name__ == "__main__":
    images_dir = r'images\renamed_png'
    labels_dir = r'images\renamed_labels'
    visualize_yolo(images_dir, labels_dir)
    print("可视化检查完成！")