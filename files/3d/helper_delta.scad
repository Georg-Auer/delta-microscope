//mini nema17-based delta
//printable on 120x120x120 trinus - max size possible
//and pumps to mount onto the scaffold
//===================================================

tolerance=0.2; //added tolerance at places needed to make 3d-printed part fit

//==================
//variables baseunit
//==================
base_r=31;//this is where the center-motorhole is located from abs center; adjusts size in xy; 31=min for nema17; this keeps all 'inside features' while making it easy to adjust outside wall via 'movewallfrombase_r'
movewallfrombase_r=29.5; //this variable moves the outside wall further from base_r (center motor holes)
height_all=100; //=height of delta-part
platethickness=12;//thickness of baseplate
reinforcementheight=30;//height above plate where hiwin-carriage is not cut out from wall
edge_y_distance=22; //distance of cylinders to form hull (inside-wall=edge_y_distance-wallthickness); use this variable to adjust wall behind sliders
wallthickness=9;//thickness of wall (grows to the inside)
edge_r=3;//'roundness' of edges
//M6 centerholes made so that hex-head is embedded
M6baseholes_r=3.3; //size of hole in center
M6_sinking_depth=7;//depth of access holes for M6 screws so that hex-head or nut is fully sunk
M6baseholeaccess_r=7;

motor_screw_diagonal = 44;//to mount nema17's 
middlemotor_r = 12; //radius of middle 'hole' of motors, big enough for 3d-printed couplers
M3_r=1.8;//a bit r added for not too tight holes to mount motors
motorscrews_access_r=4; //access_r for motor screws
motorscrews_access_heightbelowbaseplate=4; //how deep access holes go into baseplate
//subtract cylindrical shape from walls
//------------------------------------
cylinder_dia=45;
cylinder_length=100; //just that it easy to hit the wall for subtraction
wallheight_hole=-4;//mm above bottomplate where cylindrical cutout starts
cutout_r=33;//where from center cutout in wall will start
///variables hiwin
//----------------
M4_r=1.7; //r for screws, unfortunately imperial, therefore M3 screws must be used
M4_distance=12.5; //distance mounting holes, twice as many holes than in slider (25mm distance)
M4length=22; //length of screws
slide_width=14;//hiwin-slide=12mm +2mm space on each side
slide_thickness=8;//thickness hiwin-slide

slide_length=200;//length of hiwin-slides
move_slide_from_Zzero=-62.5; //move slider + screws above/below z-zero
slider_distance=22; //additional distance of slider from 'base-radius' base_r; take care if motors interfere
hiwin_carrierheight=5; //height of slider vs rail of hiwin from above
hiwin_carrier_width=28; //width of hiwin carrier (27mm+1)      
hiwin_carrier_thickness=10; //   

//===============
//variables TOP-Deltapart
//===============
delta_toplength=60;
delta_topwidth=20;
delta_topthickness=6;
delta_top_hole_r=17;
delta_top_wallthickness=8;

//=====================
//variables for slider
//=====================
height_slider = 80;//this defines where (height above plate) carriage is 
sliderwall=2;//thickness of wall around vertical holes
sliderpart_z_height=30;//height in z     
magnetdistance_to_sides=56; //USE THIS TO MAXIMISE MOVEMENT POSSIBLE + s_holder_r_in & s_holder_M6_r
magnetdistance_from_base_r=21; //distance in x from base_r to magnets   
M6_r=3.3; //+0.3 for 3d-printing

M6magnet_cutout_dia=6;//can put magnets lower, now commented out
M6magnet_cutout_height=7;//can put magnets lower, now commented out


bolt_distance_carrier=20; //distance holes on hiwin slider
carrier_screwlength=20;
screw_lengthinplastic=8;
sliderscrewaccess_r=3;
sliderscrewaccess_r_top=14.5;//r of cutout on top-screws connected on hiwin carrier

leadscrewnut_accessdia = 8.5; //leadscrewnut-nuts r=7.5 'leadscrewnut_top_bottom_r'

//========================
//variables for base plate
//========================
height_all_bottompart=20; //=height of delta-bottom_part
wallheight_hole_bottompart=5;//mm above bottomplate where cylindrical cutout starts
cylinder_dia_bottompart=60;
bottompart_base_correction=-8;//arbitrary value to adjust height of connection piece

