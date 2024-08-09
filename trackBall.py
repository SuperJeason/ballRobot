from ultralytics import YOLO

# 加载官方或自定义模型
model = YOLO("model/yolov8n.pt")  # 加载官方检测模型
model = YOLO("model/yolov8n-seg.pt")  # 加载官方分割模型
model = YOLO("model/yolov8n-pose.pt")  # 加载官方姿态估计模型
model = YOLO("runs/detect/train/weights/best.pt")  # 加载自定义训练的模型

# 使用模型进行跟踪
# results = model.track("testData/test1.mp4")  # 使用默认跟踪器进行跟踪
results = model.track(
    "testData/test2.JPG", tracker="bytetrack.yaml"
)  # 使用ByteTrack进行跟踪

for i, r in enumerate(results):
    r.boxes.cls()
    
