from datetime import datetime, timedelta
from io import BytesIO
from PIL import Image
import cv2
import numpy as np
import os
from classes.pyserial_connection_arduino import connect_to_arduino, list_available_ports
from classes.bifurcation_detection import prepare_and_analyze
from yolov5_detect import detect

from classes.scientific_camera import take_raspicampic
try:
    import RPi.GPIO as GPIO
except:
    print("No GPIOs found.")
class Experiment(object):
    def __init__(self, name, scheduler, image_path,
    Camera, experiment_positions = [], interval_minutes = 5):
        self.name = name
        self.experiment_positions = experiment_positions
        self.interval_minutes = interval_minutes
        self.minimal_interval_minutes = 5
        self.current_position = self.planned_position = [0,0,0]
        # list of experiment positions
        # created during the experiment
        self.saved_positions = []
        self.dht_pin = 4
        self.humidity = []
        self.temperature = []
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
        self.moving_time = 6 # standardized time in seconds it takes to move from pos n to n+1 in seconds
        self.flag = False
        self.motor_comport = '/dev/ttyACM0'
        # self.motor_comport = 'COM21'
        self.creation_time = datetime.today()
        self.exp_foldername = f'{self.image_path}/{self.name}'
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

    def record_environment(self):
        self.humidity, self.temperature = 0,0
        import Adafruit_DHT
        self.humidity, self.temperature = 1,1
        DHT_SENSOR = Adafruit_DHT.DHT22
        self.humidity, self.temperature = 2,2
        pin = 4
        self.humidity, self.temperature = 2,3
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, pin)
        self.humidity, self.temperature = humidity, temperature
        try:
            # record humidity and temperature
            print("Environmental data collection..")
            # import os
            # import time
            self.humidity, self.temperature = 0,0
            import Adafruit_DHT
            self.humidity, self.temperature = 1,1
            DHT_SENSOR = Adafruit_DHT.DHT22
            self.humidity, self.temperature = 2,2
            pin = 4
            self.humidity, self.temperature = 2,3
            humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, pin)
            self.humidity, self.temperature = humidity, temperature
            # with open(f"{self.exp_foldername}/environment.csv", "a") as log:
            #     self.humidity, self.temperature = Adafruit_DHT.read_retry(DHT_SENSOR, self.dht_pin)
            #     if self.humidity is not None and self.temperature is not None:                     
            #         log.write('{0},{1},{2:0.1f},{3:0.1f}\r\n'.format(time.strftime('%m/%d/%y'), time.strftime('%H:%M'), self.temperature, self.humidity))
            #         os.sync()
            #         return
            #     else:
            #         print("Failed to retrieve data from environment sensor")
            #         self.humidity, self.temperature = "NaN", "NaN"
            # log.close()
        except:
            print("GPIOs already set or unavailable")
            # self.humidity, self.temperature = "NaN", "NaN"

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
        self.experiment_running = True
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
        task_seperation_increase = self.moving_time*2
        task_seperation = 1
        for xyz_position in self.experiment_positions: 
            print(xyz_position)
            schedule_time_movement = schedule_start + timedelta(seconds=task_seperation)
            schedule_time_picture = schedule_start + timedelta(seconds=self.moving_time+task_seperation)
            self.scheduler.add_job(func=self.motor_task_creator, trigger='date', run_date=schedule_time_movement, args=[xyz_position], id='move_start'+str(xyz_position))
            print(f"created moving job {xyz_position} running at {schedule_time_movement}")
            self.scheduler.add_job(func=self.picture_task_creator, trigger='date', run_date=schedule_time_picture, args=[xyz_position], id='picture_start'+str(xyz_position))
            print(f"created picture job {xyz_position} running at {schedule_time_picture}")
            task_seperation = task_seperation + task_seperation_increase
        # last scheduled picture time is stored
        self.minimal_interval_minutes = schedule_time_picture
        idle_time = self.minimal_interval_minutes-schedule_start
        print(f"Time for one experiment: {idle_time}")
        print(f"Set interval time: {self.interval_minutes}")
        print(f"Set interval time in minutes: {timedelta(minutes=self.interval_minutes)}")
        if(idle_time <= timedelta(minutes=self.interval_minutes)):
            print(f"Schedule is possible, there is time left in the schedule {self.minimal_interval_minutes}")
        else:
            print("Schedule is impossible, stopping and rescheduling in progress")
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
        video_frame_timepoint = (datetime.now().strftime("%Y%m%d-%H%M%S"))
        # take environmental data and store to csv and experiment
        try:
            self.record_environment()
        except:
            print("No sensor data available")
            self.humidity, self.temperature = "NaN", "NaN"
        print(f"Environmental data: {self.humidity}, {self.temperature}")
        if(self.experiment_running and not self.custom_img):
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
            
        file_in_foldername = f'{self.image_path}/{self.name}/{self.raw_dir}/{filename}'
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
        cv2.imwrite(file_in_foldername, RGB_img)
        print(f"image written {file_in_foldername}")
        # self.Camera().set_resolution(new_resolution)
        # create new position with image
        self.saved_positions.append(Position(self.name, self.current_position,
        self.exp_foldername, self.raw_dir, self.skeleton_dir,
        self.yolo_dir, filename, img_mode, file_in_foldername,
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
            results = np.array(connect_to_arduino(self.motor_comport, 0, 0, self.planned_position[0], 0, 0, self.planned_position[1], 0, 0, self.planned_position[2]))
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
    def __init__(self, name, xyz_position, exp_foldername, raw_dir, skeleton_dir, yolo_dir, filename, img_mode, fullpath_raw_image, humidity, temperature):
        self.name = name
        self.position = xyz_position
        self.timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        self.filename = filename
        self.mode = img_mode
        # self.raw_image = RGB_img
        self.exp_foldername = exp_foldername
        # self.fullpath_raw_image = f"{self.exp_foldername}/{self.raw_dir}/{self.filename}"
        self.fullpath_raw_image = fullpath_raw_image
        self.raw_dir = raw_dir
        self.skeleton_dir = skeleton_dir
        self.yolo_dir = yolo_dir
        self.yolo_results = 0
        self.humidity = humidity
        self.temperature = temperature
        # should it take a starting image here?
        # video_frame_timepoint = (datetime.now().strftime("%Y%m%d-%H%M%S"))
        # filename = f'{IMAGEPATH}/het-cam-raw/position{task_position}_{video_frame_timepoint}.jpg'

    # def calculate_yolo(self):
    #     print(f"raw image should be sent to analyze objects")
    #     print(f"Calculating for position {self.name}")
    #     print(type(self.raw_image))
    #     file_in_foldername = f"{self.exp_foldername}/{self.raw_dir}/{self.filename}"
    #     print(file_in_foldername)
    #     detect(file_in_foldername, self.exp_foldername, self.yolo_dir)
        
    def calculate_yolo(self):
        print(f"raw image is sent to detection")
        print(f"Calculating for position {self.name}")
        # print(type(self.raw_image))
        # file_in_foldername = f"{self.exp_foldername}/{self.raw_dir}/{self.filename}"
        # print(file_in_foldername)
        self.yolo_results = detect(self.fullpath_raw_image)
        import pandas
        self.yolo_results_json = self.yolo_results.to_json(orient='records')

        print(f"Detection results {self.yolo_results} stored to position")

        # self.xmin, self.ymin, self.xmax, self.ymax, self.confidence, self.class, self.name = 
        # this should also get bounding boxes and found classes
        print(self.yolo_results)
        # self.xmin, self.ymin, self.xmax, self.ymax, self.confidence, self.class, self.name = results

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

