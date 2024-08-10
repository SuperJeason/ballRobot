from ultralytics import YOLO

model = YOLO("runs/detect/train/weights/best.pt")  # 加载自定义训练的模型


results = model.predict(
    "testData/test2.JPG"
)

for result in results:
    jsonRsult = result.tojson()

    # 保存 JSON 数据到文件
    path = "resultBall/data.json"
    with open(path, "w") as file:
        file.write(jsonRsult)
