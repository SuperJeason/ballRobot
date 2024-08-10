import threading
import time
import cv2
from ultralytics import YOLO
import analyzePlace
import scoreBasket
import json


# 任务类
class Task:
    def __init__(self, name, priority, task_function):
        self.name = name
        self.priority = priority
        self.task_function = task_function
        self.interrupt = threading.Event()
        self.completed = threading.Event()

    def run(self):
        self.task_function(self.interrupt, self.completed)
        if self.completed.is_set():
            post_task_function()  # 调用任务完成后的处理函数


# 任务管理器定义
class TaskManager:
    def __init__(self):
        self.current_task = None
        self.task_lock = threading.Lock()
        self.stop_event = threading.Event()

    def process_task(self):
        while not self.stop_event.is_set():
            with self.task_lock:
                if self.current_task:
                    print(f"开始执行任务: {self.current_task.name}")
                    self.current_task.run()
                    if self.current_task.completed.is_set():
                        print(f"任务完成: {self.current_task.name}")
                        self.current_task = None
                    else:
                        print(f"任务中断: {self.current_task.name}")
                        self.current_task = None
                else:
                    time.sleep(0.1)

    def check_new_task(self, new_task):
        with self.task_lock:
            if not self.current_task or new_task.priority > self.current_task.priority:
                if self.current_task:
                    print(
                        f"发现更高优先级任务: {new_task.name}，中断当前任务: {self.current_task.name}"
                    )
                    self.current_task.interrupt.set()  # 中断当前任务
                self.current_task = new_task
                return True
        return False


# YOLOv8检测线程函数
def yolov8_detection_thread(detection_result, stop_event):
    model = YOLO("yolov8_ball.pt")
    cap = cv2.VideoCapture(0)

    while not stop_event.is_set():
        ret, frame = cap.read()
        if not ret:
            continue

        task_id, priority = detect_task_from_frame(frame, model)
        if task_id:
            detection_result["task_id"] = task_id
            detection_result["priority"] = priority
        time.sleep(0.1)  # 控制检测频率

    cap.release()

    # 测试Demo
    # frame = cv2.imread("testData\\test2.JPG")
    # task_id, priority = detect_task_from_frame(frame, model)
    # if task_id:
    #     detection_result["task_id"] = task_id
    #     detection_result["priority"] = priority
    # time.sleep(0.1)  # 控制检测频率
    # task_manager.stop_event.set()

# 根据检测结果返回任务标志位
def detect_task_from_frame(frame, model):

    # 定义自己阵营
    myTeam = "red"
    results = model(frame)
    jsonRsult = json.loads((results[0].tojson()))
    classified_data = analyzePlace.classify_objects(jsonRsult)
    mapObjectsBall = analyzePlace.map_objects(classified_data)
    basket_item_count = scoreBasket.showBasket(mapObjectsBall)
    task_id, priority = scoreBasket.choose_target_basket(
        mapObjectsBall, basket_item_count, myTeam
    )
    return task_id, priority


# 根据标志位创建任务
def create_task(task_id, priority):
    task_dict = {
        0: Task(f"放在{task_id}框", priority, task_function),
        1: Task(f"放在{task_id}框", priority, task_function),
        2: Task(f"放在{task_id}框", priority, task_function),
        3: Task(f"放在{task_id}框", priority, task_function),
        4: Task(f"放在{task_id}框", priority, task_function),
        5: Task(f"任务结束，本次无需放球", priority, task_function),
    }
    return task_dict.get(task_id)


# 任务函数
def task_function(interrupt, completed):
    print("正在执行任务：")
    while not interrupt.is_set():
        # 这里添加状态检查逻辑来确定任务是否完成
        if check_task_completion():
            completed.set()  # 标记任务完成
            return
        time.sleep(0.1)


# 检查任务是否完成的函数
def check_task_completion():
    # 通过一个激光之类的传感器，根据返回值来确定任务是否完成，若完成了则返回ture
    return True


def post_task_function():
    print("重新返回拿球")


if __name__ == "__main__":
    task_manager = TaskManager()
    detection_result = {"task_id": None, "priority": 0}
    yolov8_stop_event = threading.Event()

    # 启动YOLOv8检测线程
    yolov8_thread = threading.Thread(
        target=yolov8_detection_thread, args=(detection_result, yolov8_stop_event)
    )
    yolov8_thread.start()

    # 启动任务检测线程
    process_thread = threading.Thread(target=task_manager.process_task)
    process_thread.start()

    # 主线程检查检测结果
    while not task_manager.stop_event.is_set():
        if detection_result["task_id"] is not None:
            new_task = create_task(
                detection_result["task_id"], detection_result["priority"]
            )
            if new_task:
                task_manager.check_new_task(new_task)
            detection_result["task_id"] = None  # 清空检测结果
        time.sleep(0.2)

    # 停止所有线程
    task_manager.stop_event.set()
    yolov8_stop_event.set()
    yolov8_thread.join()
    process_thread.join()

    print("程序结束")
