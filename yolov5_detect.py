# python detect.py --weights yolov5s.pt --img-size 416 --conf 0.4 --source inference/images/bus.jpg
# python yolov5/detect.py --weights yolov5weights/wells.pt --img-size 416 --conf 0.5 --save-crop --source ./yolov5/well-detection.v1-wells-only.yolov5pytorch/train/images
# python yolov5/detect.py --weights yolov5weights/wells.pt --img-size 416 --conf 0.5 --save-crop --source F:\spoc-images\hfob-saos0411\microscope-raw
# F:\spoc-images\hfob-saos0411\microscope-raw
import cv2
import torch
import logging
# import pandas as pd

# def detect(raw_image_foldername, exp_foldername, yolo_dir):
def detect(file_in_foldername, detection_class = False, confidence_threshold = 0.6):
    logging.debug(f"Parameters for detection: \n detection_class: {detection_class}, confidence_threshold: {confidence_threshold}")
    # model = torch.hub.load('yolov5', 'custom', path='weights/hetcam.pt', source='local')  # local repo
    model = torch.hub.load('yolov5', 'custom', path='yolov5weights/wells.pt', source='local')  # local repo
    
    model.conf = confidence_threshold  # confidence threshold (0-1)
    # model.iou = 0.45  # NMS IoU threshold (0-1)
    # class 0 is for spheroid detection only:
    if detection_class is not False:
        logging.debug(f"Detection specified to class {detection_class}")
        model.classes = detection_class
    else:
        logging.debug("Detection not specified, all classes considered..")
    # model.classes = None  # (optional list) filter by class, i.e. = [0, 15, 16] for persons, cats and dogs
    
    image = cv2.imread(file_in_foldername)[..., ::-1]  # OpenCV image (BGR to RGB)
    results = model(image, size=416)  # includes NMS
    results.logging.debug()
    # logging.debug(results.xyxy)
    # result2 = pd.DataFrame()
    # https://github.com/ultralytics/yolov5/issues/2703
    # pandaresult = results.pandas().xyxy[0]  # image predictions (pandas)
    # logging.debug(f"xyxy\n{pandaresult}")
    # pandaresult = results.pandas().xyxyn[0]
    
    logging.debug(f"xyxy\n{results.pandas().xyxyn[0]}")

    return results.pandas()

def bounding_boxes(yolo_results, fullpath_raw_image):
    image = cv2.imread(fullpath_raw_image)
    # df.shape[0] == 0 # this is faster than checking if empty
    # logging.debug(f"yolo_results: {type(yolo_results.pandas().xyxyn[0])}")
    logging.debug(f"yolo_results: {yolo_results.xyxyn[0]}")
    if yolo_results.xyxyn[0].empty:
        return image, image, False
        # return image, crop_img, yolo_results_xyxyn_json
    else:
        logging.debug("Dataframe not empty, continuing..")
    yolo_results_xyxyn = yolo_results.xyxyn[0]
    yolo_results_xywhn = yolo_results.xywhn[0]
    yolo_results_xyxy = yolo_results.xyxy[0]
    # logging.debug(f"xyxyn result:{yolo_results_xyxyn}")
    # logging.debug(f"xywhn result:{yolo_results_xywhn}")
    logging.debug(type(yolo_results_xyxyn))
    yolo_results_xyxyn_json = yolo_results_xyxyn.to_json(orient='records')

    if len(yolo_results_xyxyn) == 0:
        logging.debug ("No objects found")
    
    else:
        logging.debug (yolo_results_xyxyn)
        logging.debug (yolo_results_xyxyn.shape)
        logging.debug ("Number of objects detected: " + str(yolo_results_xyxyn.shape[0]))
    
        arr = yolo_results_xyxyn.to_numpy()
        logging.debug("results in array")
        logging.debug(arr)
        # logging.debug(image)
        logging.debug(image.shape)

        logging.debug("Sorting by confidence, creating a cropped image")
        logging.debug(yolo_results_xyxy)
        element = yolo_results_xyxy['confidence'].argmax()
        logging.debug(yolo_results_xyxy.iloc[element])
        xmin = yolo_results_xyxy.at[element, "xmin"]
        xmax = yolo_results_xyxy.at[element, "xmax"]
        ymin = yolo_results_xyxy.at[element, "ymin"]
        ymax = yolo_results_xyxy.at[element, "ymax"]
        logging.debug(ymin,ymax, xmin,xmax)
        crop_img = image[round(ymin):round(ymax), round(xmin):round(xmax)]
        # cv2.imshow("cropped", crop_img)
        # cv2.waitKey(0)

        i = 0
        for (y1,x1,y2,x2,n,m,o) in arr:
            x2 = int(x2*480)
            y2 = int(y2*640)
            logging.debug(x2)
            logging.debug(y2)
            y1 = int(y1*640)
            x1 = int(x1*480)
            logging.debug(f"width {x1}")
            logging.debug(f"height {y1}")
            logging.debug(f"probability {n}")
            logging.debug(f"class {m}")
            logging.debug(f"class name {o}")
            thickness = 2
            cv2.rectangle(image, (int(y1), int(x1)), (int(y2), int(x2)), ((n*255), (n*255), 255), thickness)
            # https://www.geeksforgeeks.org/python-opencv-cv2-circle-method/
            w = int((y2-y1)/2)
            w2 = int((x2-x1)/2)
            center_coordinates = (int(y1+w),int(x1+w2))
            logging.debug(center_coordinates)
            color = (0, 191, 0)
            cv2.circle(image, center_coordinates, int((w+w2)/2), color, thickness)
            i = i+1
        return image, crop_img, yolo_results_xyxyn_json

