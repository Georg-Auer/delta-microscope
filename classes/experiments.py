from datetime import datetime, timedelta
from io import BytesIO
from PIL import Image
import cv2
import numpy as np
import pandas as pd
import os
from classes.pyserial_connection_arduino import connect_to_arduino, list_available_ports
from classes.bifurcation_detection import prepare_and_analyze
from yolov5_detect import detect, bounding_boxes

from classes.scientific_camera import take_raspicampic
try:
    import RPi.GPIO as GPIO
    import board
    import adafruit_dht
except:
    print("No GPIOs and/or sensor found.")
class Experiment(object):
    def __init__(self, name, scheduler, image_path,
    Camera, experiment_positions = [], interval_minutes = 5):
        self.name = name
        self.experiment_positions = experiment_positions
        self.interval_minutes = interval_minutes
        self.minimal_interval_minutes = 5
        self.current_position = self.planned_position = [0,0,0] # does this create a bug?
        # list of experiment positions
        # created during the experiment
        self.saved_positions = []
        try:
            self.sensors = [board.D4, board.D17]
        except:
            self.sensors = []
        try:
            self.dht_pin = self.sensors[0] # board.D4 or: board.D17
        except:
            self.dht_pin = False
        self.humidity = [np.NaN, "none"]
        self.temperature = [np.NaN, "none"]
        self.scheduler = scheduler
        self.image_path = image_path
        self.Camera = Camera
        self.led = True
        self.custom_img = False
        # self.resolution = [1280, 720]
        # self.resolution = [4056, 3040]
        self.resolution = [2592, 1952]
        # self.resolution = [3296, 2464]
        self.x_resolution, self.y_resolution = self.resolution
        self.experiment_running = False
        self.experiment_iteration = 0
        self.motor_speed = 10000
        # for tracking:
        # self.real_world_ratio_x = #how many x-ticks are one screen width
        # self.real_world_ratio_y = #how many x-ticks are one screen height
        self.moving_time = 14 # standardized time in seconds it takes to move from pos n to n+1 in seconds
        self.flag = False
        self.motor_comport = '/dev/ttyACM0'
        # self.motor_comport = 'COM9'
        self.creation_time = datetime.today()
        self.exp_foldername = f'{self.image_path}/{self.name}'
        self.detection_class = 0
        self.confidence_threshold = 0.5
        self.raw_dir = "microscope-raw"
        self.skeleton_dir = "microscope-skeleton"
        self.yolo_dir = "microscope-yolo"
        self.img_variant_folders = [self.raw_dir,self.skeleton_dir,self.yolo_dir]
        self.create_directories()
        self.switch_led()

    # def show_timeframe(self):
    #     print(f"Time between imaging in experiment {self.name} set to {self.time_between} minutes")

    def switch_led(self):
        if(self.led == True):
            #if True, switch on
            try:
                GPIO.setwarnings(False)
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(18, GPIO.OUT)
                # setting blue led to on
                GPIO.output(18, GPIO.HIGH)
            except:
                print("GPIOs already set or unavailable")
                self.led = False

        else:
            #if False, switch off
            try:
                GPIO.setwarnings(False)
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(18, GPIO.OUT)
                # setting blue led to on
                GPIO.output(18, GPIO.LOW)
            except:
                print("GPIOs already set or unavailable")

    def record_environment(self, video_frame_timepoint):
        # emtpy list for new record, important because each sensor appends the list by a list
        self.humidity = []
        self.temperature = []
        # if self.sensors = [], do nothing
        print(self.sensors)
        for dht_pin in self.sensors:
            print(f"Selecting pin: {dht_pin}")
            try:
                self.dht_pin = dht_pin
                # record humidity and temperature
                # https://learn.adafruit.com/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging/python-setup
                print(f"Environmental data collection on pin {self.dht_pin}..")
                # sudo pip3 install adafruit-circuitpython-dht
                # sudo apt install libgpiod2 # this may or may not be needed
                dhtDevice = adafruit_dht.DHT22(self.dht_pin, use_pulseio=False)
                # self.humidity, self.temperature = [dhtDevice.humidity, self.dht_pin], [dhtDevice.temperature, self.dht_pin]
        
                self.humidity.append([dhtDevice.humidity, self.dht_pin])
                self.temperature.append([dhtDevice.temperature, self.dht_pin])

                if(self.experiment_running):
                    with open(f"{self.exp_foldername}/environment.csv", "a") as log:
                        if self.humidity is not None and self.temperature is not None:                     
                            # log.write('{0},{1},{2:0.1f},{3:0.1f}\r\n'.format(time.strftime('%m-%d-%y'), time.strftime('%H:%M:%S'), self.temperature, self.humidity))
                            log.write(f"{video_frame_timepoint}, {self.dht_pin}, {self.temperature[0]}, {self.humidity[0]}\r\n")
                            # log.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), self.temperature, self.humidity)
                            # print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                            os.sync()
                            log.close()
                        else:
                            print("Failed to retrieve data from environment sensor")
                            self.humidity, self.temperature = np.NaN, np.NaN
                            log.write(f"{video_frame_timepoint}, {self.temperature}, {self.humidity}\r\n")
                            os.sync()
                            log.close()
                else:
                    print("No recording of environment data outside of running experiment.")
                # log.close()

            except:
                print(f"No sensor data for sensor {dht_pin} available")
                # append for each sensor value
                self.humidity.append([np.NaN, dht_pin])
                self.temperature.append([np.NaN, dht_pin])
        else:
            print("No active sensors to record data")

    def show_experiment_positions(self):
        n = 0
        return_string = []
        for xyz_positions in self.experiment_positions:
            print(f"Position {n}, x = {xyz_positions[0]}, y = {xyz_positions[1]} z = {xyz_positions[2]}")
            return_string.append(f"Position {n}, x = {xyz_positions[0]}, y = {xyz_positions[1]} z = {xyz_positions[2]}\n")
            n += 1
        print(return_string)
        # return f"These are all planned positions\n {self.experiment_positions} of experiment {self.name}"
        # return f"These are all planned positions\n {return_string}"
        return return_string

        
    def remove_experiment_positions(self):
        print("Removing all planned positions")
        self.experiment_positions = []
    def add_current_experiment_position(self):
        print(f"Adding current position {self.current_position}")
        self.experiment_positions.append(self.current_position)
        print("These are all planned positions")
        print(self.experiment_positions)

    def save_position(self):
        # gives Position the name of the experiment and the current position
        print("Save position")
        print(self.name, self.current_position)
        # should the Camera be given to the Position????????????????
        # self.saved_positions.append(Position(self.name, self.current_position, self.Camera))
        self.saved_positions.append(Position(self.name, self.current_position))
        # take image!!!!!!!!
    
    def show_saved_positions(self):
        print(f"Saved Positions: {self.saved_positions}")
    
    # tasking
    def start_experiment(self):
        print("Starting experiment")
        self.experiment_iteration = 0
        # try:
        #     self.Camera().set_resolution(self.resolution)
        #     print(f"Resolution set to {self.resolution} for automated pictures")
        # except:
        #     print("Resolution could not be set for experiment")

        # for element in self.experiment_positions:
        #     self.saved_positions.append(Position(self.name, self.experiment_positions))
        schedule_start = datetime.today()
        
        print(f"Moving time is assumed {self.moving_time} seconds") 

        # task_seperation is the accumulated time of moving to the previous position + 1 s times the previous positions
        task_seperation_increase = self.moving_time+1
        task_seperation = 0
        print(f"Task seperation increase time is assumed {task_seperation_increase} seconds") 
        print(f"Task seperation time is assumed {task_seperation} seconds") 
        for xyz_position in self.experiment_positions: 
            print(xyz_position)
            schedule_time_movement = schedule_start + timedelta(seconds=task_seperation)
            schedule_time_picture = schedule_start + timedelta(seconds=self.moving_time+task_seperation)
            self.scheduler.add_job(func=self.motor_task_creator, trigger='date', run_date=schedule_time_movement, args=[xyz_position], id='move_start'+str(xyz_position))
            print(f"created moving job {xyz_position} running at {schedule_time_movement}")
            self.scheduler.add_job(func=self.picture_task_creator, trigger='date', run_date=schedule_time_picture, args=[xyz_position], id='picture_start'+str(xyz_position))
            print(f"created picture job {xyz_position} running at {schedule_time_picture}")
            task_seperation = task_seperation + task_seperation_increase
            print(f"Task seperation increase time is {task_seperation} seconds") 

        # last scheduled picture time is stored
        try:
            # if no schedule_time_picture is set, there might be 0 positions
            self.minimal_interval_minutes = schedule_time_picture
        except:
            print("No Positions to start")
            self.stop_experiment()
            return
        idle_time = self.minimal_interval_minutes-schedule_start
        print(f"Time for one experiment: {idle_time}")
        # print(f"Set interval time: {self.interval_minutes}")
        print(f"Set interval time in minutes: {timedelta(minutes=self.interval_minutes)}")
        if(idle_time <= timedelta(minutes=self.interval_minutes)):
            print(f"Schedule is possible, there is time left in the schedule ({timedelta(minutes=self.interval_minutes)-idle_time})")
            self.experiment_running = True
        else:
            print(f"Schedule is impossible: {idle_time-timedelta(minutes=self.interval_minutes)} missing; stopping and rescheduling in progress")
            self.stop_experiment()
            # now add the time that was missing to the interval time and schedule again
            print(f"self.minimal_interval_minutes {self.minimal_interval_minutes} self.interval_minutes {(self.interval_minutes)} idle_time {(abs(idle_time))}")
            idle_time = (abs(idle_time.seconds) % 3600) // 60
            print(idle_time)
            print(idle_time+1)
            self.interval_minutes = idle_time+1
            print(f"Interval time was increased to {self.interval_minutes} minutes")
            self.start_experiment()

    def stop_experiment(self):
        print("Stopping experiment")
        print(f"Stopped in iteration {self.experiment_iteration:04}")
        print(self.scheduler.get_jobs())
        print("Removing all scheduled jobs")
        # self.scheduler.remove_job(j0)
        self.scheduler.remove_all_jobs()
        print(self.scheduler.get_jobs())
        # print("Setting lower resolution for webstream")
        # new_resolution = [640, 480]
        # self.Camera().set_resolution(new_resolution)
        self.experiment_running = False

    def motor_task_creator(self, task_id):
        # creating motor task that runs every minute
        # self.planned_position = task_id
        # print(f"start of motor task creator {self.planned_position}")
        print(f"start of motor task creator {task_id}")
        self.scheduler.add_job(func=self.motor_task, trigger='interval', minutes=self.interval_minutes, args=[task_id], id='move'+str(task_id))
        # scheduler.add_job(func=motor_task, trigger='interval', minutes=interval_minutes, args=[task_id], id='move'+str(task_id))

    def picture_task_creator(self, task_id):
        print(f"start of picture task creator {task_id}")
        # creating picture task that runs every minute
        self.scheduler.add_job(func=self.picture_task, trigger='interval', minutes=self.interval_minutes, id='picture'+str(task_id))

    def picture_task(self):
        print(f"task: start to take picture {self.current_position}")
        # use webcam?
        frame = self.Camera().get_frame()
        video_frame_timepoint = (datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        # take environmental data and store to csv and experiment

        print(f"Environmental data: {self.humidity}, {self.temperature}")
        if(self.experiment_running and not self.custom_img):
            print(self.dht_pin)
            print(self.sensors)
            self.record_environment(video_frame_timepoint)
            filename = f'position{self.current_position}_i{self.experiment_iteration:04}_{video_frame_timepoint}.jpg'
            self.experiment_iteration = self.experiment_iteration + 1
            img_mode = "automatic"
            # if auto mode is enabled, switch led off after image
            self.led = False
        else:
            filename = f'position{self.current_position}_custom_image_{video_frame_timepoint}.jpg'
            img_mode = "custom"
            # now reset the custom image tag
            self.custom_img = False
            
        raw_file_in_foldername = f'{self.image_path}/{self.name}/{self.raw_dir}/{filename}'
        # https://picamera.readthedocs.io/en/release-1.13/recipes1.html
        # https://picamera.readthedocs.io/en/release-1.13/recipes2.html
        # https://picamera.readthedocs.io/en/release-1.13/fov.html#sensor-modes
        gif_bytes_io = BytesIO()
        gif_bytes_io.write(frame)
        image = Image.open(gif_bytes_io)
        open_cv_image = np.array(image)
        RGB_img = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2RGB)

        # try:
        #     camera.close()
        #     print("camera closed")
        # except:
        #     print("camera was not open")

        # try:
        #     from picamera import PiCamera
        #     from picamera.array import PiRGBArray
        #     import time
        #     camera = PiCamera()
        # except:
        #     print("camera was not closed last time or is still in use")
        #     #camera.close()
        #     #rawCapture.close()

        # print("Raspberry Camera loaded")
        # camera.resolution = (self.x_resolution, self.y_resolution)
        # camera.framerate = 32
        # camera.exposure_mode = 'sports'
        # if the iso is set, pictures will look more similar
        # camera.iso = 400
        # camera.shutter_speed = 1000

        # camera.brightness = 50 #(0 to 100)
        # camera.sharpness = 0 #(-100 to 100)
        # camera.contrast = 0 #(-100 to 100)
        # camera.saturation = 0 #(-100 to 100

        #camera.vflip = True
        # alternative rawCapture = PiRGBArray(camera)
        # rawCapture = PiRGBArray(camera, size=(self.x_resolution, self.y_resolution))
        # allow the camera to warmup

        # camera.resolution = (self.x_resolution, self.y_resolution)
        # camera.framerate = 24
        # time.sleep(2)
        # image = np.empty((self.y_resolution * self.x_resolution * 3,), dtype=np.uint8)
        # camera.capture(image, 'bgr')
        # image = image.reshape((self.y_resolution, self.x_resolution, 3))
        # # camera.capture(rawCapture, format="rgb")
        # # RGB_img = rawCapture.array
        # camera.close()
        # # rawCapture.close() #is this even possible?
        # # for testing only
        # # cv2.imshow('image',RGB_img)
        # # cv2.waitKey(0)
        cv2.imwrite(raw_file_in_foldername, RGB_img)
        print(f"image written {raw_file_in_foldername}")
        # self.Camera().set_resolution(new_resolution)
        # create new position with image
        self.saved_positions.append(Position(self.name, self.current_position,
        self.exp_foldername, self.raw_dir, self.skeleton_dir, self.yolo_dir, 
        self.detection_class, self.confidence_threshold,
        filename, img_mode, raw_file_in_foldername,
        self.humidity, self.temperature))
        self.switch_led()

    def create_directories(self):
        for variant in self.img_variant_folders:
            foldername = f'{self.exp_foldername}/{variant}/'
            # Create target Directory if don't exist
            if not os.path.exists(foldername):
                os.makedirs(foldername) # also creates non-existant intermediaries
                print("Directory " , foldername ,  " Created ")
            else:    
                print("Directory " , foldername ,  " already exists")

    def calculate_yolos(self):
        for position in self.saved_positions:
            position.calculate_yolo()

    # def motor_task(task_id):
    #     # send to motor position
    #     print(f"task: moving to position {task_id}")
    #     motor_position(task_id)

    # def motor_position(position_in_degree):
    #     print(f"motor_position {position_in_degree}")
    #     # 4800 steps are 270°, 360 should never be possible since = 0°
    #     # degrees are divided by 90 and multiplied by 1600
    #     # only send int values to arduino!
    #     step_position_arduino = int(position_in_degree/90*1600)
    #     print(f"Sending: {step_position_arduino} steps")
    #     try:
    #         results = np.array(connect_to_arduino(comport,motor0_enable,motor0_direction,step_position_arduino,
    #             motor1_enable,motor1_direction,motor1_position,motor2_enable,motor2_direction,motor2_position,motor3_enable,motor3_direction,motor3_position))
    #         print(f"Received values: {results}")
    #     except:
    #         print("Microcontroller not found or not connected")
    #         return
    def motor_task(self, task_id):
        # send to motor position
        print(f"task: moving to position {task_id}")
        self.planned_position = task_id
        self.motor_position()

    def motor_position(self):
        # never move in darkness
        self.led = True
        self.switch_led()
        # position_in_degree = self.planned_position
        print(f"planned_position {self.planned_position}")
        # xyz_position = self.planned_position
        # print(f"xyz_position {xyz_position}")
        # print(f"xyz_position {xyz_position[0]}")
        # print(f"xyz_position {xyz_position[1]}")
        # print(f"xyz_position {xyz_position[2]}")

        # x_position, y_position, z_position = xyz_position
        # print(f"x_position, y_position, z_position {x_position, y_position, z_position}")

        # 4800 steps are 270°, 360 should never be possible since = 0°
        # degrees are divided by 90 and multiplied by 1600
        # only send int values to arduino!
        # step_position_arduino = int(position_in_degree/90*1600)
        # print(f"Sending: {x_position, y_position, z_position}")
        # print(f"types: {type(x_position), type(y_position), type(z_position)}")
        try:
            # results = np.array(connect_to_arduino(comport = '/dev/ttyACM0',motor0_enable,motor0_direction,step_position_arduino,
            #     motor1_enable,motor1_direction,motor1_position,motor2_enable,motor2_direction,motor2_position,motor3_enable,motor3_direction,motor3_position))
            # enabled = 0, disabled = 1; 0 = counterclockwise 1 = clockwise
            # results = np.array(connect_to_arduino(self.motor_comport, 0, 0, x_position, 0, 0, y_position, 0, 0, z_position))
            results = np.array(connect_to_arduino(self.motor_comport, 0, 0, self.planned_position[0], self.motor_speed, 0, 0, self.planned_position[1], self.motor_speed, 0, 0, self.planned_position[2], self.motor_speed))
            print(f"Received values: {results}")
            # this could be parsed and converted to degree
            # or just assume motor has moved to destination
            self.current_position = self.planned_position
            # print(type(results))
            # print(f"Current position: {self.current_position}")
            # self.current_position = results[4],results[7],results[10]
            print(f"Current position: {self.current_position}")
        except:
            print("Microcontroller not found or not connected")
            print("Setting position to 0, 0, 0")
            self.current_position = [0,0,0]
            return