//=======================================
//variables for drawing mechanical parts
//=======================================
//draw motors
motor_length = 48;
motor_width = 42;
motor_halfdiagonal = 0.5* sqrt(2*(motor_width*motor_width)); //half the diagonal of square area of motor, could be too big when edges of motor are rounded
//draw shafts, coupler, leadscrew and leadscrewnut
shaftcoupler_length = 52;//the usual red one
shaftcoupler_radius = 7.5;//the usual red one

leadscrew_length = 130; //~4" +approx height of shaft-coupler=42
leadscrew_radius = 3.05;
//dimensions thorlabs-nut
leadscrewnut_length = 9;
leadscrewnut_minradius = 5.15; //dia real = 9.5, 0.3mm tolerance added for 3d-printing
leadscrewnut_top_bottom_r=7.5;
leadscrewnut_top_bottom_thickness=4;
//=====================================

//==========================
//variables optics parts
//==========================

//point grey fireflyMV camera
//===========================
//main body
ptgrey_x=44;
ptgrey_y=34;
ptgrey_z=19.18;
//USB-port
ptgrey_x_USB=10; //check with caliper
ptgrey_y_USB=15; //check with caliper
ptgrey_z_USB=5.2;
//IO-port
ptgrey_x_IO=15; //check with caliper
ptgrey_y_IO=5; //check with caliper
ptgrey_z_IO=2; //too much, but like this easy to see...
IO_from_left_edge=33.49;
IO_from_top_edge=7.56;
//============================


//30mm-thorlabs-cage (e.g. mirror)
//================================
cageoptics_xy=38.3+2*tolerance;
cageoptics_z=38.3;
itemonside_xy=12;
itemonside_thickness=5+tolerance;
itemonfront_thickness=20;//takes away space for 1inch optics
itemonfront_width=34;//takes away space for 1inch optics  

//thorlabs c->1" adapter
c_to_1inch_adapter_r_outer=15.35;
c_to_1inch_adapter_r_inner=11.45;
c_to_1inch_adapter_height=4.4; 
// 1" optics tubes
tube1inch_outer_r=15.25;
tube1inch_inner_r=11.45;
// tube1
t1_tube1inch_length=80;
//tube2
t2_tube1inch_length=25.4;
//10xolympus_objective
olympus10x_parfocal_length=45.06;
olympus10x_parfocal_r=0.5;
olympus10x_body1_r=12; 
olympus10x_bodylength1=28;
olympus10x_body2_r=8;
olympus10x_bodylength2=32;
olympus10x_body3_r=5.25;
olympus10x_bodylength3=34;
//==============================
//variables optics ground plate
//=============================
//round part
optics_plate_r=37;//adjust this to fit well inside deltapart
optics_plate_z=12; //z-height of plate
optics_plate_z_high=optics_plate_z+cageoptics_z; //z-height of middle part
opticsplate_fixhole_r=29;

//brass-inserts to mount fixture
 M6insert_r=4.4;//4.5 good for holes across layers, but too big when holes are in other printing direction
 M6insert_height=14; //min 13.5mm
 insert_x=2;
 insert_y=30;
//connector-part to outside
optics_addpart1_x=15;//must be larger than wall-end of deltapart
optics_addpart1_y=24;//must fit to size of corresponding cylinder-cutout from deltapart 
optics_addpart_movex=30;//moves connector part in x, make it fit to the optics plate in delta
//outside part which serves to screw on bigger outside platform
optics_addpart2_x=25;
optics_addpart2_y=84;  

//=============================
//optics-plate - fixture on top
//=============================
opticsfixture_height=5;
opticsfixture_wallsize=3;
//====================
//optics ADDED plate
//====================
opticsaddedplate_x=87.5;
opticsaddedplate_y=112.5;  
holestepsize=12.5;


//==================================
//PLATFORM (slide-holder)-variables
//==================================
s_holder_height=14;
s_holder_r_out=48;
// MAX MOVEMENT ADJUSTMENT: s_holder_r_in & s_holder_M6_r & magnetdistance_to_sides
s_holder_r_in=35.5;//ADJUST THIS TO MAXIMISE MOVEMENT "when the objective crushes into platform" 
//to find best place for screws and the dimensions of the place iterate manually until both ECHO messages (or green and yellow inner circles match and are at max
s_holder_M6_r=28.5; //ADJUST THIS TO MAXIMISE MOVEMENT "where the hex-screws are" 
s_holder_FOV_r_outside=base_r+magnetdistance_from_base_r-s_holder_M6_r; //base for ECHO: diameter of movement possible from outside structure (one side: rods vertical)
s_holder_FOV_r_inside=s_holder_r_in-olympus10x_body1_r; //base for ECHO: diameter of movement possible from inside structure (ring and objective) 

