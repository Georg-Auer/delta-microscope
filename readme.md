
**Supplementary 4: Delta kinematic microscope stage**

Based on a delta kinematic design, the device has a very small
footprint, which eases placement in incubators. The robotic is computer
controlled thus making is amenable for automated observing, manipulating
and monitoring of appliances and events at the microscale over prolonged
time periods.

**Materials and Technology**

**Computer-aided design (CAD) in combination with computer-aided
manufacturing (CAM) technology was applied to generate and 3D print the
load-bearing parts.** Design was achieved with the aid of the
open-source CAD software, openSCAD (openscad.org).

![images/openscad\_microscope.png](media/image5.png){width="2.05in"
height="3.242727471566054in"}
![images/3dprinted\_microscope.jpg](media/image6.jpeg){width="1.8289555993000874in"
height="3.235845363079615in"}

**SFigure 4.1:** Delta kinematic stage as depicted in CAD view (left)
and completed holding a videomicroscope (right)

For the individual building parts, files in stl format were exported and
translated into a format, which eventually can be interpreted by 3D
printers (Prusa Slicer, Pursa3d.com), in our case the 3D filament
printer Prusa MK3.

![smallparts.PNG](media/image7.png){width="2.7130850831146107in"
height="2.118436132983377in"}
![bigparts.PNG](media/image8.png){width="2.558333333333333in"
height="2.127739501312336in"}

**SFigure 4.2:** Individual parts as depicted after slicing before 3D
printing

