# -*- encoding: utf-8 -*-
"""
start with: sudo CAMERA=opencv python3 run.py
"""

from classes.pyserial_connection_arduino import list_available_ports
from flask_migrate import Migrate
from os import environ
from sys import exit
from decouple import config
import logging

from config import config_dict
from app import create_app, db

#from old camera app-----------------------------------------------------------------

from importlib import import_module
import os
from flask import Flask, render_template, url_for, Response

# import camera driver
if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    from camera import Camera

# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera

# for saving bytestream
# https://stackoverflow.com/questions/29330570/how-to-open-a-simple-image-using-streams-in-pillow-python
# https://stackoverflow.com/questions/14134892/convert-image-from-pil-to-opencv-format
from PIL import Image
from io import BytesIO

# classes experiment & position
from classes.experiments import Position, Experiment

# gallery
from flask import request, redirect, send_from_directory
from werkzeug.utils import secure_filename
# gallery end

# import old 
import time
import os
import numpy as np
from flask_apscheduler import APScheduler
import cv2
from datetime import datetime, timedelta
# import old end
# https://stackoverflow.com/questions/6871016/adding-days-to-a-date-in-python
#-----------------------------------------------------------------------------------

# WARNING: Don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'

try:
    # Load the configuration using the default values 
    app_config = config_dict[get_config_mode.capitalize()]

except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

app = create_app( app_config ) 
Migrate(app, db)

# https://stackoverflow.com/questions/5208252/ziplist1-list2-in-jinja2
app.jinja_env.filters['zip'] = zip

if DEBUG:
    app.logger.info('DEBUG       = ' + str(DEBUG)      )
    app.logger.info('Environment = ' + get_config_mode )
    app.logger.info('DBMS        = ' + app_config.SQLALCHEMY_DATABASE_URI )

# constant for saving images, used by camera and gallery
# IMAGEPATH = "app\\base\\static\\upload"
IMAGEPATH = "app/base/static/upload"

# scheduler set up:
class Config(object):
    SCHEDULER_API_ENABLED = True
app.config.from_object(Config())

scheduler = APScheduler()
# if you don't wanna use a config, you can set options here:
# scheduler.api_enabled = True
scheduler.init_app(app)
scheduler.start()

INTERVAL = 5 # experiment time in minutes
EXPERIMENT_NAME = "default"
# EXPERIMENT_POSITIONS = [[0, 0, 0],[0, 10000, 0],[10000, 0, 0],[10000, 10000, 0]]
EXPERIMENT_POSITIONS = []
DATABASE = []

@app.route('/')
@app.route('/index')
def index():
    """Video streaming home page."""
    # return render_template('index.html', images=images)
    current_experiment = select_flagged_experiment()
    return render_template("index.html", segment="index", experiment_name = current_experiment.name)
    # return render_template('index.html')
    

def gen(camera):
    current_experiment = select_flagged_experiment()
    print(f"Current experiment name(s): {current_experiment.name}")
    """Video streaming generator function."""
    # global global_video_frame
    # global global_video_frame_timepoint
    while True:
        frame_enc = camera.get_frame()

        # global_video_frame = frame_enc
        # global_video_frame_timepoint = (datetime.now().strftime("%Y%m%d-%H%M%S"))
        # print(f"frame{global_video_frame_timepoint}")

        # object_methods = [method_name for method_name in dir(camera)
        #     if callable(getattr(camera, method_name))]
        # print(object_methods)

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_enc + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# buttons

@app.route('/move_deg')
def move_deg():
    xyz_position = [0, 0, 0]
    xyz_position = request.args.getlist('xyz_position', type=int)

    # needs to be readjusted for x y
    # if(xyz_position >= 280):
    #     xyz_position = 270
    # if(xyz_position <= -90):
    #     xyz_position = -90

    print(f"Moving to {xyz_position}")
    current_experiment = select_flagged_experiment()
    print(f"Current experiment name(s): {current_experiment.name}")
    # it should be possible to add to the planned position, not the current
    # otherwise, movement has to be finished to send another
    current_experiment.planned_position = [x + y for x, y in zip(current_experiment.planned_position, xyz_position)]

    current_experiment.motor_position()
    return '''<h1>Moving to: {}</h1>'''.format(xyz_position)
    # return ("nothing")

#-------------------------------------------------------------------------------------

