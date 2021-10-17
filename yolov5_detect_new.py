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
img2 = cv2.imread('spheroids2.jpg')[..., ::-1]  # OpenCV image (BGR to RGB)
imgs = [img1, img2]  # batch of images

# Inference
# results = model(imgs, size=640)  # includes NMS
results = model(imgs, size=416)  # includes NMS

# Results
results.print()  
results.save()  # or .show()

results.xyxy[0]  # img1 predictions (tensor)
results.pandas().xyxy[0]  # img1 predictions (pandas)
#      xmin    ymin    xmax   ymax  confidence  class    name
# 0  749.50   43.50  1148.0  704.5    0.874023      0  person
# 1  433.50  433.50   517.5  714.5    0.687988     27     tie
# 2  114.75  195.75  1095.0  708.0    0.624512      0  person
# 3  986.00  304.00  1028.0  420.0    0.286865     27     tie

#--------------------------------------------------------------------


# import torch

# # Model
# model = torch.hub.load('/yolov5', 'yolov5weights/spheroids', source='local')

# # Image
# img = 'spheroids1.jpg'

# # Inference
# results = model(img)

# results.pandas().xyxy[0]

#      xmin    ymin    xmax   ymax  confidence  class    name
# 0  749.50   43.50  1148.0  704.5    0.874023      0  person
# 1  433.50  433.50   517.5  714.5    0.687988     27     tie
# 2  114.75  195.75  1095.0  708.0    0.624512      0  person
# 3  986.00  304.00  1028.0  420.0    0.286865     27     tie


# import cv2
# import torch
# # import pandas as pd

# # def detect(raw_image_foldername, exp_foldername, yolo_dir):
# def detect(file_in_foldername):
#     # model = torch.hub.load('yolov5/', 'custom', path='weights/hetcam.pt', source='local')  # local repo
#     model = torch.hub.load('yolov5/', 'custom', path='weights/spheroids.pt', source='local')  # local repo
#     image = cv2.imread(file_in_foldername)  # OpenCV image (BGR to RGB)
#     results = model(image, size=416)  # includes NMS
#     results.print()
#     # print(results.xyxy)
#     # result2 = pd.DataFrame()
#     # https://github.com/ultralytics/yolov5/issues/2703
#     # pandaresult = results.pandas().xyxy[0]  # image predictions (pandas)
#     # print(f"xyxy\n{pandaresult}")
#     pandaresult = results.pandas().xyxyn[0]
#     print(f"xyxy\n{pandaresult}")
#     # pandaresult = results.pandas().xywhn[0]
#     # print(f"xywhn\n{pandaresult}")
#     # print(result2)
#     # print(type(result2))
#     # print(result2.sort_values("confidence",ascending=True))
#     # print(result2.head(1))
#     # result2 = pd.DataFrame(results.pandas().xyxy[0])  # image predictions (pandas)
#     # print(result2)
#     return pandaresult

# if __name__ == '__main__':

#     image = cv2.imread("spheroids2.jpg")
#     yolo_results = detect("spheroids2.jpg")
#     # image = cv2.imread("het-cam-ha-small.jpg")
#     # yolo_results = detect("het-cam-ha-small.jpg")
#     print(yolo_results)
#     print(type(yolo_results))
#     yolo_results_json = yolo_results.to_json(orient='records')

#     if len(yolo_results) == 0:
#         print ("No objects found")
    
#     else:
#         print (yolo_results)
#         print (yolo_results.shape)
#         print ("Number of objects detected: " + str(yolo_results.shape[0]))
    
#         arr = yolo_results.to_numpy()
#         print(arr)
#         print(image)
#         print(image.shape)
#         i = 0
#         for (h,w,y,x,n,m,o) in arr:
#             x = int(x*640)
#             y = int(y*480)
#             print(x)
#             print(y)
#             w = int(w*640)
#             print(w)
#             h = int(h*480)
#             print(h)
#             print(n)
#             print(m)
#             print(o)
#             # resize image
#             # dim = (416, 416)
#             # image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

#             cv2.rectangle(image, (int(x), int(y)), (int(w), int(h)), ((i*40), (i*40), 255), 1)
            
#             # cv2.rectangle(image, (int(w), int(h)), (int(x), int(y)), (0, (i*40), 255-(i*40)), 1)
#             # cv2.rectangle(image, (int(w), int(h)), (int(x+(h*0.5)), int(y+(w*0.5))), (0, (i*40), 255-(i*40)), 1)

#             i = i+1
#             # cv2.rectangle(image,x,y,(x+w,y+h),(0,255,0),1)

#         # resize image
#         # dim = (416, 416)
#         # resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

#         # cv2.rectangle(image, (50, 100), (10, 10), (255, 255, 255), 1)
#         # cv2.rectangle(resized, (50, 100), (10, 10), (255, 255, 255), 1)
#         cv2.imshow("resulting image",image)
#         # cv2.imshow("resized image",resized)
#         cv2.waitKey(0)

# # if __name__ == '__main__':
        
# #     # load Model
# #     # model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
# #     # model = torch.hub.load('ultralytics/yolov5', 'yolov5s', classes=10)
# #     # model = torch.hub.load('path/to/yolov5', 'custom', path='path/to/best.pt', source='local')  # local repo
# #     model = torch.hub.load('yolov5/', 'custom', path='weights/best.pt', source='local')  # local repo
# #     # Images
# #     # from PIL import Image
# #     # img1 = Image.open('het-cam-test.jpg')  # PIL image

# #     # img2 = img1
# #     img1 = cv2.imread('het-cam-test.jpg')  # OpenCV image (BGR to RGB)
# #     # imgs = [img1, img2]  # batch of images

# #     # resize image
# #     # print('Original Dimensions : ',img1.shape)
# #     # width = 640
# #     # height = 640
# #     # dim = (width, height)
# #     # img1 = cv2.resize(img1, dim, interpolation = cv2.INTER_AREA)
# #     # print('Resized Dimensions : ',img1.shape)

# #     # Inference
# #     # results = model(img1, size=640)  # includes NMS
# #     results = model(img1, size=640)  # includes NMS
# #     # results = model(img1, size=320)  # includes NMS

# #     # Results
# #     results.print()  
# #     # results.show()  # or .show()
# #     # results.save()  # or .show()

# #     result1 = results.xyxy[0]  # img1 predictions (tensor)
# #     result2 = results.pandas().xyxy[0]  # img1 predictions (pandas)

# #     # print(result1)
# #     print(result2)
# #     #      xmin    ymin    xmax   ymax  confidence  class    name
# #     # 0  749.50   43.50  1148.0  704.5    0.874023      0  person
# #     # 1  433.50  433.50   517.5  714.5    0.687988     27     tie
# #     # 2  114.75  195.75  1095.0  708.0    0.624512      0  person
# #     # 3  986.00  304.00  1028.0  420.0    0.286865     27     tie


