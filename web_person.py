import os
from time import time

import cv2
from imageai.Detection import VideoObjectDetection

camera = cv2.VideoCapture(0)

filename = "web_" + str(int(time()))

objectdict = {
    "person": True,
    "truck": True,
    # "car": True,
    # "hat": True,
    # "chair": True,
    # "stop_sign": True,
}


def dist(a, b):
    return abs(((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** (1 / 2))


def forFrame(frame_number, output_array, output_count: dict):
    print(
        f"FRAME: {frame_number} PERSON: {output_count.get('person', 0)} TRUCK: {output_count.get('truck', 0)}"
    )
    print(f"{output_array=}")

    person_list = [
        d.get("box_points")
        for d in output_array
        if d.get("name") == "person" and d.get("box_points")
    ]
    print(f"{person_list=}")

    heap = 0
    while len(person_list) > 1:
        p1 = person_list.pop()
        for p2 in person_list:
            p1xy = p1[0], p1[1]
            p2xy = p2[0], p2[1]
            d = dist(p1xy, p2xy)
            print(f"{d=}")
            if d < 200:
                heap += 1

    print(heap + 1)

    # if output_count.get('stop sign', 0) > 0:
    #     exit()


current_directory = os.getcwd()
print(current_directory)

detector = VideoObjectDetection()

detector.setModelTypeAsRetinaNet()
m = "retinanet_resnet50_fpn_coco-eeacb38b.pth"
# detector.setModelTypeAsYOLOv3()
# m = "yolov3.pt"

detector.setModelPath(os.path.join(current_directory + "/models", m))
detector.loadModel()
detector.useCPU()

custom = detector.CustomObjects(**objectdict)

detector = detector.detectObjectsFromVideo(
    camera_input=camera,
    custom_objects=custom,
    output_file_path=os.path.join(current_directory + "/web", filename),
    frames_per_second=25,
    frame_detection_interval=25,  # 5
    # log_progress=True,
    minimum_percentage_probability=70,
    per_frame_function=forFrame,
    # per_second_function=forSeconds,
    detection_timeout=4,
    # display_percentage_probability=False,
    # display_object_name=False,
)


"""
FRAME: 225 PERSON: 1
[{'name': 'person', 'percentage_probability': 96.65, 'box_points': [68, 150, 627, 470]}]
FRAME: 250 PERSON: 1
[{'name': 'person', 'percentage_probability': 95.89, 'box_points': [77, 125, 618, 470]}]
"""