s_holder_r_top=28;  //s_holder_r_in; //only needed to differ from s_holder_r_in if uscope slide is to small... 
s_holder_r_top_height=3;//holding structure smaller than air-gap between objective and sample

//carriage-platform connectors
//============================   
     magnet_r=5;//neodymium sphere radius
     hex_r=4.95;//hex-head_r 
     hex_height=5.85;//hex-head height
     magnet_in_hex_height=9.9;//measure this: when magnet is assembled in hex, where is its center, if hexhead-'bottom' = 0?

//===============================
//BEGIN KINEMATICS - Calculations
//===============================
x=-23.5; //x-coordinate; +/-23.5=max with current holder
y=-23.5; //y-coordinate; +/-23.5=max with current holder
z=0; //z-coordinate
L=70; //measure length of sticks (from magnet-center to magnet-center - L is defined above; right now 55.1
R=base_r+magnetdistance_from_base_r-s_holder_M6_r; //base_r+magnetdistance_from_base_r=where magnet on slider is from (x=0); s_holder_M6_r=where magnet on platform is from (x=0)     .....magnet_slider/magnet_carriage-distance in the x- plane on C-column 
Ax0=cos(30)*R;
Bx0=Ax0;

Ay0=cos(60)*R;
By0=Ay0;
Cy0=R;

A0= sqrt(L*L-(Ax0)*(Ax0)-(Ay0)*(Ay0)); //bottom left column; x,y=0,0
A= sqrt(L*L-(Ax0+x)*(Ax0+x)-(Ay0+y)*(Ay0+y)); //bottom left column

B0= sqrt(L*L-(Bx0)*(Bx0)-(By0)*(By0)); //bottom right column; x,y=0,0
B= sqrt(L*L-(Bx0-x)*(Bx0-x)-(By0+y)*(By0+y)); //bottom right column

C0= sqrt(L*L-(Cy0)*(Cy0)); //top column (in line with x); x,y=0,0
C= sqrt(L*L-x*x-(Cy0-y)*(Cy0-y)); //top column (in line with x)

echo("x=", x,"y=", y,"z=", z);
echo("L=", L,"R=", R);
echo("Ay0=", Ay0, "By0", By0, "Cy0=", Cy0);
echo("Ax0=", Ax0, "Bx0", Bx0);

echo("Bottom left column A0=",A0, "A=", A, "+z", z, "=", A+z, "travel_from_0=", A-A0);
echo("Bottom right column B0=", B0, "B=", B, "+z", z, "=", B+z, "travel_from_0=", B-B0);
echo("Top column C0=", C0,"C=", C, "+z", z, "=", C+z, "travel_from_0=", C-C0);

//===============================
//END KINEMATICS - Calculations
//===============================
//=================
//Pumps
//=================
     
//shared variables    
movepump_in_z=0;//moves pump with respect to delta assembly
movepump_in_x=64;//moves pump with respect to delta assembly....64 is close
spaceforsliders=12.5;//adjust this to make space for the slider
awayfrombaseline_x=40; //=change here to move center-line from bottom of pump
railawayfrombaseline_x=10;
p_sink_depth_for_nuts=6;//depth of access with screws to mount rail
pump_smallbottom=50; //play with this to make the cutout at the bottom the 'right' size (or vanish)
//variables motorpart
pump_mx=62;
pump_my=50;
motorpart_z=85;
spaceforcoupler_r=12;//r must be bigger than r of motorcoupler used
thickness_motormount=20;
//endstop
endstop_x=20.3;
endstop_y=14;
endstop_z=7;

