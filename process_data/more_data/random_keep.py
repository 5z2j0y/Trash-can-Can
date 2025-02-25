import os
import random
import shutil
from pathlib import Path


def get_image_files(folder_path):
    """获取指定文件夹下的所有图片文件"""
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']
    image_files = []
    
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path) and os.path.splitext(file)[1].lower() in image_extensions:
            image_files.append(file_path)
    
    return image_files


def keep_random_images(folder_path, num_to_keep, temp_folder=None):
    """随机保留指定数量的图片文件"""
    image_files = get_image_files(folder_path)
    
    if len(image_files) <= num_to_keep:
        print(f"文件夹中只有 {len(image_files)} 张图片，少于或等于要保留的 {num_to_keep} 张，不需要删除。")
        return
    
    # 随机选择要保留的图片
    images_to_keep = random.sample(image_files, num_to_keep)
    
    # 如果提供了临时文件夹，则将要删除的图片移动到那里
    if temp_folder:
        os.makedirs(temp_folder, exist_ok=True)
        for image_file in image_files:
            if image_file not in images_to_keep:
                filename = os.path.basename(image_file)
                shutil.move(image_file, os.path.join(temp_folder, filename))
        print(f"已将 {len(image_files) - num_to_keep} 张图片移动到临时文件夹 {temp_folder}")
    # 否则直接删除不需要保留的图片
    else:
        for image_file in image_files:
            if image_file not in images_to_keep:
                os.remove(image_file)
        print(f"已删除 {len(image_files) - num_to_keep} 张图片")
    
    print(f"成功随机保留了 {num_to_keep} 张图片")


def main():
    # 直接在这里指定参数，而不是使用argparse
    folder_path = r"datasets\former_trash_png\carrot"  # 在这里修改为实际的文件夹路径
    num_to_keep = 100               # 在这里修改要保留的图片数量
    temp_folder = None             # 如果需要移动而不是删除，在这里指定临时文件夹路径
    
    if not os.path.isdir(folder_path):
        print(f"错误：{folder_path} 不是一个有效的文件夹路径")
        return
    
    if num_to_keep <= 0:
        print("错误：要保留的图片数量必须大于0")
        return
    
    keep_random_images(folder_path, num_to_keep, temp_folder)


if __name__ == "__main__":
    main()
