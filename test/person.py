import os

from imageai.Detection import ObjectDetection

# m_tensorflow = "resnet50_coco_best_v2.0.1.h5"
m = "retinanet_resnet50_fpn_coco-eeacb38b.pth"

current_directory = os.getcwd()

detector = ObjectDetection()
detector.setModelTypeAsRetinaNet()

detector.setModelPath(os.path.join(current_directory, m))
detector.loadModel()

custom = detector.CustomObjects(person=True)

detections = detector.detectObjectsFromImage(
    custom_objects=custom,
    input_image=os.path.join(current_directory, "p2.jpg"),
    output_image_path=os.path.join(current_directory, "traffic_detected.jpg"),
    minimum_percentage_probability=70,
)

for eachObject in detections:
    print(
        eachObject["name"],
        " : ",
        eachObject["percentage_probability"],
        " : ",
        eachObject["box_points"],
    )
print("--------------------------------")
