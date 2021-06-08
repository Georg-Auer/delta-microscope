
//quadstepper_inverted deltabot

// kinematics integrated, 
// after movement finished, 
// cam and LED is triggered with time-settings specified in the OSC-message
// enable/disable motors

//xyz movement

//pins:
/*
-STANDARD WIRING DIAGRAM (teensy 3.x): not all pins are used in every setup!
=================================================================== 
    
* Modular Setup - PIN connections - teensy 3.2/3.6 compatible

| PIN | PUMP           | Pump-function  | DELTA-BOT      | SOLENOIDS | Sol-driver | MEASUREMENT/SORTING     | M/S function                                                             |
|-----+----------------+----------------+----------------+-----------+------------+-------------------------+--------------------------------------------------------------------------|
|   0 |                |                |                | SOL1      | ULN1/Pin1  |                         |                                                                          |
|   1 | enablePumppin  | EnableP0       | ENMD1          | SOL2      | ULN1/Pin2  |                         |                                                                          |
|   2 | directionpin   | DIRpump0       | MD1            | SOL3      | ULN1/Pin3  |                         |                                                                          |
|   3 | steppin        | STEPpump0      | MD1            | SOL4      | ULN1/Pin4  |                         |                                                                          |
|   4 | enablePump1pin | EnableP1       | ENMD2          | SOL5      | ULN1/Pin5  |                         |                                                                          |
|   5 | directionpin1  | DIRpump1       | MD2            | SOL6      | ULN1/Pin6  |                         |                                                                          |
|   6 | steppin1       | STEPpump1      | MD2            | SOL7      | ULN1/Pin7  |                         |                                                                          |
|   7 | enablePump2pin | EnableP2       | ENMD3          | SOL8      | ULN1/Pin8  |                         |                                                                          |
|   8 | directionpin2  | DIRpump2       | MD3            |           |            |                         |                                                                          |
|   9 | steppin2       | STEPpump2      | MD3            |           |            |                         |                                                                          |
|  10 | enablePump3pin | EnableP3       | not used       |           |            |                         |                                                                          |
|  11 | directionpin3  | DIRpump3       | not used       |           |            |                         |                                                                          |
|  12 | steppin3       | STEPpump3      | not used       |           |            |                         |                                                                          |
|-----+----------------+----------------+----------------+-----------+------------+-------------------------+--------------------------------------------------------------------------|
|  13 | not used       | not used       | not used       | SOL16     | ULN2/Pin8  |                         |                                                                          |
|  14 | A0 (not used)  | Trigger (opt)  | A0=cam-trigger | SOL15     | ULN2/Pin7  |                         |                                                                          |
|  15 | A1 (not used)  | Trigger (opt)  | A1=LED-trigger | SOL14     | ULN2/Pin6  |                         |                                                                          |
|  16 | endStopFpin    | EndSTOPP0Front | ESTOPMD1F      | SOL13     | ULN2/Pin5  |                         |                                                                          |
|  17 | endStopBpin    | EndSTOPP0Back  | ESTOPMD1B      | SOL12     | ULN2/Pin4  |                         |                                                                          |
|  18 | endStop1Fpin   | EndSTOPP1Front | ESTOPMD2F      | SOL11     | ULN2/Pin3  | Trigger3                | broken out with GND                                                      |
|  19 | endStop1Bpin   | EndSTOPP1Back  | ESTOPMD2B      | SOL10     | ULN2/Pin2  | Trigger2                | broken out with GND                                                      |
|  20 | endStop2Fpin   | EndSTOPP2Front | ESTOPMD3F      | SOL9      | ULN2/Pin1  | Trigger1                | broken out with GND                                                      |
|  21 | endStop2Bpin   | EndSTOPP2Back  | ESTOPMD3B      |           |            | CAMERA-Trigger          | broken out with GND                                                      |
|  22 | endStop3Fpin   | EndSTOPP3Front | not used       |           |            | LED-Strobe-Trigger      | broken out with GND                                                      |
|  23 | endStop3Bpin   | EndSTOPP3Back  | not used       |           |            | SENSOR-Measurement (A9) | with Analog-GND + 3.3V (talos-sensors); A-GND only (BNC-connected sens.) |
|     |                |                |                |           |            |                         |                                                                          |



camera-trigger: pin 14
LED-trigger: pin 15


motor1 (towerA, MD1)
enable              1
DIR                 2
STP                 3

motor2 (towerB, MD2)
enable              4
DIR                 5
STP                 6

motor3 (towerC, MD3)
enable              7
DIR                 8
STP                 9


Big Easy Driver - things not used:
/////////////////////////////////////////////////////////////////////////////////////
MS1 MS2 MS3  (16 ustepping per default)
H   H   H    1/16
/////////////////////////////////////////////////////////////////////////////////////

FORMAT OF THE OSC_MESSAGE
/////////////////////////
position/speed motors; 
camera-waiting time after movement completed (usec); 
3x(strobepulse & duration - in usec after camera was triggered); 
CAM&LED-on/off 

17 values:
==========

in_motorA
speed_motorA
in_motorB
speed_motorB
in_motorC
speed_motorC

delta_status
*/