# https://stackoverflow.com/questions/15589517/how-to-crop-an-image-in-opencv-using-python
# def bounding_box_crop(image, yolo_results_xywhn):
#     # import cv2
#     logging.debug(yolo_results_xywhn)

#     crop_img = image[y:y+h, x:x+w]
#     cv2.imshow("cropped", crop_img)
#     cv2.waitKey(0)
#     return crop_img

if __name__ == '__main__':
    detection_class = 0
    confidence_threshold = 0.7
    image = cv2.imread("spheroids2.jpg")
    yolo_results = detect("spheroids2.jpg", detection_class, confidence_threshold)
    # yolo_results = detect("spheroids2.jpg")
    # image = cv2.imread("het-cam-ha-small.jpg")
    # yolo_results = detect("het-cam-ha-small.jpg")
    image, yolo_results, yolo_results_xyxyn_json = bounding_boxes(yolo_results, "spheroids2.jpg")
    try:
        logging.debug(yolo_results.pandas().xywhn[0])
        logging.debug(yolo_results.pandas().xywhn)
    except:
        logging.debug(yolo_results)
    cv2.imshow("resulting image",image)
    cv2.waitKey(0)

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
#     # logging.debug('Original Dimensions : ',img1.shape)
#     # width = 640
#     # height = 640
#     # dim = (width, height)
#     # img1 = cv2.resize(img1, dim, interpolation = cv2.INTER_AREA)
#     # logging.debug('Resized Dimensions : ',img1.shape)

#     # Inference
#     # results = model(img1, size=640)  # includes NMS
#     results = model(img1, size=640)  # includes NMS
#     # results = model(img1, size=320)  # includes NMS

#     # Results
#     results.logging.debug()  
#     # results.show()  # or .show()
#     # results.save()  # or .show()

#     result1 = results.xyxy[0]  # img1 predictions (tensor)
#     result2 = results.pandas().xyxy[0]  # img1 predictions (pandas)

#     # logging.debug(result1)
#     logging.debug(result2)
#     #      xmin    ymin    xmax   ymax  confidence  class    name
#     # 0  749.50   43.50  1148.0  704.5    0.874023      0  person
#     # 1  433.50  433.50   517.5  714.5    0.687988     27     tie
#     # 2  114.75  195.75  1095.0  708.0    0.624512      0  person
#     # 3  986.00  304.00  1028.0  420.0    0.286865     27     tie


