import os
import shutil
from PIL import Image
from tqdm import tqdm
import glob

def read_trash_names(file_path):
    """读取trash.names文件，返回类别列表"""
    with open(file_path, 'r') as f:
        names = [line.strip() for line in f if line.strip()]
    return names

def read_yolo_label(label_path):
    """读取YOLO标签文件，返回类别列表"""
    classes = []
    if os.path.exists(label_path):
        with open(label_path, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if parts:
                    class_id = int(parts[0])
                    classes.append(class_id)
    return classes

def main():
    # 路径设置
    names_file = 'trash.names'
    origin_img_dir = 'images/origin_img'
    yolo_labels_dir = 'images/yolo_labels'
    renamed_png_dir = 'images/renamed_png'
    renamed_labels_dir = 'images/renamed_labels'  # 新增重命名标签的目录
    
    # 确保输出目录存在
    os.makedirs(renamed_png_dir, exist_ok=True)
    os.makedirs(renamed_labels_dir, exist_ok=True)  # 创建标签输出目录
    
    # 读取类别名称
    trash_names = read_trash_names(names_file)
    print(f"读取到 {len(trash_names)} 个类别: {trash_names}")
    
    # 获取原始图片文件列表
    image_files = glob.glob(os.path.join(origin_img_dir, '*.*'))
    print(f"找到 {len(image_files)} 张图片需要处理")
    
    # 创建进度条
    for img_path in tqdm(image_files, desc="正在处理图片"):
        # 提取不带扩展名的文件名
        img_filename = os.path.basename(img_path)
        img_name = os.path.splitext(img_filename)[0]
        
        # 获取对应的标签文件路径
        label_path = os.path.join(yolo_labels_dir, f"{img_name}.txt")
        
        # 读取标签文件获取类别列表
        class_ids = read_yolo_label(label_path)
        
        if not class_ids:
            print(f"警告: 图片 {img_name} 没有找到标签或标签为空，跳过处理")
            continue
        
        # 打开图片准备转换为PNG
        try:
            img = Image.open(img_path)
            
            # 处理每个检测到的类别
            for i, class_id in enumerate(class_ids):
                if 0 <= class_id < len(trash_names):
                    class_name = trash_names[class_id]
                    new_filename = f"{class_name}{i+1}"
                    new_img_path = os.path.join(renamed_png_dir, f"{new_filename}.png")
                    new_label_path = os.path.join(renamed_labels_dir, f"{new_filename}.txt")
                    
                    # 如果文件已存在，添加一个序号
                    counter = 1
                    while os.path.exists(new_img_path) or os.path.exists(new_label_path):
                        new_filename = f"{class_name}{i+1}_{counter}"
                        new_img_path = os.path.join(renamed_png_dir, f"{new_filename}.png")
                        new_label_path = os.path.join(renamed_labels_dir, f"{new_filename}.txt")
                        counter += 1
                    
                    # 保存为PNG格式
                    img.save(new_img_path, 'PNG')
                    
                    # 复制并重命名标签文件
                    shutil.copy(label_path, new_label_path)
                else:
                    print(f"警告: 图片 {img_name} 中的类别ID {class_id} 超出范围")
            
        except Exception as e:
            print(f"处理图片 {img_name} 时出错: {e}")

if __name__ == "__main__":
    main()
    print("所有图片和对应的标签处理完成！")
