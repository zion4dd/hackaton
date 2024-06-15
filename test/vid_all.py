import os

from imageai.Detection import VideoObjectDetection

current_directory = os.getcwd()

detector = VideoObjectDetection()
detector.setModelTypeAsRetinaNet()

detector.setModelPath(os.path.join(current_directory, "resnet50_coco_best_v2.0.1.h5"))
detector.loadModel()

detections = detector.detectObjectsFromVideo(
    input_file_path=os.path.join(current_directory, "footage.mp4"),
    output_file_path=os.path.join(current_directory, "footage_detected"),
    frames_per_second=20,
    log_progress=True,
)