// Library for stepper motors
#include <AccelStepper.h>

//define Pins
AccelStepper motorA(1, 3, 2);
AccelStepper motorB(1, 6, 5);
AccelStepper motorC(1, 9, 8);//...(1[means driver board is used], step, dir)

///libraries and code for OSC communication
#include <OSCBundle.h>
#include <OSCBoards.h>

#ifdef BOARD_HAS_USB_SERIAL
#include <SLIPEncodedUSBSerial.h>
SLIPEncodedUSBSerial SLIPSerial( thisBoardsSerialUSB );
#else
#include <SLIPEncodedSerial.h>
SLIPEncodedSerial SLIPSerial(Serial);
#endif

//OSC

// Read new position - incoming from PD, seems unused and should be removed
int32_t in_motorA = 0;
int32_t in_motorB = 0;
int32_t in_motorC = 0;

// used for endstops and start-stop
int delta_status = 0;

//-----------------------new for internal coordinates
//internal motor Values
int32_t arduino_motorA = 0;
int32_t arduino_motorB = 0;
int32_t arduino_motorC = 0;

//internal x,y,z values
int32_t arduino_x = 0;
int32_t arduino_y = 0;
int32_t arduino_z = 0;
//------------------------------------

//which speed?
int32_t speed_motorA = 20000;
int32_t speed_motorB = 20000;
int32_t speed_motorC = 20000;
int32_t speed_motorABC = 20000;
int32_t endstopspeed = 15000; //steps/s and anti-clockwise movement if go to endstop is triggered

//raw-coordinates xyz (in ticks)
int x_movement = 0;
int y_movement = 0;
int z_movement = 0;

//int send = 0; //prints positions via OSC to periphery, print is 0 at start

const int ledPin = 13;  //for debugging

