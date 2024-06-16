import os
from time import time

import cv2
from imageai.Detection import VideoObjectDetection
from PIL import Image
from sqlalchemy import select

from config import settings
from database import session_
from firebase import FireBase as FB
from models import Data, FireBase

# detection set
detection_timeout = 5
heap_distance = 300
heap_limit = 3

objectdict = {
    "person": True,
    "truck": True,
    "hat": True,
    # "car": True,
    # "chair": True,
    # "stop_sign": True,
}

model = settings.ImageAImodel
current_directory = os.getcwd()
filename = "web_" + str(int(time()))
camera = cv2.VideoCapture(0)
firebase = FB()


def dist(a, b):
    return abs(((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** (1 / 2))


def save_frame(np_arr) -> tuple:
    img = Image.fromarray(np_arr, "RGB")
    datetime = int(time())
    filename = f"frame_{datetime}.png"
    filepath = current_directory + "\\frames\\" + filename
    img.save(filepath)
    return filename, datetime


def forFrame(frame_number, output_array, output_count: dict, frame_detected=None):
    if output_count.get("stop sign"):
        exit()

    person_count = output_count.get("person", 0)
    truck_count = output_count.get("truck", 0)
    hat_count = output_count.get("hat", 0)

    print(
        f"{frame_number} PERSON: {person_count} | TRUCK: {truck_count} | HAT: {hat_count}"
    )
    print(f"{output_array=}")

    person_list = [
        d.get("box_points")
        for d in output_array
        if d.get("name") == "person" and d.get("box_points")
    ]
    # print(f"{person_list=}")

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
    print(f"{heap=}")
    frame_url, datetime = save_frame(frame_detected)

    data = Data(
        frame_number=frame_number,
        person_count=person_count,
        heap=heap,
        frame_url=frame_url,
        datetime=datetime,
    )
    # print(f"{data=}")

    with session_() as session:
        session.add(data)
        session.commit()

        if heap >= heap_limit:
            stmt = select(FireBase.token).where(FireBase.name == settings.FBConsumer)
            token = session.execute(stmt).scalars().first()
            if token:
                firebase.push(
                    registration_id=token,
                    body="Скопление рабочих на стройплощадке",
                )


def run():
    detector = VideoObjectDetection()

    if model == "retinanet_resnet50_fpn_coco-eeacb38b.pth":
        detector.setModelTypeAsRetinaNet()
    elif model == "yolov3.pt":
        detector.setModelTypeAsYOLOv3()
    else:
        print("unknown model")
        exit()

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


if __name__ == "__main__":
    run()
