import time

from celery import shared_task

from judge.models import DrivingImage, SafetyScore

import cv2
import numpy as np

DARKNET_PATH = "D:/Develop/Darknet/darknet/build/darknet/x64/"


def lerp(a, b, t):
    return a + (b - a) * t


def inv_lerp(a, b, v):
    return (v - a) / (b - a)


def clamp01(v):
    return max(min(v, 1.0), 0.0)


@shared_task
def judge_image(pk):
    record = DrivingImage.objects.get(pk=pk)
    image = record.image

    st = time.time()

    net = cv2.dnn.readNet(DARKNET_PATH + "yolov3.weights", DARKNET_PATH + "yolov3.cfg")
    classes = []
    with open(DARKNET_PATH + "data/coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    colors = np.random.uniform(0, 255, size=(len(classes), 3))

    cv_img = cv2.imdecode(np.fromstring(image.read(), np.uint8), cv2.IMREAD_UNCHANGED)
    height, width, _ = cv_img.shape

    blob = cv2.dnn.blobFromImage(cv_img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            if classes[class_id] != "person":
                continue
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.3, 0.4)

    max_speed = 25
    target_speed = max_speed

    # 매우매우 휴리스틱한 판정 알고리즘..

    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            if h / height < 0.2:
                continue
            rate = clamp01(inv_lerp(0.2, 0.6, h / height))
            cx = (x + w / 2) / width
            if x < 0.33:
                rate *= lerp(0.75, 1.0, cx * (1 / 0.33))
            elif x > 0.67:
                rate *= lerp(1.0, 0.75, (1 - cx) * (1 / 0.33))

            spd = lerp(1.0, 0.4, rate) * max_speed
            target_speed = min(target_speed, spd)

    print(str(indexes.size) + " Person(s) Found!")
    print("Maximum Speed: " + str(target_speed))
    print("Execution Time: " + str(time.time() - st) + "s.")

    safety_rate = inv_lerp(target_speed + 5, target_speed, record.speed)

    score = SafetyScore(drive=record.drive, score=safety_rate)
    score.save()

    """
    font = cv2.FONT_HERSHEY_PLAIN
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            color = colors[i]
            cv2.rectangle(cv_img, (x, y), (x + w, y + h), color, 2)
    cv2.putText(cv_img, "Target Speed = " + str(target_speed) + "km/h", (0, 30), font, 3, [0, 255, 0], 2)
    cv2.imshow("Image", cv_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    """