int endstops(int delta_status){
  if (delta_status == 2){
    //as long as not all motors are in zero position::::HIGH = on endstop  
    while (digitalRead(16)==LOW || digitalRead(18)==LOW || digitalRead(20)==LOW){
      //motorA::run towards endstop, then stop, and set pos & coordinate-variable to 0
      if (digitalRead(16)==LOW){
        motorA.setSpeed(endstopspeed);
        motorA.runSpeed();      
      } else if (digitalRead(16)==HIGH){
        in_motorA = 0;//set coordinate to 0 
        arduino_motorA = 0;
        speed_motorA = 0;//set speed to 0 to be sure 
        motorA.setSpeed(0);//stop motor
      }
      //motorB::run towards endstop, then stop, and set pos & coordinate-variable to 0
      if (digitalRead(18)==LOW){
        motorB.setSpeed(endstopspeed);
        motorB.runSpeed();      
      } else if (digitalRead(18)==HIGH){
        in_motorB = 0;//set coordinate to 0 
        arduino_motorB = 0;
        speed_motorB = 0;//set speed to 0 to be sure  
        motorB.setSpeed(0);//stop motor
        
      }
      //motorC::run towards endstop, then stop, and set pos & coordinate-variable to 0
      if (digitalRead(20)==LOW){
        motorC.setSpeed(endstopspeed);
        motorC.runSpeed();      
      } else if (digitalRead(20)==HIGH){
        in_motorC = 0;//set coordinate to 0 
        arduino_motorC = 0;
        speed_motorC = 0;//set speed to 0 to be sure 
        motorC.setSpeed(0);//stop motor
      } 

    }//end of while

    motorA.setCurrentPosition(0);//set pos to 0  
    motorB.setCurrentPosition(0);//set pos to 0 
    motorC.setCurrentPosition(0);//set pos to 0
    delta_status=0;//'arrived on endstops, sets back the status'
    //should send a statement to PD that everything is on zero
    send_osc_message();
  }//end of if-statement
  return delta_status;
}

void send_osc_message(){
  OSCBundle bndlOUT;  //name of bundle that is created  
  //sends back actual position
  bndlOUT.add("/x-position").add(arduino_x); 
  bndlOUT.add("/y-position").add(arduino_y);
  bndlOUT.add("/z-position").add(arduino_z);
  bndlOUT.add("/delta_status").add(delta_status);
  
  //sends back position where arduino was sent to
  bndlOUT.add("/x-position").add(x_movement); 
  bndlOUT.add("/y-position").add(y_movement);
  bndlOUT.add("/z-position").add(z_movement);
  
  //for debugging: send back calculated values
  bndlOUT.add("/arduino_motorA").add(arduino_motorA);
  bndlOUT.add("/arduino_motorB").add(arduino_motorB);
  bndlOUT.add("/arduino_motorC").add(arduino_motorC);

  SLIPSerial.beginPacket();
  bndlOUT.send(SLIPSerial); // send the bytes to the SLIP stream
  SLIPSerial.endPacket(); // mark the end of the OSC Packet
  bndlOUT.empty(); // empty the bundle to free room for a new one
} 