The respective files (stl as well as the sliced format are freely
available for download at
https://github.com/spoc-lab/delta\_microscope/tree/master/files

The STL files for the robotic stage were sliced in Prusa Slicer 2.2.0
and printed in ecoPLA NeonOrange with 20% infill.

Materials used for assembly were as compiled in the table below and
depicted in SFigure 4.3.

Stable 4.1

| item                                                           | number | purpose               | bought from   |  part-no | costs in € |
|----------------------------------------------------------------+--------+-----------------------+---------------+----------+------------|
| Allegro A4983 Based Stepper Boards: here the 'Big Easy Driver' |      3 | stepper board         | Technobots    | 2900-445 | ~ 70       |
| Teensy 4.0 or 4.1 Microcontroller                              |      1 | stepper control       | Conrad        |  2269230 | ~ 30       |
| Nema 17 Steppers (0.9° 2.4 A)                                  |      3 | stepper motor         | Act-motor     | 1402-050 | ~ 60       |
| Fine Hex Adjuster, 1/4"-80, 4" Long                            |      3 | leadscrew             | Thorlabs      | F25SS400 | ~ 40       |
| Locking Phosphor-Bronze Bushing with Nut, 1/4"-80, L=0.50"     |      3 | leadscrewnut          | Thorlabs      |   N80L6P | ~ 28       |
| Linear Guide Rails (min 200 mm)                                |      3 | slides platform       | Amazon        | CNBTR214 | ~ 45       |
| Universal Coupling Body                                        |      3 | motor-screw-connector | Technobots    | 4604-050 | ~ 12       |
| Universal Coupling Insert - 5 mm                               |      3 | motor-side            | Technobots    | 4604-059 | ~ 8        |
| Universal Coupling Insert - 1/4"                               |      3 | screw-side            | Technobots    | 4604-066 | ~ 8        |
| OTHER SMALL ITEMS                                              |        |                       |               |          |            |
| 160 mm x 100 mm Copper Clad Stripboard                         |      1 | mount for electronics | Conrad        |          | ~ 2        |
| Male & Female PCB Headers 2.45 mm pitch                        |   some | simple connectors     | Conrad        |          | ~ 10       |
| Screws M3 (10 mm): 12 for motors, 6 for sliders, 15 for guides |     33 | mount slider & motors | Bauhaus       |          |            |
| Nuts M3                                                        |     33 | fixing screws         | Bauhaus       |          |            |
| Screws M6 (15 mm)                                              |     12 | suspension            | Bauhaus       |          |            |
| Screws M6 (60 mm)                                              |      6 | suspension            | Bauhaus       |          |            |
| Nuts M6 (end nut)                                              |      6 | suspension            | Bauhaus       |          |            |
| Neodymium bullet magnets ⌀ 10 mm                               |      6 | suspension            | Bauhaus       |          |            |
| USB (micro) cable                                              |      1 |                       | Conrad        |          | ~ 3        |
| 6 wire colored ribbon cable                                    |    3 m |                       | Conrad        |          | ~ 3        |
| 12 V / >=5 A power supply                                      |      1 |                       | Conrad        |          | ~ 20       |
| 197 g 3D-printer filament (PLA 1.75 mm)                        |1*250 g | microscope structure  | 3d jake       |          | ~ 10       |
| USA Digital Microscope 40x-1000x                               |      1 | microscope camera     | Bysameyee     |          | ~ 20       |
|----------------------------------------------------------------+--------+-----------------------+---------------+----------+------------|
|                                                                |        |                       |               |          | <  400     |


\*Technobots:
[www.technobotsonline.com](http://www.technobotsonline.com); Thorlabs:
[www.thorlabs.com](http://www.thorlabs.com); Conrad:
[www.conrad.at](http://www.conrad.at); Bauhaus:
[www.bauhaus.at](http://www.bauhaus.at); 3djake:
[www.3djake.at](http://www.3djake.at); Bysameyee:
[www.bysameyee.com/microscope](http://www.bysameyee.com/microscope)

![signal-2020-07-15-150952.jpg](media/image9.jpeg){width="4.25in"
height="4.2153324584426946in"}

**SFigure4.3** Parts before assembly

**Mechanical Assembly was accomplished first** tinning the leads of the
motors with solder, then adding a male PCB-connector (or any other
connector, next using heat-shrinking tube to electrically isolate the
connectors at the end, and eventually adding the mechanical connector
for the leadscrew (5-mm brass insert) to the motor as one is space-wise
greatly hindered later. For the l**eadscrew part,** the brass inserts
are added to connect the motor onto the leadscrew, the screws are
inserted very carefully to avoid damaging the thread.

The linear guide rails were screwed onto the main part, and the top part
was then screwed onto the guide rails with 15xM3 screws and nuts. For
correct assembly, the top part has to end on height of the guide rails.
The three stepper motors where then screwed (12xM3) onto the bottom
part. The bottom part needs to be screwed on the other end of the guide
rails (3xM3). Now the universal couplings are screwed onto the motors
and the optical fine threaded rods are fixed on the other side of the
universal couplings. For better durability, the plastic part of the
universal couplings are glued to the metallic part with epoxy glue. Six
M6 screws are glued into the three slider parts, and 6 M6 are glued into
the platform. The slider parts are now joined with their threaded insert
and can be screwed onto the guide rails. The end nuts are now placed on
the 60 mm M6 screws and the microscope stage is completed by putting the
neodymium magnets in the joint positions. Finally, the microscope-camera
can be put in the ring on top where it is held in position with the
printed clamp.

**In order to control the stepper motors an A4983 stepper driver chip
was implemented (Allegro Microsystems for details see
http://www.technobotsonline.com/Datasheets2/1518-009-A4983SETTR-T.pdf),
optimally the 'Big Easy Driver' for each motor
(<https://www.sparkfun.com/products/12859>) as the latter works by
default in a 16-step microstepping mode ('MS1, MS2, MS3' pins
unconnected). The stepper drivers are controlled with a teensy 4.0 or
4.1 microcontroller.**

**In order to assemble the board, connectors were soldered onto the
driver board (e.g. PCB-connectors), the parts are then allocated on a
stripboard and holes were drilled in a way that the board can be easily
mounted with screws into a base made from laser-cut acrylic. Next,
female PCB-connectors for the teensy and the stepper boards were
soldered on the board, not forgetting to cut the traces on the
stripboard underneath, and everything is connected accordingly (SFigure
4.4.)**

![images/Electronics.jpeg](media/image10.jpeg){width="6.3in"
height="3.001359361329834in"}

**SFigure 4.4. Connecting board to motors: Left: Images of the
electronics board with three stepper driver boards mounted. Right:
Schematic diagram.**

**The system was made as simple as possible, by omitting connection to
MS1, MS2, MS3 (all are pulled high when not connected meaning the driver
are set to the default 16 microstep-mode. Furthermore sleep (slp) and
reset (rst) was not connected thus automatically activating these modes
when the system is powered and for shutting down the motors, the power
is turned off. Solely following steps had to be performed: (i) enable
(en) was pulled low on all by connecting to ground (this is important,
otherwise the pins float); (ii) GND was shared between teensy and the
quadstepper board (or single big easy drivers); (iii) step-pin (stp) was
activated in a way that if high for \>1 microsecond, the motor will
step; (iv) the direction-pin (dir) was adapted through the high/low sets
which control the direction of the motors steps, which can be easily
changed by reverse the connections of the leads from green, black, blue,
red --\> to red, blue, black, green; (v) Teensy was powered by a USB
connection, motors by a 12V 5A power supply (make sure that the current
supplied to the motor is adjusted with the small potentiometer on the
stepper driver board. On max, the chip rapidly turns hot and the motor
might exhibit a strong enough torque to carry on driving beyond the
end-stop, thus damaging the microscope assembly.**

**The motors were controlled with a microcontroller (a 'teensy' 4.0 or
4.1) and a software front end was written in Pure Data (PD). Pure Data
(PD, https://puredata.info/) is an open-source dataflow programming
language used primarily for music and video applications. It runs on
nearly every computing platform, is straightforward to learn and can be
modified 'live'. The teensy (https://www.pjrc.com/teensy/teensy31.html)
was a 3.3V, 32-bit ARM based microcontroller that is compatible with the
Arduino toolchain (https://www.arduino.cc/en/Guide/HomePage) and
therefore easy to program. The prime reason to use a teensy was
availability of high-speed USB data transfer
(https://www.pjrc.com/teensy/benchmark\_usb\_serial\_receive.html)
making them, apart from controlling machinery, well suited for data
acquisition tasks. The easiest way to program teensy microcontrollers is
to use the Arduino IDE
(download:https://www.arduino.cc/en/Main/Software). For the teensy
microcontrollers to be recognized by the Arduino IDE, one must
additionally install 'Teensyduino' (download:
https://www.pjrc.com/teensy/td\_download.html). Most of the Arduino
libraries are compatible with teensy.**

**As an easy-to-use two-way communication protocol between the
microcontroller and PD, OSC ('Open Sound Control',
https://www.opensoundcontrol.org) was implemented. (SFigure 4.5). In the
frontend control of PureData, the rotation movement of the individual of
motors is calculated. The specified number of steps is concomitantly
sent to the microcontroller, which in turn controls the motor driver via
the Step/Dir protocol.**

![SoftwareWorkflow.png](media/image11.png){width="6.3in"
height="1.0778248031496063in"}

**SFigure 4.5 Schematic diagram for operating and controlling the
system.**

**PureData can be downloaded from the PD community site
(https://puredata.info/downloads). For Mac or Win you should choose to
install PD-extended, which is pre-packaged with many additional
externals from the community (all necessary things needed for this
project should be installed per default). PD-extended is not actively
maintained any more, but still works well. Alternatively, PD-Vanilla can
be installed using externals via the 'deken'-plugin
(https://github.com/pure-data/deken) as required. On a Linux system,
'PD-L2ORK'
(http://l2ork.music.vt.edu/main/make-your-own-l2ork/software/), an
up-to-date, maintained and beautified version of PD-extended from the
'Linux Laptop Orchestra' (Virginia Tech Music Department) is applied.
Beta versions for Mac and Win are now also available. PD-L2ORK runs well
on Ubuntu, but also under Raspberry OS on Raspberry Pi Model 3 and 4.
This allows a small touchscreen interface to be used resulting in a
small-footprint solution.**

**We created a shell script (raspberry-setup.sh) to get a raspberry 3b/4
system to install all necessary programs. A copy of the git hub
repository is also created on the system. Alternatively, Arduino, Teensy
and Puredata can be installed manually on various OS. After the
necessary programs were installed, the firmware
(./files/delta\_microscope\_arduino/delta\_microscope\_arduino.ino) can
be uploaded to the microcontroller with the Arduino software.**

**The puredata programs (./files/delta\_microscope/delta\_microscope.pd)
together with a little helper-program for OSC
(./files/o.io.slipserial.pd) need to be in the same folder and can now
be opened it in PD-extended or PD-L2ORK.**

**The file 'delta\_microscope.pd' is the software front end and can
connect to the Arduino microcontroller. Typically, the USB port for the
first Arduino on an raspberry OS is "/dev/ttyACM0", on an windows system
its always "USB" followed up with a decimal number. After clicking on
"devices", the current ports are listed in the command window of
PureData. Now the appropriate connection can be opened by clicking on
"open x", where x is the corresponding port number. If needed, the
PureData program can be modified to fit the number by pressing "STRG +
E".**

**After successful connection and enabling of the system by pressing
both ON/OFF buttons, the computer-controllable stage can now be directed
to any wanted position with the JOG buttons.**

![software\_screenshot.PNG](media/image12.png){width="5.361111111111111in"
height="6.435416666666667in"}

**SFigure 4.6 Screenshot of the program.**

**Eventually the computer-controllable stage can be converted into an
automated microscope. Videomicroscope lenses could be incorporated at
the central position underneath the stage. We successfully used a
Raspberry HQ Camera v1.0 with SM1 to C-mount adapter (thorlabs, SM1A9)
to accommodate 1-inch optics connected to a Zeiss Plan 2.5 objective, as
well as a low-cost USB microscope camera with integrated 40x-1000x zoom
lenses.**

![opencv-python.jpeg](media/image13.jpeg){width="4.1311242344706915in"
height="3.5101859142607172in"}

**SFigure 4.7 The opencv python library can be used to process the image
of a printed 0.05 mm raster. After conversion to grayscale and edge
detection, horizontal and vertical lines are detected. The crossover of
a single picture can be saved as x/y coordinate.**

![Figure\_1.png](media/image14.png){width="5.3191021434820644in"
height="2.9900984251968503in"}

**SFigure 4.8 The automated stage can now be controlled via an
additional PureData program and a python script to run to different x/y
positions and back to the origin. After reaching the origin again, a
picture of a raster is taken and analyzed for the crossover. After
running the microscope to four different positions 100 times and back,
the resulting standard deviation is calculated by the system. While the
automated stage has a systematic error depending on the approaching
direction, the possibility to detect features can correct for that error
via this feedback.**
