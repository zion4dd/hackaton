import os
from time import time

import cv2
from imageai.Detection import VideoObjectDetection

camera = cv2.VideoCapture(0)


w = "web"
t = str(int(time()))


objectdict = {
    "person": True,
    # "truck": True,
    # "car": True,
    "hat": True,
}


def forFrame(frame_number, output_array, output_count: dict):
    print(f"FRAME: {frame_number} PERSON: {output_count.get('person', 0)} HAT: {output_count.get('hat', 0)}")
    print(output_array)


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
    output_file_path=os.path.join(current_directory + "/web", f"{w}_{t}"),
    frames_per_second=25,
    frame_detection_interval=25,  # 5
    # log_progress=True,
    minimum_percentage_probability=70,
    per_frame_function=forFrame,
    # per_second_function=forSeconds,
    detection_timeout=30,
    # display_percentage_probability=False,
    # display_object_name=False,
)


"""
FRAME: 225 PERSON: 1
[{'name': 'person', 'percentage_probability': 96.65, 'box_points': [68, 150, 627, 470]}]
FRAME: 250 PERSON: 1
[{'name': 'person', 'percentage_probability': 95.89, 'box_points': [77, 125, 618, 470]}]
FRAME: 275 PERSON: 1
[{'name': 'person', 'percentage_probability': 97.29, 'box_points': [122, 118, 615, 471]}]
FRAME: 300 PERSON: 1
[{'name': 'person', 'percentage_probability': 97.37, 'box_points': [129, 121, 613, 471]}]
FRAME: 325 PERSON: 1
[{'name': 'person', 'percentage_probability': 94.85, 'box_points': [31, 124, 621, 473]}]
"""
