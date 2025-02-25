import os
import cv2
import json
import random
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from datetime import datetime

def load_png_with_alpha(image_path):
    """加载PNG图片，保留alpha通道"""
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    # 确保图像有4个通道，包含alpha
    if image.shape[2] == 4:
        # 转换为RGB+Alpha (OpenCV读取为BGRA)
        return cv2.cvtColor(image, cv2.COLOR_BGRA2RGBA)
    else:
        # 如果只有3通道，创建一个alpha通道
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        alpha = np.ones((image.shape[0], image.shape[1], 1), dtype=np.uint8) * 255
        return np.concatenate((rgb, alpha), axis=2)

def load_background(bg_path):
    """加载背景图片"""
    bg = cv2.imread(bg_path)
    return cv2.cvtColor(bg, cv2.COLOR_BGR2RGB)

def load_json_annotation(json_path):
    """加载labelme的JSON标注文件"""
    with open(json_path, 'r') as f:
        return json.load(f)

def update_polygon_position(shapes, offset_x, offset_y, scale_factor=1.0):
    """更新多边形位置，根据偏移量和缩放因子"""
    updated_shapes = []
    
    for shape in shapes:
        new_shape = shape.copy()
        new_points = []
        
        for point in shape['points']:
            # 应用缩放和偏移
            new_x = point[0] * scale_factor + offset_x
            new_y = point[1] * scale_factor + offset_y
            new_points.append([new_x, new_y])
        
        new_shape['points'] = new_points
        updated_shapes.append(new_shape)
    
    return updated_shapes

def composite_image(fg_img, bg_img, position=(0, 0), resize_factor=None):
    """将前景图像合成到背景图像上"""
    # 如果需要，调整前景图像大小
    if resize_factor is not None and resize_factor != 1.0:
        new_height = int(fg_img.shape[0] * resize_factor)
        new_width = int(fg_img.shape[1] * resize_factor)
        fg_img = cv2.resize(fg_img, (new_width, new_height))
    
    # 确保位置在背景图像的有效范围内
    x_pos, y_pos = position
    if x_pos < 0:
        x_pos = 0
    if y_pos < 0:
        y_pos = 0
        
    # 计算前景图像在背景上的区域
    fg_height, fg_width = fg_img.shape[:2]
    bg_height, bg_width = bg_img.shape[:2]
    
    # 确保前景不超出背景
    if x_pos + fg_width > bg_width:
        x_pos = bg_width - fg_width
    if y_pos + fg_height > bg_height:
        y_pos = bg_height - fg_height
    
    # 创建合成图像的副本
    result = bg_img.copy()
    
    # 获取前景区域
    roi = result[y_pos:y_pos+fg_height, x_pos:x_pos+fg_width]
    
    # 分离前景的RGB和alpha通道
    fg_rgb = fg_img[:, :, :3]
    fg_alpha = fg_img[:, :, 3:4] / 255.0  # 归一化alpha值
    
    # 使用alpha通道进行混合
    for c in range(3):
        result[y_pos:y_pos+fg_height, x_pos:x_pos+fg_width, c] = \
            roi[:, :, c] * (1 - fg_alpha[:, :, 0]) + \
            fg_rgb[:, :, c] * fg_alpha[:, :, 0]
    
    return result, (x_pos, y_pos)

