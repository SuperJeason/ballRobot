import threading
import queue
import time
import cv2
import torch
import json
from ultralytics import YOLO
import analyzePlace
import scoreBasket


# 视频帧生产者线程函数
def frame_producer(cap, frame_queue, stop_event):
    while not stop_event.is_set():
        ret, frame = cap.read()
        if not ret:
            break
        frame_queue.put(frame)  # 将帧放入队列中
        while frame_queue.qsize() > 10 and not stop_event.is_set():
            time.sleep(0.01)  # 控制队列大小，防止内存占用过大
    print("Frame producer 线程退出")
    cap.release()


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


# YOLOv8检测线程函数
def yolov8_detection_thread(detection_result, stop_event):
    model = YOLO("yolov8_ball.pt")
    model.to("cuda" if torch.cuda.is_available() else "cpu")
    cap = cv2.VideoCapture("testData\\test1.mp4")
    cv2.namedWindow("YOLOv8 Detection", cv2.WINDOW_NORMAL)

    frame_queue = queue.Queue(maxsize=10)  # 队列大小为10

    producer_thread = threading.Thread(
        target=frame_producer, args=(cap, frame_queue, stop_event)
    )
    producer_thread.start()

    frame_count = 0
    process_every_n_frames = 1  # 每20帧进行一次处理

    while not stop_event.is_set():
        if not frame_queue.empty():  # 检查队列中是否有帧
            frame = frame_queue.get()  # 从队列中取出帧
            frame_count += 1

            if frame_count % process_every_n_frames == 0:
                results = model(
                    frame, device="cuda" if torch.cuda.is_available() else "cpu"
                )

                annotated_frame = results[0].plot()  # 绘制检测结果
                cv2.imshow("YOLOv8 Detection", annotated_frame)

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    stop_event.set()
                    task_manager.stop_event.set()
                    break

                # 将检测结果转换为JSON格式
                jsonResult = json.loads(results[0].tojson())
                classified_data = analyzePlace.classify_objects(jsonResult)
                mapObjectsBall = analyzePlace.map_objects(classified_data)
                basket_item_count = scoreBasket.showBasket(mapObjectsBall)
                task_id, priority = scoreBasket.choose_target_basket(
                    mapObjectsBall, basket_item_count, "red"
                )

                with lock:  # 更新检测结果
                    detection_result["task_id"] = task_id
                    detection_result["priority"] = priority
            else:
                cv2.imshow("YOLOv8 Detection", frame)  # 显示原始帧
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    stop_event.set()
                    task_manager.stop_event.set()
                    break
        else:
            time.sleep(0.01)

    print("YOLOv8检测线程正在退出")
    cv2.destroyAllWindows()
    producer_thread.join()  # 等待生产者线程结束


# 任务函数（假设定义为全局函数或类方法）
def task_function(interrupt, completed):
    print("正在执行任务：")
    start_time = time.time()
    while not interrupt.is_set() and not task_manager.stop_event.is_set():
        if check_task_completion() or (
            time.time() - start_time > 5
        ):  # 假设5秒后任务完成
            completed.set()
            break
        time.sleep(0.1)
    print("任务完成")


# 示例任务完成检查函数
def check_task_completion():
    return True  # 示例：任务直接完成


# 后置任务处理函数
def post_task_function():
    print("重新返回拿球")


# 任务管理器类
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


# 创建任务对象
def create_task(task_id, priority):
    if task_id == 5:
        task_manager.stop_event.set()
    task_dict = {
        0: Task(f"放在{task_id}框", priority, task_function),
        1: Task(f"放在{task_id}框", priority, task_function),
        2: Task(f"放在{task_id}框", priority, task_function),
        3: Task(f"放在{task_id}框", priority, task_function),
        4: Task(f"放在{task_id}框", priority, task_function),
    }
    return task_dict.get(task_id)


if __name__ == "__main__":
    global task_manager  # 全局变量
    task_manager = TaskManager()
    detection_result = {"task_id": None, "priority": 0}
    yolov8_stop_event = threading.Event()
    lock = threading.Lock()

    yolov8_thread = threading.Thread(
        target=yolov8_detection_thread, args=(detection_result, yolov8_stop_event)
    )
    yolov8_thread.start()

    process_thread = threading.Thread(target=task_manager.process_task)
    process_thread.start()

    # 主线程检查检测结果
    while not task_manager.stop_event.is_set():
        with lock:
            if detection_result["task_id"] is not None:
                new_task = create_task(
                    detection_result["task_id"], detection_result["priority"]
                )
                if new_task:
                    task_manager.check_new_task(new_task)
                detection_result["task_id"] = None  # 清空检测结果
        time.sleep(0.1)
        if yolov8_stop_event.is_set():
            break
    print("主程序正在退出，等待所有线程完成...")
    task_manager.stop_event.set()
    yolov8_stop_event.set()
    yolov8_thread.join()
    process_thread.join()
    print("程序结束")
