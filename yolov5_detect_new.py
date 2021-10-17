import cv2
import torch
from PIL import Image

# Model
# model = torch.hub.load('yolov5', 'yolov5s')
model = torch.hub.load('yolov5', 'custom', path='yolov5weights/spheroids.pt', source='local')  # local repo

# Images
# for f in ['spheroids1.jpg']:
#     torch.hub.download_url_to_file('https://ultralytics.com/images/' + f, f)  # download 2 images
img1 = Image.open('spheroids2.jpg')  # PIL image
img2 = cv2.imread('spheroids1.jpg')[..., ::-1]  # OpenCV image (BGR to RGB)
imgs = [img1, img2]  # batch of images

model.conf = 0.6  # confidence threshold (0-1)
# model.iou = 0.45  # NMS IoU threshold (0-1)
# class 0 is for spheroid detection only:
# model.classes = None  # (optional list) filter by class, i.e. = [0, 15, 16] for persons, cats and dogs

# Inference
# results = model(imgs, size=640)  # includes NMS
results = model(imgs, size=416)  # includes NMS

# Results
results.print()  
# results.save()  # or .show()
results.show()
# print("1")
# print(results.xyxy)
# print("2")
# print(results.xyxy[0])  # img1 predictions (tensor)
# print("3")
print(results.pandas().xyxy[0])  # img1 predictions (pandas)
#          xmin        ymin        xmax        ymax  confidence  class      name
# 0  496.221252  242.118607  599.258057  344.487427    0.788762      0  spheroid
# 1  136.804352  206.301865  261.107330  331.260986    0.722638      0  spheroid
# 2   75.455215    0.000000  184.007217   83.206726    0.674978      0  spheroid
# 3  191.439102  404.267792  281.820465  480.000000    0.592858      0  spheroid
# 4  501.906982    3.391178  640.000000  158.920624    0.514878      0  spheroid

#--------------------------------------------------------------------

