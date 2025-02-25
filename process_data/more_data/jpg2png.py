import os
from PIL import Image

def convert_jpg_to_png(input_folder, output_folder=None, class_name=None, start_number=1):
    """
    将指定文件夹中的所有jpg图片转换为png格式，并可选择按指定格式重命名
    
    参数:
        input_folder: 输入文件夹路径，包含jpg图片
        output_folder: 输出文件夹路径，如果为None，则使用输入文件夹
        class_name: 指定的类别名称，如果提供，将文件重命名为 "class_name#.png" 格式
        start_number: 文件编号的起始值，默认为1
    """
    if output_folder is None:
        output_folder = input_folder
    
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 获取所有文件
    files = os.listdir(input_folder)
    
    # 筛选出jpg文件
    jpg_files = [file for file in files if file.lower().endswith(('.jpg', '.jpeg'))]
    
    # 统计转换结果
    total_files = len(jpg_files)
    converted_files = 0
    failed_files = 0
    
    print(f"找到 {total_files} 个jpg/jpeg文件")
    
    # 计数器，用于给文件编号，从指定的起始值开始
    counter = start_number
    
    # 遍历并转换每个jpg文件
    for jpg_file in jpg_files:
        try:
            # 构建完整的文件路径
            input_path = os.path.join(input_folder, jpg_file)
            
            # 构建输出文件名
            if class_name:
                # 使用指定的类名和序号命名
                output_filename = f"{class_name}{counter}_temp.png"
                counter += 1
            else:
                # 保持原文件名，仅更改扩展名
                file_name, _ = os.path.splitext(jpg_file)
                output_filename = f"{file_name}.png"
            
            output_path = os.path.join(output_folder, output_filename)
            
            # 打开图片并转换
            with Image.open(input_path) as img:
                img.save(output_path, 'PNG')
            
            print(f"已转换: {jpg_file} -> {output_filename}")
            converted_files += 1
            
        except Exception as e:
            print(f"转换失败: {jpg_file}, 错误: {str(e)}")
            failed_files += 1
    
    # 输出统计结果
    print("\n转换完成!")
    print(f"总计: {total_files} 个文件")
    print(f"成功: {converted_files} 个文件")
    print(f"失败: {failed_files} 个文件")

if __name__ == "__main__":
    # 直接指定输入和输出文件夹路径
    input_folder = r"datasets\former_trash\hongluobo"  # 请替换为实际的输入文件夹路径
    output_folder = r"datasets\former_trash_png\carrot"  # 请替换为实际的输出文件夹路径
    class_name = "carrot"  # 指定类名，如果不需要重命名，设为None
    start_number = 1  # 指定起始编号
    
    # 执行转换
    convert_jpg_to_png(input_folder, output_folder, class_name, start_number)
