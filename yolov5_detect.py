import cv2
import torch
# import pandas as pd

# def detect(raw_image_foldername, exp_foldername, yolo_dir):
def detect(file_in_foldername, detection_class = False, confidence_threshold = 0.6):
    # model = torch.hub.load('yolov5', 'custom', path='weights/hetcam.pt', source='local')  # local repo
    model = torch.hub.load('yolov5', 'custom', path='yolov5weights/spheroids.pt', source='local')  # local repo
    
    model.conf = confidence_threshold  # confidence threshold (0-1)
    # model.iou = 0.45  # NMS IoU threshold (0-1)
    # class 0 is for spheroid detection only:
    if detection_class:
        print(f"Detection specified to class {detection_class}")
        model.classes = detection_class
    else:
        print("Detection no specified, all classes considered..")
    # model.classes = None  # (optional list) filter by class, i.e. = [0, 15, 16] for persons, cats and dogs
    
    image = cv2.imread(file_in_foldername)[..., ::-1]  # OpenCV image (BGR to RGB)
    results = model(image, size=416)  # includes NMS
    results.print()
    # print(results.xyxy)
    # result2 = pd.DataFrame()
    # https://github.com/ultralytics/yolov5/issues/2703
    # pandaresult = results.pandas().xyxy[0]  # image predictions (pandas)
    # print(f"xyxy\n{pandaresult}")
    # pandaresult = results.pandas().xyxyn[0]
    
    print(f"xyxy\n{results.pandas().xyxyn[0]}")
    # pandaresult = results.pandas().xywhn[0]
    # print(f"xywhn\n{pandaresult}")
    # print(result2)
    # print(type(result2))
    # print(result2.sort_values("confidence",ascending=True))
    # print(result2.head(1))
    # result2 = pd.DataFrame(results.pandas().xyxy[0])  # image predictions (pandas)
    # print(result2)
    return results

def bounding_boxes(yolo_results, fullpath_raw_image):
    image = cv2.imread(fullpath_raw_image)
    yolo_results_xyxyn = yolo_results.pandas().xyxyn[0]
    yolo_results_xywhn = yolo_results.pandas().xywhn[0]
    print(f"xyxyn result:{yolo_results_xyxyn}")
    print(f"xywhn result:{yolo_results_xywhn}")
    print(type(yolo_results_xyxyn))
    yolo_results_xyxyn_json = yolo_results_xyxyn.to_json(orient='records')

    if len(yolo_results_xyxyn) == 0:
        print ("No objects found")
    
    else:
        print (yolo_results_xyxyn)
        print (yolo_results_xyxyn.shape)
        print ("Number of objects detected: " + str(yolo_results_xyxyn.shape[0]))
    
        arr = yolo_results_xyxyn.to_numpy()
        print("results in array")
        print(arr)
        # print(image)
        print(image.shape)
        i = 0
        for (y1,x1,y2,x2,n,m,o) in arr:
            x2 = int(x2*480)
            y2 = int(y2*640)
            print(x2)
            print(y2)
            y1 = int(y1*640)
            x1 = int(x1*480)
            print(f"width {x1}")
            print(f"height {y1}")
            print(f"probability {n}")
            print(f"class {m}")
            print(f"class name {o}")

            thickness = 2

            cv2.rectangle(image, (int(y1), int(x1)), (int(y2), int(x2)), ((n*255), (n*255), 255), thickness)
            # https://www.geeksforgeeks.org/python-opencv-cv2-circle-method/
            w = int((y2-y1)/2)
            w2 = int((x2-x1)/2)
            center_coordinates = (int(y1+w),int(x1+w2))
            print(center_coordinates)
            color = (0, 191, 0)
            cv2.circle(image, center_coordinates, int((w+w2)/2), color, thickness)
            i = i+1
        return image, yolo_results, yolo_results_xyxyn_json



if __name__ == '__main__':
    detection_class = 0
    confidence_threshold = 0.5
    image = cv2.imread("spheroids2.jpg")
    # yolo_results = detect("spheroids2.jpg", detection_class, confidence_threshold)
    yolo_results = detect("spheroids2.jpg")
    # image = cv2.imread("het-cam-ha-small.jpg")
    # yolo_results = detect("het-cam-ha-small.jpg")
    image, yolo_results, yolo_results_xyxyn_json = bounding_boxes(yolo_results)
    print(yolo_results.pandas().xywhn[0])
    print(yolo_results.pandas().xywhn)
    # cv2.imshow("resulting image",image)
    # cv2.waitKey(0)

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


