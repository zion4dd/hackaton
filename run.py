import os
from time import time

import cv2
from imageai.Detection import VideoObjectDetection
from PIL import Image

from config import settings
from database import session_
from models import Data

# detection set
detection_timeout = settings.detection_timeout
heap_distance = settings.heap_distance
objectdict = {
    "person": True,
    "truck": True,
    "hat": True,
    # "car": True,
    # "chair": True,
    # "stop_sign": True,
}

model = settings.ImageAImodel
filename = "web_" + str(int(time()))
camera = cv2.VideoCapture(0)


def dist(a, b):
    return abs(((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** (1 / 2))


def save_frame(np_arr):
    img = Image.fromarray(np_arr, "RGB")
    filepath = current_directory + f"\\frames\\frame_{str(int(time()))}.png"
    img.save(filepath)
    return filepath


def forFrame(frame_number, output_array, output_count: dict, frame_detected=None):
    person_count = output_count.get("person", 0)
    truck_count = output_count.get("truck", 0)
    hat_count = output_count.get("hat", 0)

    print(
        f"FRAME: {frame_number} PERSON: {person_count} TRUCK: {truck_count} HAT: {hat_count}"
    )
    print(f"{output_array=}")

    person_list = [
        d.get("box_points")
        for d in output_array
        if d.get("name") == "person" and d.get("box_points")
    ]
    print(f"{person_list=}")

    heap = 1
    while len(person_list) > 1:
        p1 = person_list.pop()
        for p2 in person_list:
            p1xy = p1[0], p1[1]
            p2xy = p2[0], p2[1]
            d = dist(p1xy, p2xy)
            print(f"{d=}")
            if d < heap_distance:
                heap += 1

    print(heap)

    # if output_count.get('stop sign', 0) > 0:
    #     exit()
    frame_url = save_frame(frame_detected)

    data = Data(
        frame_number=frame_number,
        person_count=person_count,
        heap=heap,
        frame_url=frame_url,
    )
    print(f"{data=}")

    with session_() as session:
        session.add(data)
        session.commit()


current_directory = os.getcwd()
print(current_directory)

detector = VideoObjectDetection()

if model == "retinanet_resnet50_fpn_coco-eeacb38b.pth":
    detector.setModelTypeAsRetinaNet()
elif model == "yolov3.pt":
    detector.setModelTypeAsYOLOv3()

detector.setModelPath(os.path.join(current_directory + "\\models", model))
detector.loadModel()
detector.useCPU()

custom = detector.CustomObjects(**objectdict)

detector = detector.detectObjectsFromVideo(
    camera_input=camera,
    custom_objects=custom,
    output_file_path=os.path.join(current_directory + "\\web", filename),
    frames_per_second=20,
    frame_detection_interval=20,
    # log_progress=True,
    minimum_percentage_probability=70,
    per_frame_function=forFrame,
    # per_second_function=forSeconds,
    detection_timeout=detection_timeout,
    display_percentage_probability=False,
    display_object_name=False,
    return_detected_frame=True,
)


# import numpy as np
# def sample():
#     w, h = 512, 512
#     data = np.zeros((h, w, 3), dtype=np.uint8)
#     data[0:256, 0:256] = [255, 0, 0] # red patch in upper left
#     img = Image.fromarray(data)
#     filepath = current_directory + f"\\frames\\frame_{str(int(time()))}.png"
#     img.save(filepath)
#     return filepath
