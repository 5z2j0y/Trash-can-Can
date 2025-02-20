import os
import random
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from PIL import Image

# 定义类别颜色映射
LABEL_COLORS = {
    0: 'red',       # bottle
    1: 'blue',      # brick
    2: 'green',     # battery
    3: 'yellow',    # can
    4: 'purple',    # carrot
    5: 'orange',    # china
    6: 'pink',      # paperCup
    7: 'cyan',      # pill
    8: 'brown',     # potato
    9: 'gray',      # radish
    10: 'lime',     # stone
    11: 'magenta'   # potato_chip
}

# 添加类别名称映射
LABEL_NAMES = {
    0: 'bottle',
    1: 'brick',
    2: 'battery',
    3: 'can',
    4: 'carrot',
    5: 'china',
    6: 'paperCup',
    7: 'pill',
    8: 'potato',
    9: 'radish',
    10: 'stone',
    11: 'potato_chip'
}

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
    legend_elements = [plt.Line2D([0], [0], color=color, label=f'{label}:{name}', linewidth=2)
                      for label, (color, name) in enumerate(zip(LABEL_COLORS.values(), LABEL_NAMES.values()))]
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
                    color = LABEL_COLORS.get(int(category_id), 'yellow')

                    # 创建矩形patch
                    rect = Rectangle((x, y), w, h,
                                  fill=False, edgecolor=color, linewidth=2)
                    ax.add_patch(rect)

                    # 修改标签文本显示
                    class_id = int(category_id)
                    ax.text(x, y-5, f'{class_id}:{LABEL_NAMES[class_id]}',
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
    images_dir = r'datasets\trashcan\valid'
    labels_dir = images_dir
    visualize_yolo(images_dir, labels_dir)
    print("可视化检查完成！")