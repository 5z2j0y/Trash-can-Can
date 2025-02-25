
import os
import json
import cv2
from pathlib import Path
from tqdm import tqdm

def convert_jpg_to_png(input_dir):
    """
    将指定目录下的所有JPG文件转换为PNG文件，并更新对应JSON文件中的imagePath
    
    Args:
        input_dir: 输入目录路径
    """
    # 创建Path对象以操作路径
    input_path = Path(input_dir)
    
    # 查找所有jpg和jpeg文件
    jpg_files = list(input_path.glob("*.jpg")) + list(input_path.glob("*.jpeg"))
    
    if not jpg_files:
        print(f"在目录 {input_dir} 中未找到任何JPG/JPEG文件")
        return
    
    print(f"找到 {len(jpg_files)} 个JPG/JPEG文件，开始转换...")
    
    # 使用tqdm显示进度条
    for jpg_file in tqdm(jpg_files, desc="转换进度"):
        # 定义对应的PNG文件名
        png_file = jpg_file.with_suffix(".png")
        
        # 读取图像
        try:
            img = cv2.imread(str(jpg_file))
            if img is None:
                print(f"无法读取图像: {jpg_file}")
                continue
                
            # 保存为PNG
            cv2.imwrite(str(png_file), img)
            
            # 寻找对应的JSON文件
            json_file = jpg_file.with_suffix(".json")
            if json_file.exists():
                # 读取JSON文件
                with open(json_file, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)
                
                # 更新imagePath字段
                old_image_path = json_data.get('imagePath', '')
                if old_image_path.endswith(('.jpg', '.jpeg', '.JPG', '.JPEG')):
                    # 替换扩展名为.png
                    base_name = os.path.splitext(old_image_path)[0]
                    json_data['imagePath'] = f"{base_name}.png"
                    
                    # 保存更新后的JSON文件
                    with open(json_file, 'w', encoding='utf-8') as f:
                        json.dump(json_data, f, indent=2, ensure_ascii=False)
                        
            # 可选：删除原始JPG文件
            # jpg_file.unlink()
            
        except Exception as e:
            print(f"处理文件 {jpg_file} 时出错: {str(e)}")
    
    print("转换完成!")

def main():
    # 设置命令行参数
    import argparse
    parser = argparse.ArgumentParser(description='将JPG图像转换为PNG并更新JSON标注')
    parser.add_argument('input_dir', help='包含JPG图像和JSON标注的目录')
    parser.add_argument('--delete', action='store_true', help='转换后删除原始JPG文件')
    
    args = parser.parse_args()
    
    # 执行转换
    convert_jpg_to_png(args.input_dir)
    
    # 如果指定了删除原始文件
    if args.delete:
        input_path = Path(args.input_dir)
        jpg_files = list(input_path.glob("*.jpg")) + list(input_path.glob("*.jpeg"))
        for jpg_file in tqdm(jpg_files, desc="删除原始JPG文件"):
            jpg_file.unlink()
        print(f"已删除 {len(jpg_files)} 个原始JPG文件")

if __name__ == "__main__":
    # 如果直接运行脚本，使用命令行参数
    # 否则可以直接调用convert_jpg_to_png函数
    # main()
    
    # 或者可以直接指定目录
    convert_jpg_to_png(r"E:\github_projects\Trash-can-Can\images\test\extracted_trash")
