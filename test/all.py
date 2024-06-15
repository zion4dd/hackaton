import os

from imageai.Detection import ObjectDetection

current_directory = os.getcwd()

detector = ObjectDetection()
detector.setModelTypeAsRetinaNet()

detector.setModelPath(os.path.join(current_directory, "resnet50_coco_best_v2.0.1.h5"))
detector.loadModel()

detections = detector.detectObjectsFromImage(
    input_image=os.path.join(current_directory, "traffic.jpg"),
    output_image_path=os.path.join(current_directory, "traffic_detected.jpg"),
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