void blinking(int time = 1000){
  digitalWrite(ledPin, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(time);               // wait for a second
  digitalWrite(ledPin, LOW);    // turn the LED off by making the voltage LOW
  delay(time);               // wait for a second
}


// int move_to_xyz(int32_t arduino_motorA, int32_t arduino_motorB, int32_t arduino_motorC, int speed, int delta_status){
//   //normal movement::set parameters and move it  
//   motorA.setSpeed(speed);
//   motorB.setSpeed(speed);
//   motorC.setSpeed(speed);

//   //move to absolute values instead in_motor
//   motorA.moveTo(arduino_motorA);
//   motorB.moveTo(arduino_motorB);
//   motorC.moveTo(arduino_motorC);

//   //move motors - do it!  
//   motorA.runSpeedToPosition(); 
//   motorB.runSpeedToPosition(); 
//   motorC.runSpeedToPosition(); 

//   //delta_status = 0;
//   return delta_status;
// }


int calculate_motorA(int32_t x_movement, int32_t y_movement, int32_t z_movement){
  //calculate arduino_motor A,B,C here
  int delta_arms = 1214550;  // L=60.12mm 1step = 0.0495um =1214550 ticks
  //int delta_radius = ????;
  int Ax0 = 408178; //=Bx0
  int Ay0 = 235663; //=By0
  arduino_motorA = (sqrt((pow(delta_arms,2))-(pow((Ax0+x_movement),2))-(pow((Ay0+y_movement),2))))-z_movement-0.5; //-0.5 to round down!
  int start_value = 1119367;
  arduino_motorA = arduino_motorA-start_value;
  return (arduino_motorA);
}
int calculate_motorB(int32_t x_movement, int32_t y_movement, int32_t z_movement){
  //calculate arduino_motor A,B,C here
  int delta_arms = 1214550;  // L=60.12mm 1step = 0.0495um =1214550 ticks
  //int delta_radius = ????;
  int Ax0 = 408178; //=Bx0
  int Ay0 = 235663; //=By0
  arduino_motorB = (sqrt(pow(delta_arms,2)-(pow((Ax0-x_movement),2))-(pow((Ay0+y_movement),2))))-z_movement-0.5; //-0.5 to round down!
  int start_value = 1119367;
  arduino_motorB = arduino_motorB-start_value;
  return (arduino_motorB);
}
int calculate_motorC(int32_t x_movement, int32_t y_movement, int32_t z_movement){
  //calculate arduino_motor A,B,C here
  int delta_arms = 1214550;  // L=60.12mm 1step = 0.0495um =1214550 ticks
  //int delta_radius = ????;
  int Cy0 = 471323;
  arduino_motorC = (sqrt((pow(delta_arms,2))-(pow(x_movement,2))-(pow((Cy0-y_movement),2))))-z_movement-0.5; //-0.5 to round down!
  int start_value = 1119368;
  arduino_motorC = arduino_motorC-start_value;
  return (arduino_motorC);
}

void setup(){
  // initialize serial communications:
  //begin SLIPSerial just like Serial
  SLIPSerial.begin(115200);   // set this as high as you can reliably run on your platform
  
  pinMode(ledPin, OUTPUT); //internal LED for debugging

  //enable motors
  pinMode (1, OUTPUT); //motorA_EN
  pinMode (4, OUTPUT); //motorB_EN
  pinMode (7, OUTPUT); //motorC_EN

  //motors on at the beginning
  digitalWrite (1, LOW); //motorA HIGH:off, LOW:on
  digitalWrite (4, LOW); //motorB
  digitalWrite (7, LOW); //motorC

  //enable endstop-pins   -->endstop works with 'active high'
  pinMode(16, INPUT_PULLDOWN); //endstop motorA
  pinMode(18, INPUT_PULLDOWN); //endstop motorB
  pinMode(20, INPUT_PULLDOWN); //endstop motorC

  // //disable endstop-pins for debugging  -->endstop works with 'active high'
  // pinMode(16, INPUT_PULLUP); //endstop motorA
  // pinMode(18, INPUT_PULLUP); //endstop motorB
  // pinMode(20, INPUT_PULLUP); //endstop motorC

  //max speed  
  motorA.setMaxSpeed(20000); //check if too fast/slow, take care not to loose steps
  motorA.setAcceleration(2500);
  motorB.setMaxSpeed(20000);
  motorB.setAcceleration(2500);
  motorC.setMaxSpeed(20000);
  motorC.setAcceleration(2500);
}

void loop(){
  if (delta_status == 1){
    // blinking(500);
    digitalWrite (1, LOW); //motorA
    digitalWrite (4, LOW); //motorB
    digitalWrite (7, LOW); //motorC
    //move_to_xyz(arduino_motorA,arduino_motorB,arduino_motorC);
    //for testing: move all motors to received z value
    arduino_motorA = calculate_motorA(x_movement,y_movement,z_movement);
    arduino_motorB = calculate_motorB(x_movement,y_movement,z_movement);
    arduino_motorC = calculate_motorC(x_movement,y_movement,z_movement);
    motorA.setSpeed(speed_motorABC);
    motorB.setSpeed(speed_motorABC);
    motorC.setSpeed(speed_motorABC);
    delta_status = 3; //status for set movement, unfinished
  }
  else if (delta_status == 2){
    // blinking(500);
    digitalWrite (1, LOW); //motorA
    digitalWrite (4, LOW); //motorB
    digitalWrite (7, LOW); //motorC
    delta_status = endstops(delta_status); //this should pass an 0 to delta_status
    // blinking(500);
    //set everything to zero
    x_movement = 0;
    y_movement = 0;
    z_movement = 0;
    arduino_motorA = calculate_motorA(x_movement,y_movement,z_movement);
    arduino_motorB = calculate_motorB(x_movement,y_movement,z_movement);
    arduino_motorC = calculate_motorC(x_movement,y_movement,z_movement);
  }
  //enable/disable motors::::HIGH:off, LOW:on
  else if (delta_status == 0){ 
    digitalWrite (1, HIGH); //motorA
    digitalWrite (4, HIGH); //motorB
    digitalWrite (7, HIGH); //motorC     
  }

  // move_to_xyz(arduino_motorA,arduino_motorB,arduino_motorC,speed_motorABC,delta_status);
  // //delta_status = 0;

  //move to absolute values instead in_motor
  motorA.moveTo(arduino_motorA);
  motorB.moveTo(arduino_motorB);
  motorC.moveTo(arduino_motorC);

  motorA.setSpeed(speed_motorABC);
  motorB.setSpeed(speed_motorABC);
  motorC.setSpeed(speed_motorABC);

  //move motors - do it!  
  motorA.runSpeedToPosition(); 
  motorB.runSpeedToPosition(); 
  motorC.runSpeedToPosition(); 

  // && (delta_status != 2)
  // maybe this should be further up
  if ((motorA.distanceToGo() == 0) && (motorB.distanceToGo() == 0) && (motorC.distanceToGo() == 0)){
    //send osc that position is reached, motors are idle
    delta_status = 0;
  }
  
  //only listen to OSC slipserial incoming communication when a message is waiting 
  if (SLIPSerial.available() > 0){
    //OSC slipserial incoming communication
    OSCMessage messageIN; 
    while(!SLIPSerial.endofPacket()){
      int size = SLIPSerial.available();
        if (size>0){
          while(size--){
            messageIN.fill(SLIPSerial.read());
          }
        }
    } 
 
    //get the values
    x_movement = messageIN.getInt(0);
    y_movement = messageIN.getInt(1);
    z_movement = messageIN.getInt(2);
    speed_motorABC = messageIN.getInt(3); 
    delta_status = messageIN.getInt(4);

    messageIN.empty(); ///clears message from contents

    //update motor values before sending back calculated values
    arduino_motorA = calculate_motorA(x_movement,y_movement,z_movement);
    arduino_motorB = calculate_motorB(x_movement,y_movement,z_movement);
    arduino_motorC = calculate_motorC(x_movement,y_movement,z_movement);
    //declare the bundle to send some of the received messages back to PD for confirmation
    OSCBundle bndlOUT;  //name of bundle that is created  
    //sends back actual position
    bndlOUT.add("/x-position").add(arduino_x); 
    bndlOUT.add("/y-position").add(arduino_y);
    bndlOUT.add("/z-position").add(arduino_z);
    bndlOUT.add("/delta_status").add(delta_status);  //gives feedback that previous movement is 'done' (1), or endstops reached (2)
    
    //sends back position where arduino was sent to
    bndlOUT.add("/x-position").add(x_movement); 
    bndlOUT.add("/y-position").add(y_movement);
    bndlOUT.add("/z-position").add(z_movement);
    
   //for debugging: send back calculated values
    bndlOUT.add("/arduino_motorA").add(arduino_motorA);
    bndlOUT.add("/arduino_motorB").add(arduino_motorB);
    bndlOUT.add("/arduino_motorC").add(arduino_motorC);

    SLIPSerial.beginPacket();
    bndlOUT.send(SLIPSerial); // send the bytes to the SLIP stream
    SLIPSerial.endPacket(); // mark the end of the OSC Packet
    bndlOUT.empty(); // empty the bundle to free room for a new one    
    //send = 0;
  }
}
