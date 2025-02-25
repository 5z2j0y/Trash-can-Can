import os
import glob

def clear_unlabeled_images(directory, label_ext='json'):
    # 获取所有图片文件
    image_files = glob.glob(os.path.join(directory, "*.png"))
    image_files.extend(glob.glob(os.path.join(directory, "*.jpg")))
    
    removed_count = 0
    
    for image_path in image_files:
        # 构建对应的标签文件路径
        label_path = os.path.splitext(image_path)[0] + f'.{label_ext}'
        
        # 如果不存在对应的标签文件，删除图片
        if not os.path.exists(label_path):
            try:
                os.remove(image_path)
                print(f"已删除: {image_path}")
                removed_count += 1
            except Exception as e:
                print(f"删除失败 {image_path}: {str(e)}")
    
    print(f"\n清理完成! 总共删除了 {removed_count} 个未标注的图片文件。")
    print(f"还剩下 {len(image_files) - removed_count} 个文件。")

if __name__ == "__main__":
    # 指定要处理的目录路径
    target_directory = r"datasets\former_trash_png\carrot"  # 请替换为实际的目录路径

    """
    ---------------------------------------------------
                ！！！先别急着运行！！！
    如果是要根据json清除，那么label_extension = "json"
    如果是要根据txt清除，那么label_extension = "txt"
    ---------------------------------------------------
    """
    label_extension = "json"  # 可以改为 "txt" 或其他扩展名
    
    if os.path.exists(target_directory):
        print(f"开始处理目录: {target_directory}")
        clear_unlabeled_images(target_directory, label_extension)
    else:
        print("错误: 指定的目录不存在!")
