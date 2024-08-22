import threading
import cv2
import torch
import json
from ultralytics import YOLO
import analyzePlace
import scoreBasket
import time


# YOLOv8检测和任务处理函数
def process_video():
    model = YOLO("yolov8_ball.pt")
    model.to("cuda" if torch.cuda.is_available() else "cpu")
    cap = cv2.VideoCapture("testData\\test1.mp4")

    frame_count = 0
    process_every_n_frames = 1  # 每1帧进行一次处理

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        if frame_count % process_every_n_frames == 0:
            results = model(
                frame, device="cuda" if torch.cuda.is_available() else "cpu"
            )

            annotated_frame = results[0].plot()

            height, width, channels = annotated_frame.shape
            new_width = 800
            new_height = int(height * (new_width / width))
            resized_frame = cv2.resize(annotated_frame, (new_width, new_height))

            cv2.imshow("YOLOv8 Detection", resized_frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

            jsonResult = json.loads(results[0].tojson())
            classified_data = analyzePlace.classify_objects(jsonResult)
            mapObjectsBall = analyzePlace.map_objects(classified_data)
            basket_item_count = scoreBasket.showBasket(mapObjectsBall)
            task_id, priority = scoreBasket.choose_target_basket(
                mapObjectsBall, basket_item_count, "red"
            )

            # 执行任务逻辑
            if task_id is not None:
                task = create_task(task_id, priority)
                print(f"开始执行任务: {task.name}")
                task.run()
                print(f"任务完成: {task.name}")

        else:
            cv2.imshow("YOLOv8 Detection", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        time.sleep(0.01)  # 控制处理速度

    print("视频处理完成")
    cap.release()
    cv2.destroyAllWindows()


# 任务函数（假设定义为全局函数或类方法）
def task_function(interrupt, completed):
    print("正在执行任务")
    print("任务完成")
    completed.set()


# 示例任务完成检查函数
def check_task_completion():
    return True  # 示例：任务直接完成


# 后置任务处理函数
def post_task_function():
    print("重新返回拿球")


# 创建任务对象
def create_task(task_id, priority):
    task_dict = {
        0: Task(f"放在{task_id}框", priority, task_function),
        1: Task(f"放在{task_id}框", priority, task_function),
        2: Task(f"放在{task_id}框", priority, task_function),
        3: Task(f"放在{task_id}框", priority, task_function),
        4: Task(f"放在{task_id}框", priority, task_function),
    }
    return task_dict.get(task_id)


class Task:
    def __init__(self, name, priority, task_function):
        self.name = name
        self.priority = priority
        self.task_function = task_function
        self.interrupt = threading.Event()  # 用于中断任务
        self.completed = threading.Event()  # 用于标记任务完成

    def run(self):
        self.task_function(self.interrupt, self.completed)
        if self.completed.is_set():
            post_task_function()  # 调用任务完成后的处理函数


if __name__ == "__main__":
    process_video()
    print("程序结束")
