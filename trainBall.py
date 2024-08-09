from ultralytics import YOLO

if __name__ == "__main__":
    model = YOLO("model/yolov8m.pt")

    # 训练模型
    results = model.train(data="data/coco_ball.yaml", epochs=300)

    # 验证模型
    val_results = model.val()