def replace_backgrounds(extracted_dir, bg_dir, output_dir, num_compositions=50, visualize=False):
    """将提取的垃圾样品放置在随机背景上"""
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 获取所有的PNG文件
    extracted_files = [f for f in os.listdir(extracted_dir) if f.endswith('.png')]
    bg_files = [f for f in os.listdir(bg_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
    
    if not extracted_files:
        print(f"在 {extracted_dir} 中未找到PNG文件")
        return
    
    if not bg_files:
        print(f"在 {bg_dir} 中未找到背景图片")
        return
    
    # 生成指定数量的合成图像
    for comp_idx in range(num_compositions):
        # 随机选择一个背景
        bg_file = random.choice(bg_files)
        bg_path = os.path.join(bg_dir, bg_file)
        bg_img = load_background(bg_path)
        bg_height, bg_width = bg_img.shape[:2]
        
        # 随机选择1-3个垃圾样品
        num_trash = random.randint(1, min(3, len(extracted_files)))
        selected_trash = random.sample(extracted_files, num_trash)
        
        # 创建一个新的合成图像
        composite = bg_img.copy()
        # 创建新的标注文件模板
        new_annotation = {
            "version": "4.5.6",
            "flags": {},
            "shapes": [],
            "imagePath": "",
            "imageData": None,
            "imageHeight": bg_height,
            "imageWidth": bg_width
        }
        
        # 为每个垃圾样品生成合成
        for trash_file in selected_trash:
            # 加载垃圾样品图片
            trash_img_path = os.path.join(extracted_dir, trash_file)
            trash_img = load_png_with_alpha(trash_img_path)
            
            # 加载对应的JSON标注
            json_file = os.path.splitext(trash_file)[0] + '.json'
            json_path = os.path.join(extracted_dir, json_file)
            
            if not os.path.exists(json_path):
                print(f"找不到 {trash_file} 对应的JSON标注文件，跳过此样品")
                continue
                
            trash_annotation = load_json_annotation(json_path)
            
            # 随机确定缩放因子 (0.5-0.8)
            scale_factor = random.uniform(0.5, 0.8)
            
            # 计算缩放后的尺寸
            scaled_width = int(trash_img.shape[1] * scale_factor)
            scaled_height = int(trash_img.shape[0] * scale_factor)
            
            # 随机确定位置 (确保完全在背景图像内)
            max_x = bg_width - scaled_width
            max_y = bg_height - scaled_height
            
            if max_x <= 0 or max_y <= 0:
                # 如果缩放后的图像比背景大，重新选择缩放因子
                continue
                
            pos_x = random.randint(0, max_x)
            pos_y = random.randint(0, max_y)
            
            # 合成图像
            composite, actual_position = composite_image(
                trash_img, composite, position=(pos_x, pos_y), resize_factor=scale_factor
            )
            
            # 更新标注位置
            actual_x, actual_y = actual_position
            updated_shapes = update_polygon_position(
                trash_annotation['shapes'], actual_x, actual_y, scale_factor
            )
            
            # 将更新后的标注添加到新标注中
            new_annotation['shapes'].extend(updated_shapes)
        
        # 生成输出文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        output_basename = f"composite_{timestamp}_{comp_idx}"
        output_img_path = os.path.join(output_dir, f"{output_basename}.jpg")
        output_json_path = os.path.join(output_dir, f"{output_basename}.json")
        
        # 更新标注中的图像路径
        new_annotation['imagePath'] = f"{output_basename}.jpg"
        
        # 保存合成图像
        cv2.imwrite(output_img_path, cv2.cvtColor(composite, cv2.COLOR_RGB2BGR))
        
        # 保存标注文件
        with open(output_json_path, 'w') as f:
            json.dump(new_annotation, f, indent=2)
            
        # 可视化结果
        if visualize and comp_idx < 5:  # 只显示前5个结果用于调试
            plt.figure(figsize=(10, 8))
            plt.imshow(composite)
            
            # 绘制标注
            for shape in new_annotation['shapes']:
                # 获取多边形点
                points = np.array(shape['points'])
                
                # 绘制多边形
                plt.plot(points[:, 0], points[:, 1], '-', linewidth=2, color='red')
                
                # 显示标签
                label = shape['label']
                centroid = points.mean(axis=0)
                plt.text(centroid[0], centroid[1], label, color='white', 
                        backgroundcolor='red', fontsize=8)
            
            plt.title(f"合成 {comp_idx+1}")
            plt.axis('off')
            plt.tight_layout()
            plt.show()
        
        print(f"已创建第 {comp_idx+1}/{num_compositions} 张合成图像")
    
    print(f"所有 {num_compositions} 张合成图像已保存到 {output_dir}")

if __name__ == "__main__":
    # 定义路径
    extracted_trash_dir = r"images\test\extracted_trash_cropped"
    background_dir = r"images\test\blank_background"
    output_dir = r"images\test\synthetic_trash"
    
    # 创建合成图像
    replace_backgrounds(
        extracted_trash_dir,
        background_dir,
        output_dir,
        num_compositions=20,  # 创建20张合成图像
        visualize=False  # 设置为True可以查看前5个结果
    )
