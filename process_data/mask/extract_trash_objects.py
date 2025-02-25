import os
import cv2
import json
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

def load_image_and_json(image_path, json_path):
    """加载图像和对应的JSON标注文件"""
    # 加载图像
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # 加载JSON
    with open(json_path, 'r') as f:
        annotation = json.load(f)
    
    return image, annotation

def create_mask_from_polygon(shape, height, width):
    """从多边形点创建蒙版"""
    mask = np.zeros((height, width), dtype=np.uint8)
    
    # 处理多边形
    if shape['shape_type'] == 'polygon':
        points = np.array(shape['points'], dtype=np.int32)
        cv2.fillPoly(mask, [points], 1)
    
    # 处理矩形 (转换为多边形)
    elif shape['shape_type'] == 'rectangle':
        x1, y1 = map(int, shape['points'][0])
        x2, y2 = map(int, shape['points'][1])
        points = np.array([[x1, y1], [x2, y1], [x2, y2], [x1, y2]], dtype=np.int32)
        cv2.fillPoly(mask, [points], 1)
    
    return mask

def extract_object(image, mask):
    """使用蒙版从图像中提取对象，创建带有透明背景的图像"""
    # 创建RGBA图像
    rgba = np.zeros((image.shape[0], image.shape[1], 4), dtype=np.uint8)
    rgba[:, :, :3] = image  # 复制RGB通道
    
    # Alpha通道：蒙版位置为255（完全不透明），其他位置为0（完全透明）
    rgba[:, :, 3] = mask * 255
    
    return rgba

def crop_to_content(rgba_image):
    """裁剪图像，只保留包含内容的部分"""
    # 查找非零值（非透明部分）
    non_zero = np.nonzero(rgba_image[:, :, 3])
    if len(non_zero[0]) == 0 or len(non_zero[1]) == 0:
        return rgba_image  # 如果没有内容，返回原始图像
    
    # 获取边界框
    min_y, max_y = np.min(non_zero[0]), np.max(non_zero[0])
    min_x, max_x = np.min(non_zero[1]), np.max(non_zero[1])
    
    # 添加一个小的边距
    padding = 10
    min_y = max(0, min_y - padding)
    min_x = max(0, min_x - padding)
    max_y = min(rgba_image.shape[0], max_y + padding)
    max_x = min(rgba_image.shape[1], max_x + padding)
    
    # 裁剪图像
    cropped = rgba_image[min_y:max_y, min_x:max_x]
    
    # 返回裁剪的图像和裁剪的坐标
    return cropped, (min_x, min_y, max_x, max_y)

def update_json_for_cropped_image(annotation, crop_coords, original_shape, new_shape):
    """更新JSON标注以匹配裁剪的图像"""
    # 解包裁剪坐标
    min_x, min_y, max_x, max_y = crop_coords
    
    # 创建新的JSON标注
    new_annotation = annotation.copy()
    new_annotation["imageHeight"] = new_shape[0]
    new_annotation["imageWidth"] = new_shape[1]
    
    # 更新所有形状的坐标
    for shape in new_annotation["shapes"]:
        new_points = []
        for point in shape["points"]:
            x, y = point
            # 调整坐标，减去裁剪区域的原点
            new_x = x - min_x
            new_y = y - min_y
            new_points.append([new_x, new_y])
        shape["points"] = new_points
    
    return new_annotation

def extract_trash_objects(input_dir, output_dir, visualize=False):
    """从源图像中提取垃圾对象并保存为带透明背景的PNG"""
    os.makedirs(output_dir, exist_ok=True)
    
    # 获取所有图像文件
    image_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.png')]
    
    for img_file in image_files:
        # 构建路径
        img_path = os.path.join(input_dir, img_file)
        json_path = os.path.join(input_dir, os.path.splitext(img_file)[0] + '.json')
        
        # 检查是否存在对应的JSON文件
        if not os.path.exists(json_path):
            print(f"找不到 {img_file} 对应的JSON标注，跳过")
            continue
        
        # 加载图像和JSON
        image, annotation = load_image_and_json(img_path, json_path)
        height, width = image.shape[:2]
        
        # 为每个标注形状单独提取对象
        for i, shape in enumerate(annotation['shapes']):
            # 创建蒙版
            mask = create_mask_from_polygon(shape, height, width)
            
            # 提取对象
            extracted_object = extract_object(image, mask)
            
            # 裁剪到内容
            cropped_object, crop_coords = crop_to_content(extracted_object)
            
            # 创建单独的标注JSON
            single_shape_annotation = {
                "version": annotation.get("version", "4.5.6"),
                "flags": {},
                "shapes": [shape.copy()],
                "imagePath": os.path.splitext(img_file)[0] + f"_obj{i}.png",
                "imageData": None,
                "imageHeight": height,
                "imageWidth": width
            }
            
            # 更新JSON以匹配裁剪后的图像
            updated_annotation = update_json_for_cropped_image(
                single_shape_annotation, crop_coords, 
                (height, width), cropped_object.shape[:2]
            )
            
            # 生成输出文件名
            base_name = os.path.splitext(img_file)[0]
            obj_name = f"{base_name}_obj{i}"
            output_img_path = os.path.join(output_dir, f"{obj_name}.png")
            output_json_path = os.path.join(output_dir, f"{obj_name}.json")
            
            # 保存提取的对象
            cv2.imwrite(output_img_path, cv2.cvtColor(cropped_object, cv2.COLOR_RGBA2BGRA))
            
            # 保存更新的JSON
            with open(output_json_path, 'w') as f:
                json.dump(updated_annotation, f, indent=2)
            
            # 可视化
            if visualize:
                plt.figure(figsize=(15, 5))
                
                plt.subplot(1, 3, 1)
                plt.imshow(image)
                plt.title("原始图像")
                
                plt.subplot(1, 3, 2)
                plt.imshow(mask, cmap='gray')
                plt.title(f"蒙版 ({shape['label']})")
                
                plt.subplot(1, 3, 3)
                # 创建白色背景用于显示透明图像
                bg = np.ones((cropped_object.shape[0], cropped_object.shape[1], 3)) * 240
                # 合成显示
                alpha = cropped_object[:, :, 3:4] / 255
                rgb = cropped_object[:, :, :3]
                composite = bg * (1 - alpha) + rgb * alpha
                
                plt.imshow(composite.astype(np.uint8))
                plt.title("提取的对象")
                
                plt.suptitle(f"对象提取: {obj_name}")
                plt.tight_layout()
                plt.show()
        
        print(f"已处理: {img_file}")
    
    print(f"所有对象提取完成，已保存到 {output_dir}")

if __name__ == "__main__":
    input_directory = r"images\test\extracted_trash"  # 输入包含原始图像和标注的目录
    output_directory = r"images\test\extracted_trash_cropped"  # 输出提取的垃圾对象
    
    extract_trash_objects(input_directory, output_directory, visualize=False)
