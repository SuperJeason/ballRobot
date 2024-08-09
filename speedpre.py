import cv2

from ultralytics import YOLO, solutions

model = YOLO("model/yolov8x.pt")
names = model.model.names

cap = cv2.VideoCapture("testData\\testCar.gif")
w, h, fps = (
    int(cap.get(x))
    for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS)
)
video_writer = cv2.VideoWriter(
    "speed_estimation.avi", cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h)
)

# Initialize SpeedEstimator
speed_obj = solutions.SpeedEstimator(
    reg_pts=[(0, 360), (1280, 360)],
    names=names,
    view_img=True,
)

while cap.isOpened():
    success, im0 = cap.read()
    if not success:
        break
    tracks = model.track(im0, persist=True, show=False)
    im0 = speed_obj.estimate_speed(im0, tracks)
    video_writer.write(im0)

cap.release()
video_writer.release()
cv2.destroyAllWindows()
