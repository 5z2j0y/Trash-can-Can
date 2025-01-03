import cv2
from ultralytics import YOLO
import serial
import time

# 加载模型
model = YOLO(r"models\trashcan.pt", verbose=False) 

# 配置串口连接
arduino_port = "/dev/ttyUSB0"  # 根据你的系统调整端口，Windows 上可能是 "COM3"
baud_rate = 9600  # 波特率，应与 Arduino 代码一致
timeout = 1  # 超时时间（秒）

try:
    # 打开串口
    ser = serial.Serial(arduino_port, baud_rate, timeout=timeout)
    print(f"成功连接到 Arduino，端口: {arduino_port}")
    time.sleep(2)  # 等待 Arduino 初始化

    # 定义发送到Arduino的函数
    def send_to_arduino(trash_type):
        category_id = trash_category_ids.get(trash_type, 0)
        ser.write(str(category_id).encode())  # 将类别ID转换为字节并发送
        print(f"发送: {category_id}")

    # 定义垃圾分类
    trash_categories = {
        "可回收": ["bottle", "can", "paperCup"],
        "厨余": ["carrot", "potato", "radish", "potato_chip"],
        "有害": ["battery", "pill"],
        "其他": ["stone", "china", "brick"]
    }

    # 定义垃圾分类编号
    trash_category_ids = {
        "可回收": 1,
        "厨余": 2,
        "有害": 3,
        "其他": 4
    }

    def classify_trash(label):
        for category, items in trash_categories.items():
            if label in items:
                return category
        return "未知"

    video_path = "test.mp4"
    # 打开视频捕捉
    video_cap = cv2.VideoCapture(video_path)

    # 是否显示检测结果
    show_results = True 

    # 初始化变量
    last_cls_id = None
    frame_count = 0
    threshold = 5  # 连续帧数阈值

    while video_cap.isOpened():
        success, frame = video_cap.read()
        if not success:
            break

        # 裁切画面到480x480
        frame = frame[:, 80:560]

        # 调整尺寸为320x320
        frame = cv2.resize(frame, (320, 320))

        # 设置置信度
        conf = 0.7
        # 进行YOLO预测
        results = model.predict(frame, conf=conf, verbose=False)
        
        for result in results:
            # 只有在show_results为True时才绘制结果
            if show_results:
                frame = result.plot()
            # 取出结果的类别、置信度、坐标
            boxes = result.boxes
            for box in boxes:
                cls_id = int(box.cls.item())
                score = box.conf.item()
                label = model.names[cls_id]

                # 分类垃圾
                trash_type = classify_trash(label)

                # 检测相同的cls_id
                if cls_id == last_cls_id:
                    frame_count += 1
                else:
                    last_cls_id = cls_id
                    frame_count = 1
                # 如果连续帧数超过阈值, 发送到Arduino
                if frame_count >= threshold:
                    print(f" {label}, {trash_type}")
                    send_to_arduino(trash_type)
                    frame_count = 0  # 重置计数器

        # 只有在show_results为True时才显示图像
        if show_results:
            cv2.imshow('Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 释放资源
    video_cap.release()
    cv2.destroyAllWindows()

except serial.SerialException as e:
    print(f"串口错误: {e}")
except Exception as e:
    print(f"未知错误: {e}")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("已关闭串口连接。")