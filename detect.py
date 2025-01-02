import cv2
from ultralytics import YOLO

# 加载模型
model = YOLO(r"models\yolo\examples\yolov11s.pt")  # 加载官方模型

# 定义发送到Arduino的函数
def send_to_arduino(cls_id):
    print(f"Sending to Arduino: {cls_id}")

# 打开视频捕捉
video_cap = cv2.VideoCapture(0)

# 初始化变量
last_cls_id = None
frame_count = 0
threshold = 5  # 连续帧数阈值

while video_cap.isOpened():
    success, frame = video_cap.read()
    if not success:
        break

    # 设置置信度
    conf = 0.8
    # 进行YOLO预测
    results = model.predict(frame, conf=conf)
    
    for result in results:
        # 绘制结果
        frame = result.plot()
        # 取出结果的类别、置信度、坐标
        boxes = result.boxes
        for box in boxes:
            cls_id = int(box.cls.item())
            score = box.conf.item()
            label = model.names[cls_id]

            # 检测相同的cls_id
            if cls_id == last_cls_id:
                frame_count += 1
            else:
                last_cls_id = cls_id
                frame_count = 1
            # 如果连续帧数超过阈值, 发送到Arduino
            if frame_count >= threshold:
                send_to_arduino(cls_id)
                frame_count = 0  # 重置计数器

    cv2.imshow('Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放资源
video_cap.release()
cv2.destroyAllWindows()