@app.route('/get_toggled_status') 
def toggled_status():
    current_status = request.args.get('status')
    if(scheduler.get_jobs()):
        print(bool(scheduler.get_jobs()))
        print("jobs scheduled")
        # current_status = 'Automatic On'
    else:
        print(bool(scheduler.get_jobs()))
        print("no jobs scheduled")
    #     current_status = 'Automatic On'

    # create dummy experiment for now
    # new_experiment = Experiment(EXPERIMENT_NAME, scheduler, IMAGEPATH, Camera, [0, 90, 180, 270], INTERVAL)
    current_experiment = select_flagged_experiment()
    print(f"Current experiment name(s): {current_experiment.name}")
    # if Automatic On was sent and no jobs are scheduled
    if(current_status == 'Automatic Off') and not(scheduler.get_jobs()):
        print("Switching On")
        print(current_experiment.experiment_positions)
        current_experiment.show_experiment_positions()
        # start dummy experiment for now
        current_experiment.start_experiment()
        if(current_experiment.experiment_running):
            print("Experiment was started")
        else:
            print("Experiment could not be started")

    else:
        print("Switching Off")
        print(scheduler.get_jobs())
        print("Removing all scheduled jobs")
        current_experiment.stop_experiment()
        if(current_experiment.experiment_running == False):
            print("Experiment was stopped")
        else:
            print("Experiment could not be stopped")

    return 'Automatic On' if current_status == 'Automatic Off' else 'Automatic Off'

@app.route('/picture')
def picture():
    current_experiment = select_flagged_experiment()
    current_experiment.custom_img = True
    current_experiment.picture_task()
    print(f"Picture saved in Experiment: {current_experiment.name}")
    print(f"There are {len(current_experiment.saved_positions)} saved positions")
    print(f"Created at {current_experiment.saved_positions[-1].timestamp}")
    # this should return all saved positions, would help the user immensely
    return ("nothing")

@app.route('/led')
def led():
    # toggle led on button press
    current_experiment = select_flagged_experiment()
    current_experiment.custom_img = True
    if(current_experiment.led == True):
        current_experiment.led = False
    else:
        current_experiment.led = True
    current_experiment.switch_led()
    return ("nothing")

# buttons, scheduler end

#code gallery
# images could be sent directly:
# https://stackoverflow.com/questions/56946969/how-to-send-an-image-directly-from-flask-server-to-html

@app.route("/gallery")
def show_gallery():
    current_experiment = select_flagged_experiment()
    print(f"Current experiment name(s): {current_experiment.name}")
    raw_image_foldername = f'{current_experiment.image_path}/{current_experiment.name}/{current_experiment.raw_dir}/'
    raw_image_list = os.listdir(raw_image_foldername)
    print(raw_image_list)
    foldername_gallery = f'{current_experiment.name}/{current_experiment.raw_dir}/'
    return render_template("gallery.html", segment="gallery", experiment_name = current_experiment.name, 
    image_foldername = foldername_gallery, images = raw_image_list)

@app.route("/gallery-yolo")
def show_yolo():
    current_experiment = select_flagged_experiment()
    print(f"Current experiment name(s): {current_experiment.name}")
    current_experiment.calculate_yolos()

    yolo_image_foldername = f'{current_experiment.image_path}/{current_experiment.name}/{current_experiment.yolo_dir}/'
    yolo_image_list = os.listdir(yolo_image_foldername)
    print(yolo_image_list)
    foldername_gallery = f'{current_experiment.name}/{current_experiment.yolo_dir}/'

    # return render_template("gallery.html", saved_positions = current_experiment.saved_positions, image_foldername = foldername_gallery,
    # experiment_name = current_experiment.name, images = yolo_image_list)
    return render_template("gallery.html", segment="gallery-yolo", saved_positions = current_experiment.saved_positions, image_foldername = foldername_gallery,
    experiment_name = current_experiment.name, images = yolo_image_list)

@app.route("/environment")
def show_environment():
    current_experiment = select_flagged_experiment()
    print(f"Current experiment name(s): {current_experiment.name}")
    table_output = []
    # this needs to be changed for two sensors
    for position in current_experiment.saved_positions:
        table_output.append(f"Environment data for {position.name} @{position.timestamp} {position.humidity} % humidity, {position.temperature} °C")
    print(f"table_output: {table_output}")
    import pandas as pd
    import seaborn as sns
    import matplotlib
    # to avoid X11 errors, use Agg rendering engine:
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib import dates

    data_output = []
    # for position in current_experiment.saved_positions:
    #     for sensordata in position.humidity:
    #         print(f"sensordata: {sensordata}")
    #         print(f"position.humidity: {position.humidity[0][0]}")
    #         print(f"position.temperature: {position.temperature}")
    #         print(f"position.humidity: {position.humidity[0][0]}")
    #         print(f"position.temperature: {position.temperature}")
    #         data_line = position.name, position.timestamp, position.humidity[0], position.humidity[1], position.temperature[0], position.temperature[1]
    #         data_output.append(data_line)
