import cv2
import time
from ultralytics import YOLO

# 加载自定义训练的模型
model = YOLO("runs/detect/train/weights/best.pt")

# 打开视频文件
video_path = "testData/test1.mp4"
cap = cv2.VideoCapture(video_path)

# 获取视频的宽度、高度和帧率
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# 定义字体
font = cv2.FONT_HERSHEY_SIMPLEX

# 初始化时间
prev_frame_time = time.time()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 进行YOLO推理，返回处理后的图像
    results = model.predict(frame, show=False)
    annotated_frame = results[0].plot()  # 获取标注后的图像

    # 计算帧率
    new_frame_time = time.time()
    time_diff = new_frame_time - prev_frame_time

    if time_diff > 0:
        actual_fps = 1 / time_diff
    else:
        actual_fps = fps  # 使用视频的原始帧率作为初始值

    prev_frame_time = new_frame_time

    # 在图像上叠加帧率信息
    fps_text = f"FPS: {int(actual_fps)}"
    cv2.putText(
        annotated_frame, fps_text, (10, 30), font, 1, (255, 255, 255), 2, cv2.LINE_AA
    )

    # 显示图像
    cv2.imshow("YOLO Prediction", annotated_frame)

    # 按 'q' 键退出
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()


# for result in results:
#     jsonRsult = result.tojson()

#     # 保存 JSON 数据到文件
#     path = "resultBall/data.json"
#     with open(path, "w") as file:
#         file.write(jsonRsult)
