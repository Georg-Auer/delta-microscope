import time
import numpy as np
from pySerialTransfer import pySerialTransfer as txfer
# please make sure to pip install pySerialTransfer==1.2
# connection will not work with pySerialTransfer==2.0
# requirement: pip install pyserial (works with 3.4 and most likely newer but not much older versions)
# on teensy: include "SerialTransfer.h" Version 2.0
# updated: now works with current SerialTransfer.h, and pySerialTransfer (27.02.2021)

# def connect_to_arduino(comport = '/dev/ttyACM0',
def connect_to_arduino(comport = 'COM21',
        motor0_enable = 1, motor0_direction = 0, motor0_position = 0, motor0_speed = 5000,
        motor1_enable = 1, motor1_direction = 0, motor1_position = 0, motor1_speed = 5000,
        motor2_enable = 1, motor2_direction = 0, motor2_position = 0, motor2_speed = 5000,
        motor3_enable = 1, motor3_direction = 0, motor3_position = 0, motor3_speed = 5000):
    try:
        logging.debug(f"Connecting to {comport}")
        link = txfer.SerialTransfer(comport)
        
        link.open()
        time.sleep(1) # allow some time for the Arduino to completely reset
        
        # reset send_size
        send_size = 0
        
        # Send a list
        list_ = [motor0_enable, motor0_direction, motor0_position, motor0_speed, motor1_enable, motor1_direction, motor1_position, motor1_speed, 
            motor2_enable, motor2_direction, motor2_position, motor2_speed, motor3_enable, motor3_direction, motor3_position, motor3_speed]
        logging.debug(list_)
        list_size = link.tx_obj(list_)
        send_size += list_size
        
        # Transmit all the data to send in a single packet
        link.send(send_size)
        logging.debug("Message sent...")
        
        # Wait for a response and report any errors while receiving packets
        while not link.available():
            if link.status < 0:
                if link.status == -1:
                    logging.debug('ERROR: CRC_ERROR')
                elif link.status == -2:
                    logging.debug('ERROR: PAYLOAD_ERROR')
                elif link.status == -3:
                    logging.debug('ERROR: STOP_BYTE_ERROR')

        # Parse response list
        ###################################################################
        rec_list_  = link.rx_obj(obj_type=type(list_),
                                    obj_byte_size=list_size,
                                    list_format='i')
 
        logging.debug(f'SENT: {list_}')
        logging.debug(f'RCVD: {rec_list_}')

        link.close()
        return rec_list_

    except KeyboardInterrupt:
        link.close()

    except:
        import traceback
        traceback.logging.debug_exc()
        link.close()

def list_available_ports() -> list:
    ports = txfer.open_ports()
    logging.debug("Available ports:")
    logging.debug(ports)
    return ports

if __name__ == "__main__":
    ports = list_available_ports()
    logging.debug(ports)
    comport = '/dev/ttyACM0'
    # enable = 0, disable = 1
    motor0_enable = 0
    motor0_direction = 0
    motor0_position = 0
    motor0_speed = 0
    motor1_enable = 0
    motor1_direction = 0
    motor1_position = 0
    motor1_speed = 0
    motor2_enable = 0
    motor2_direction = 0
    motor2_position = 0
    motor2_speed = 0
    motor3_enable = 0
    motor3_direction = 0
    motor3_position = 0
    motor3_speed = 0
    try:
        list_ = [motor0_enable, motor0_direction, motor0_position, motor0_speed, motor1_enable, motor1_direction, motor1_position, motor1_speed, 
            motor2_enable, motor2_direction, motor2_position, motor2_speed, motor3_enable, motor3_direction, motor3_position, motor3_speed]
        logging.debug(list_)
    except:
        logging.debug("Sending did not work, please check comport")