# table_output: ['Environment data for sens2 @2021-10-19 20:30:38 [[71.6, 4], [70.1, 17]] % humidity, [[13.5, 4], [13.6, 17]] °C', 'Environment data for sens2 @2021-10-19 20:31:38 [[71.5, 4], [70.1, 17]] % humidity, [[13.5, 4], [13.6, 17]] °C']
# sensordata: [71.6, 4]
# position.humidity: 71.6
# position.temperature: [[13.5, 4], [13.6, 17]]
# position.humidity: 71.6
# position.temperature: [[13.5, 4], [13.6, 17]]


    for position in current_experiment.saved_positions:
        data_line = position.name, position.timestamp, position.humidity[0][0], position.humidity[0][1], position.temperature[0][0], position.temperature[0][1]
        data_output.append(data_line)
        data_line2 = position.name, position.timestamp, position.humidity[1][0], position.humidity[1][1], position.temperature[1][0], position.temperature[1][1]
        data_output.append(data_line2)
    print(data_output)
    try:
        room_quality = pd.DataFrame(data=data_output,
                                columns=["name","datetime","humidity", "humidity_sensorpin", "temperature", "temperature_sensorpin"])
    except:
        blank_data = f"{current_experiment.name}: no data", datetime.now(), 0, 0
        room_quality = pd.DataFrame(data=blank_data,
                                columns=["name","datetime","humidity", "humidity_sensorpin", "temperature", "temperature_sensorpin"])
    print(room_quality.dtypes)
    room_quality['ordinal'] = dates.datestr2num(room_quality['datetime'])
    room_quality["datetime"] = pd.to_datetime(room_quality["datetime"])
    print(room_quality.dtypes)
    # create a month column, useful for seasonal data analysis
    room_quality['month'] = room_quality['datetime'].dt.strftime('%b')
    # # create a weekday column, useful for seasonal data analysis
    room_quality['weekday'] = room_quality['datetime'].dt.strftime('%a')
    # set index to datetime:
    room_quality = room_quality.set_index('datetime')
    sns.set(rc={'figure.figsize':(11, 4)})

    @plt.FuncFormatter
    def revert_to_dates(x, pos):
        """ Custom formater to turn floats into e.g., 2016-05-08"""
        return dates.num2date(x).strftime('%Y-%m-%d')
        # return dates.num2date(x).strftime('%m-%d')

    # remove NaNs and corrosponding row
    print(room_quality)
    # Drop the rows where at least one element is missing.
    # https://www.w3resource.com/pandas/dataframe/dataframe-dropna.php
    # https://www.geeksforgeeks.org/python-pandas-dataframe-dropna/
    # room_quality.dropna()
    # print(room_quality)
    # room_quality_nonan = room_quality.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)
    room_quality_nonan = room_quality.dropna(axis = 0, how ='any')
    print(room_quality_nonan)

    fig, ax = plt.subplots()
    # just use regplot if you don't need a FacetGrid
    sns.regplot(x=room_quality_nonan["ordinal"], y=room_quality_nonan["temperature"], ax=ax)
    # here's the magic:
    ax.xaxis.set_major_formatter(revert_to_dates)
    # legible labels
    # ax.tick_params(labelrotation=45)
    plt.savefig(f"{current_experiment.exp_foldername}/temperature.png")

    fig, ax = plt.subplots()
    # just use regplot if you don't need a FacetGrid
    sns.regplot(x=room_quality_nonan["ordinal"], y=room_quality_nonan["humidity"], ax=ax)
    # here's the magic:
    ax.xaxis.set_major_formatter(revert_to_dates)
    # legible labels
    # ax.tick_params(labelrotation=45)
    plt.savefig(f"{current_experiment.exp_foldername}/humidity.png")

    return render_template("environment.html", segment="environment",
    experiment_name = current_experiment.name, environment = table_output)

@app.route("/add-position")
def add_position():
    current_experiment = select_flagged_experiment()
    print(f"Current experiment name(s): {current_experiment.name}")
    current_experiment.add_current_experiment_position()
    # return experiment_positions=f"{current_experiment.experiment_positions}"
    return render_template("index.html", experiment_name = current_experiment.name, experiment_positions=current_experiment.show_experiment_positions())

