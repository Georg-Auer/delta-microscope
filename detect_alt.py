import cv2
import torch

# def detect(raw_image_foldername, exp_foldername, yolo_dir):
def detect():
    model = torch.hub.load('yolov5/', 'custom', path='weights/best.pt', source='local')  # local repo
    img1 = cv2.imread('het-cam-test.jpg')  # OpenCV image (BGR to RGB)
    results = model(img1, size=640)  # includes NMS
    results.print()  
    result2 = results.pandas().xyxy[0]  # img1 predictions (pandas)
    print(result2)

if __name__ == '__main__':
    detect()

# if __name__ == '__main__':
        
#     # load Model
#     # model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
#     # model = torch.hub.load('ultralytics/yolov5', 'yolov5s', classes=10)
#     # model = torch.hub.load('path/to/yolov5', 'custom', path='path/to/best.pt', source='local')  # local repo
#     model = torch.hub.load('yolov5/', 'custom', path='weights/best.pt', source='local')  # local repo
#     # Images
#     # from PIL import Image
#     # img1 = Image.open('het-cam-test.jpg')  # PIL image

#     # img2 = img1
#     img1 = cv2.imread('het-cam-test.jpg')  # OpenCV image (BGR to RGB)
#     # imgs = [img1, img2]  # batch of images

#     # resize image
#     # print('Original Dimensions : ',img1.shape)
#     # width = 640
#     # height = 640
#     # dim = (width, height)
#     # img1 = cv2.resize(img1, dim, interpolation = cv2.INTER_AREA)
#     # print('Resized Dimensions : ',img1.shape)

#     # Inference
#     # results = model(img1, size=640)  # includes NMS
#     results = model(img1, size=640)  # includes NMS
#     # results = model(img1, size=320)  # includes NMS

#     # Results
#     results.print()  
#     # results.show()  # or .show()
#     # results.save()  # or .show()

#     result1 = results.xyxy[0]  # img1 predictions (tensor)
#     result2 = results.pandas().xyxy[0]  # img1 predictions (pandas)

#     # print(result1)
#     print(result2)
#     #      xmin    ymin    xmax   ymax  confidence  class    name
#     # 0  749.50   43.50  1148.0  704.5    0.874023      0  person
#     # 1  433.50  433.50   517.5  714.5    0.687988     27     tie
#     # 2  114.75  195.75  1095.0  708.0    0.624512      0  person
#     # 3  986.00  304.00  1028.0  420.0    0.286865     27     tie


