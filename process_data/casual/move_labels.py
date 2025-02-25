import os
import shutil
from pathlib import Path

def move_label_files(image_dir, label_dir, label_type='json'):
    """
    将标注文件移动到对应的图片文件夹
    
    Args:
        image_dir (str): 图片文件夹路径
        label_dir (str): 标注文件夹路径
        label_type (str): 标注文件类型，可选 'json' 或 'txt'
    """
    # 确保路径存在
    image_dir = Path(image_dir)
    label_dir = Path(label_dir)
    
    if not image_dir.exists() or not label_dir.exists():
        print("图片文件夹或标注文件夹不存在！")
        return
    
    # 验证标注文件类型
    if label_type not in ['json', 'txt']:
        print("不支持的标注文件类型！请使用 'json' 或 'txt'")
        return

    # 获取所有图片文件
    image_files = []
    for ext in ('*.jpg', '*.jpeg', '*.png'):
        image_files.extend(image_dir.rglob(ext))
    
    # 处理每个图片文件
    for image_path in image_files:
        # 获取不带扩展名的文件名
        image_stem = image_path.stem
        # 构建对应的标注文件路径
        label_path = label_dir / f"{image_stem}.{label_type}"
        
        if label_path.exists():
            # 复制标注文件到图片所在文件夹
            destination = image_path.parent / label_path.name
            try:
                shutil.copy2(label_path, destination)
                print(f"成功：复制 {label_path.name} 到 {destination.parent}")
            except Exception as e:
                print(f"错误：复制 {label_path.name} 失败 - {str(e)}")
        else:
            print(f"警告：未找到对应的{label_type}标注文件 {label_path.name}")

if __name__ == "__main__":
    # 设置图片文件夹和标注文件夹的路径
    IMAGE_DIR = r"images\landmark\datasets\train"  # 替换为你的图片文件夹路径
    LABEL_DIR = r"images\landmark\yolo_txt"  # 替换为你的标注文件夹路径

    """
    ---------------------------------------------------
                ！！！先别急着运行！！！
    如果标签是json，那么LABEL_TYPE = "json"
    如果标签是txt，那么LABEL_TYPE = "txt"
    ---------------------------------------------------
    """

    LABEL_TYPE = 'txt'  # 可以修改为 'txt'
    
    move_label_files(IMAGE_DIR, LABEL_DIR, LABEL_TYPE)