@app.route("/yolo-search-go")
def search_go():
    current_experiment = select_flagged_experiment()
    current_experiment.custom_img = True
    # take a picture at position, for yolo analysis
    current_experiment.picture_task()
    print(f"Picture saved in Experiment: {current_experiment.name}")
    print(f"There are {len(current_experiment.saved_positions)} saved positions")
    print(f"Created at {current_experiment.saved_positions[-1].timestamp}")
    current_experiment.saved_positions[-1].calculate_yolo()
    x1, y1, confidence1 = current_experiment.saved_positions[-1].center_yolo_object

    # print the xy coordinates of the yolo object with the highest confidence
    print(f"Yolo object at {x1, y1}, with confidence: {confidence1}")

    print(f" {(x1, y1)}")
    if x1 < 0.5 and y1 < 0.5:
        current_experiment.planned_position = current_experiment.current_position + [1000, 1000, 0]
    elif x1 < 0.5 and y1 > 0.5:
        current_experiment.planned_position = current_experiment.current_position + [1000, -1000, 0]
    elif x1 > 0.5 and y1 < 0.5:
        current_experiment.planned_position = current_experiment.current_position + [-1000, 1000, 0]
    elif x1 > 0.5 and y1 > 0.5:
        current_experiment.planned_position = current_experiment.current_position + [-1000, -1000, 0]
    else:
        print("Bullseye, nothing to move")
    # move
    current_experiment.motor_position()
    # now wait 1s! :/
    time.sleep(1)
    # take new image, find out how much closer we are:
    current_experiment.custom_img = True
    current_experiment.picture_task()
    current_experiment.saved_positions[-1].calculate_yolo()
    x2, y2 = current_experiment.saved_positions[-1].center_yolo_object
    x_difference, y_difference = x2 - x1, y2 - y1
    print(x_difference, y_difference)

    # how much ticks are 
    x_rate = 1000/x_difference
    y_rate = 1000/y_difference
    print(x_rate, y_rate)
    print(x_rate*(0.5-x2), y_rate*(0.5-y2))
    # now calculate movement from remainding error
    x_ticks = x_rate*(0.5-x2)
    y_ticks = y_rate*(0.5-y2)

    # move the rest of the distance
    current_experiment.planned_position = current_experiment.current_position + [-x_ticks, -y_ticks, 0]
    current_experiment.motor_position()

    # or use some fancy PID
    # https://929687.smushcdn.com/2407837/wp-content/latex/4d6/4d620c4182821e707f2c3ec704cf2039-ffffff-000000-0.png?lossy=1&strip=1&webp=0

    return ("nothing")

# flask form for experiment selection
# https://python-adv-web-apps.readthedocs.io/en/latest/flask_forms.html
# https://www.codecademy.com/learn/learn-flask/modules/flask-templates-and-forms/cheatsheet
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, widgets, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired

# Flask-WTF requires an encryption key - the string can be anything
app.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'

# Flask-Bootstrap requires this line
Bootstrap(app)
class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()
# class SimpleForm(FlaskForm):
#     string_of_files = ['one\r\ntwo\r\nthree\r\n']
#     list_of_files = string_of_files[0].split()
#     # create a list of value/description tuples
#     files = [(x, x) for x in list_of_files]
#     example = MultiCheckboxField('Label', choices=files)

class ExperimentForm(FlaskForm):
    name = StringField('Experiment name: ', validators=[DataRequired()])
    interval = IntegerField('Interval between automatic imaging in minutes: ', default = 30)
    # positions = BooleanField('Position 0', false_values=None)
    # options:
    # string_of_files = ['0,0,0\r\n1000,0,0\r\n0,1000,0\r\n-1000,0,0\r\n0,-1000,0\r\n']
    # 10 positions, starting at the right top (0,0,0), going down 5, 1 left and 5 up
    string_of_files = ['0,0,0\r\n-125000,0,0\r\n-235000,0,-10000\r\n-345000,-15000,-30000\r\n-445000,-25000,-40000\r\n-435000,100000,-40000\r\n-330000,100000,-35000\r\n-220000,110000,-30000\r\n-105000,125000,-15000\r\n20000,130000,0']
    list_of_files = string_of_files[0].split()
    # print(list_of_files)
    # print(type(list_of_files))
    # print(type(list_of_files[0]))
    # create a list of value/description tuples
    files = [(x, x) for x in list_of_files]
    positions = MultiCheckboxField('Positions', choices=files)

    submit = SubmitField('Create')

