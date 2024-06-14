import os
from time import time

from imageai.Detection import VideoObjectDetection

# m_tensorflow = "resnet50_coco_best_v2.0.1.h5"
m = "retinanet_resnet50_fpn_coco-eeacb38b.pth"
f = "foo5.mp4"
t = str(int(time()))


def forFrame(frame_number, output_array, output_count: dict):
    print(f"FRAME: {frame_number} PERSON: {output_count.get('person', 0)}")
    # print("FOR FRAME " , frame_number)
    # print("Output for each object : ", output_array)
    # print("Output count for unique objects : ", output_count)
    # print("------------END OF A FRAME --------------")


def forSeconds(second_number, output_arrays, count_arrays, average_output_count):
    for i in count_arrays:
        if "person" in i:
            print(second_number, i.get("person"))
    # print("SECOND : ", second_number)
    # print("Array for the outputs of each frame ", output_arrays)
    # print("Array for output count for unique objects in each frame : ", count_arrays)
    # print("Output average count for unique objects in the last second: ", average_output_count)
    # print("------------END OF A SECOND --------------")


current_directory = os.getcwd()

detector = VideoObjectDetection()
detector.setModelTypeAsRetinaNet()

detector.setModelPath(os.path.join(current_directory + "/models", m))
detector.loadModel()
detector.useCPU()

custom = detector.CustomObjects(person=True)

detector = detector.detectObjectsFromVideo(
    custom_objects=custom,
    input_file_path=os.path.join(current_directory + "/vid", f),
    output_file_path=os.path.join(current_directory + "/vid", f.replace(".mp4", "") + "_" + t),
    frames_per_second=25,
    frame_detection_interval=25,  # 5
    # log_progress=True,
    minimum_percentage_probability=70,
    per_frame_function=forFrame,
    # per_second_function=forSeconds,
)