//variables syringepart
//=====================
pump_sx=42;
pump_sy=pump_my;
syringepart_z=100; //total length of part: syringepart_z & length_of_syringeholder determine length of movement possible with pump
length_of_syringeholder=45; //length for syringe to sit on plastic
move_p_slide_from_Zzero=move_slide_from_Zzero;//here you can move hiwin-rail+screws up & down
//--------------------------------------------------------------------------------------------
leadscrewopening_r=6.5; //r for hole to accomodate end of leadscrew
s_cutout_awayfrombaseline_x=pump_sx; //center-height of cutout to harbor syringe
s_cutout_r=9; //r of cutout
add_thickness_to_hiwin_slider=1+2*tolerance; //add height to cutout so that slider can move a bit into part
screw_access_r=M6insert_r; //openings to screw syringepart to hiwin slide from top, also used to make space for M3-nuts at the very bottom of pump & used to fit M6-brass inserts in
//insert_holder_magnets 
    magnetinsertheight=5; //play with this to adjust height    
    syr_holder_magnet_r1=3.3;
    syr_holder_magnet_r1height=12; //too high so tht it cuts through so that access to rail is open
    syr_holder_magnet_r2=5.3;
    syr_holder_magnet_r2height=5;//rawn double to be sure it cuts everything  

//variables - syringe-holder-part1 - with magnets
//===============================================
s_holder_part1_thickness=4;//thickness of the part
move_s_holder_part1_in_x=60; //move the part in x  
//variables syringe-holder-part2 - the one with the M6-rods
//===============================================
s_holder_part2_thickness=4;//thickness of part
s_holder_part2_move_z=10; //move in z from syringe-part edge
s_holder_part2_cut=21;//cut the part over the slider=height of part

//variables pump_leadscrewpart
//============================
moveholesupforfixture=15;//moves M6 holes for syringeholder up/down
leadscrewpart_z=38;
pump_lx=44;
pump_ly=pump_my;
l_distance_from_bottom=18; //move the part towards desired height (so that it can slide nicely)
leadscrewnut_access_lpart=11; //hole to fit motorcoupler
p_hiwincarrier_access_r=M6insert_r; //must be big enough for screwdriver to fit & fit M6 brass inserts
p_move_carrier_screws_relative_to_part=-8; //this value moves all 4 screws to mount on hiwin-carrier up/down
p_height_slider=79;//moves part + leadscrewnut up/down

//variables syringe-holder Leadscrewpart
//======================================
leadscrewpart_syrholder_z=4;//thickness of part
leadscrewpart_syrholder_takeaway=25;//place where the part is cut in x




//variables 2mL-terumo-syringe
//=======================
//variables - with drawing, '0' will be the point between syr-cylinder and end-piece before plunger starts
syr_body_r=5;
syr_body_r2=5.25;
syr_body_r2_length=7;
syr_body_totallength=52.75;
syr_body_end_r=6.7;
syr_body_end_dist_between_r=6.6;   //20-2*6.7
syr_body_end_thickness=2.25;

syr_tip_r=2.25;
syr_tip_length=9;

syr_plunger_r=3; //approx r on the last 5mm of plunger
syr_plunger_end_r=6.25;
syr_plunger_end_thickness=1.3;

syr_plunger_length_min=10.5;
syr_plunger_length_max=52;
//========================================================
//========================================================

//=============================
//optics-plate - fixture on top
//=============================

translate ([0,0,optics_plate_z_high+platethickness+opticsfixture_height/2]){

difference (){
union (){    
hull (){
translate ([insert_x,-insert_y,0])     
cylinder(r = M6_r+opticsfixture_wallsize, h = opticsfixture_height, $fa=1, $fs=0.5);
translate ([insert_x,insert_y,0])     
cylinder(r = M6_r+opticsfixture_wallsize, h = opticsfixture_height, $fa=1, $fs=0.5);
translate ([0,0,0])     
cylinder(r = tube1inch_outer_r+4*tolerance+opticsfixture_wallsize, h = opticsfixture_height, $fa=1, $fs=0.5);    
}    
translate ([0,0,-opticsfixture_height/2])     
cylinder(r = tube1inch_outer_r+opticsfixture_wallsize, h = 2*opticsfixture_height, $fa=1, $fs=0.5);    
}
//make two holes for attaching holder-plate from top
          translate ([insert_x,-insert_y,0])     
          cylinder(r = M6_r, h = opticsfixture_height, $fa=1, $fs=0.5);
          translate ([insert_x,insert_y,0])     
          cylinder(r = M6_r, h = opticsfixture_height, $fa=1, $fs=0.5);
          translate ([0,0,-opticsfixture_height/2])     
          cylinder(r = tube1inch_outer_r+4*tolerance, h = 2*opticsfixture_height, $fa=1, $fs=0.5);
}}