@app.route('/experiments', methods=['GET', 'POST'])
def experiments():
    names = []
    positions = []
    intervals = []
    sensors = []
    for experiment in DATABASE:
        names.append(experiment.name)
        positions.append(experiment.experiment_positions)
        intervals.append(experiment.interval_minutes)
        sensors.append(experiment.sensors)
        
    print(f"Current experiment name(s): {names}")
    # you must tell the variable 'form' what you named the class, above
    # 'form' is the variable name used in this template: index.html
    form = ExperimentForm()
    message = ""
    interval = INTERVAL
    experiment_positions = EXPERIMENT_POSITIONS
    if form.validate_on_submit():
        name = form.name.data
        if name.lower() in names:
            # empty the form field
            form.name.data = ""
            # id = get_id(ACTORS, name)
            # redirect the browser to another route and template
            # return redirect( url_for('actor', id=id) )
            message = "The experiment name is already taken."
        else:
            print(DATABASE)
            # unflag all previous experiments
            for experiment in DATABASE:
                if(experiment.flag):
                    experiment.flag = False
                    print(f"Experiment {experiment.name} unflagged")
            interval = int(form.interval.data)
            # experiment_positions = list(map(list, form.positions.data))
            # experiment_positions = list(map(int, form.positions.data))
            print(type(form.positions.data))
            print(form.positions.data)
            # this is unreadable, sorry
            # it converts the strings in the list of list to int
            experiment_positions = [[int(num) for num in map(int, sub.split(','))] for sub in form.positions.data]
            print(experiment_positions)

            # insert sensors

            experiment_name = name.lower() # experiments are forced into lowercase
            new_experiment = Experiment(experiment_name, scheduler,
                IMAGEPATH, Camera, experiment_positions, interval)
        
            new_experiment.flag = True
            DATABASE.append(new_experiment)
            message = (f"The experiment {new_experiment.name} was created. Positions set to {new_experiment.experiment_positions}. Interval time set to {new_experiment.interval_minutes} minutes")

    return render_template('experiments.html', names=names, segment="experiments" ,positions=positions, intervals=intervals, sensors=sensors, form=form, message=message)

@app.route('/get_experiment_status') 
# @app.route('/experiments')
def experiment_status():
    experiment_name = request.args.get('status')
    print(f"Experiment name: {experiment_name}")

    # this cannto work for now !!!!!!!!!!!!!!!!!!!!!!
    # experiment_positions = request.args.get('experiment_positions')
    # interval = request.args.get('interval')
    # new_experiment = Experiment(experiment_name, scheduler,
    # IMAGEPATH, Camera, experiment_positions, interval)

    # create new experiment with custom name, positions, interval,...
    new_experiment = Experiment(experiment_name, scheduler,
    IMAGEPATH, Camera, EXPERIMENT_POSITIONS, INTERVAL)

    # unflag all experiments, works already
    for experiment in DATABASE:
        if(experiment.flag):
            experiment.flag = False
    DATABASE.append(new_experiment)
    new_experiment.flag = True

    # this creates the default experiment and flags it - works!
    # new_experiment = select_flagged_experiment()
    # print(new_experiment.name)
    # new_experiment.name = "GeorgsExperiment"

    return f"{new_experiment.name}"

# select experiment by name
@app.route('/experiment/<experiment_name>')
def profile(experiment_name):
    experiment_name = experiment_name.lower()
    print(f"Selected experiment: {experiment_name}")
    # unflag all experiments for preparation
    for experiment in DATABASE:
        if(experiment.flag):
            experiment.flag = False
    # during generation of experiments, it is ensured that names are uniqe and lowercase
    for experiment in DATABASE:
        if(experiment.name == experiment_name):
            experiment.flag = True
            return redirect(url_for('index'))
            # return experiment

def select_flagged_experiment():
    print(f"Current database lenght: {len(DATABASE)}")
    if(len(DATABASE) == 0):
        print("No experiments found, creating default experiment")
        new_experiment = Experiment(EXPERIMENT_NAME, scheduler,
        IMAGEPATH, Camera, EXPERIMENT_POSITIONS, INTERVAL)
        DATABASE.append(new_experiment)
        return new_experiment
    else:
        # try to select experiment
        # return render_template("gallery.html", image_foldername = foldername_gallery)
        try:
            print("Trying to select the first flagged experiment")
            for experiment in DATABASE:
                if(experiment.flag):
                    return experiment
            print("No flagged experiments")
            raise Exception 
        except:
            print("Trying to select the last experiment in DB")
            new_experiment = DATABASE[-1]
            return new_experiment

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, threaded=True)