class Position(object):
    # raw_image, skeletal_image,
    # feature_bifurcations, feature_endings, yolo_image, yolo_classes,
    # yolo_coordinates, yolo_poi_circles, features_bifurcations_poi, feature_endings_poi
    def __init__(self, name, xyz_position, exp_foldername, raw_dir, skeleton_dir, yolo_dir, detection_class, confidence_threshold, filename, img_mode, fullpath_raw_image, humidity, temperature):
        self.name = name
        self.position = xyz_position
        self.timestamp = (datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.filename = filename
        self.mode = img_mode
        # self.raw_image = RGB_img
        self.exp_foldername = exp_foldername
        # self.fullpath_raw_image = f"{self.exp_foldername}/{self.raw_dir}/{self.filename}"
        self.fullpath_raw_image = fullpath_raw_image
        self.raw_dir = raw_dir
        self.skeleton_dir = skeleton_dir
        self.yolo_dir = yolo_dir
        # self.yolo_results = 0 # better: no variable at start
        self.detection_class = detection_class
        self.confidence_threshold = confidence_threshold
        # self.center_yolo_object
        self.humidity = humidity
        self.temperature = temperature
        # should it take a starting image here?
        # video_frame_timepoint = (datetime.now().strftime("%Y%m%d-%H%M%S"))
        # filename = f'{IMAGEPATH}/het-cam-raw/position{task_position}_{video_frame_timepoint}.jpg'
 
    def calculate_yolo(self):
        print(f"raw image is sent to detection")
        print(f"Calculating for position {self.filename}")
        print(f"Calculating for position {self.fullpath_raw_image}")
        # print(type(self.raw_image))
        # raw_file_in_foldername = f"{self.exp_foldername}/{self.raw_dir}/{self.filename}"
        # print(raw_file_in_foldername)

        self.yolo_results = detect(self.fullpath_raw_image, self.detection_class, self.confidence_threshold)
        try:
            yolo_image, self.yolo_results, self.yolo_results_json = bounding_boxes(self.yolo_results, self.fullpath_raw_image)
        except Exception as e:
            print(f"{e} \n No objects could be detected, returning None..")
            return

        # raw_file_in_foldername = f"{self.exp_foldername}/{self.raw_dir}/{self.filename}"
        yolo_file_in_foldername = f'{self.exp_foldername}/{self.yolo_dir}/{self.filename}'
        print(yolo_file_in_foldername)
        cv2.imwrite(yolo_file_in_foldername, yolo_image)

        print(f"Detection results {self.yolo_results} stored to position {self.name}")

        self.yolo_results = pd.DataFrame(self.yolo_results.pandas().xywhn[0])
        print(self.yolo_results['confidence'].argmax())
        element = self.yolo_results['confidence'].argmax()
        print(self.yolo_results.iloc[element])
        print(self.yolo_results.at[element, "xcenter"])
        print(self.yolo_results.at[element, "ycenter"])
        print(self.yolo_results.at[element, "confidence"])

        # gets the relative xy center of the object with the highest confidence
        self.center_yolo_object = [self.yolo_results.at[element, "xcenter"], self.yolo_results.at[element, "ycenter"], self.yolo_results.at[element, "confidence"]]

if __name__ == '__main__':

    cells = Experiment("Nr. 1", [1000, 2000, 0], 5)
    print(cells.experiment_positions)

    cells.show_experiment_positions()
    cells.add_experiment_positions(2000, 3000, 1000)
    cells.show_experiment_positions()
    cells.remove_experiment_positions()
    cells.show_experiment_positions()

    cells.start_experiment()
    print("was started")
    cells.stop_experiment()
    # test_position = Position("test", 270)
    # print(test_position.name)
    # print(test_position.timestamp)
#---------------------------------------------------------

