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
    
//===============
//begin Deltapart
//===============

//baseplate with holes    
//====================
//begin baseunit
//====================
difference (){ 
//make it    
hull (){
  for(turn0 = [0 : 120 : 360])
    rotate([0,0,turn0]){ 
     translate([base_r+movewallfrombase_r,edge_y_distance/2,0]) 
     cylinder(r = edge_r, h = height_all, $fa=1, $fs=0.5);
     translate([base_r+movewallfrombase_r,-edge_y_distance/2,0]) 
     cylinder(r = edge_r, h = height_all, $fa=1, $fs=0.5);
    }}
//subtract inside
hull (){
  for(turn1 = [0 : 120 : 360])
    rotate([0,0,turn1]){ 
     translate([base_r+movewallfrombase_r-wallthickness,edge_y_distance/2-wallthickness/2,platethickness]) 
     cylinder(r = edge_r, h = height_all, $fa=1, $fs=0.5);
     translate([base_r+movewallfrombase_r-wallthickness,-(edge_y_distance/2-wallthickness/2),platethickness]) 
     cylinder(r = edge_r, h = height_all, $fa=1, $fs=0.5);
    }}    
//end baseunit
//=============  

//subtractions: begin holes
//=========================
    
//turn everything        
for(turn = [0 : 120 : 360])
     rotate([0,0,turn]) 
     translate([base_r,0,0]){         
//M3 motor screws
  for(turn = [45 : 90 : 405])
     rotate([0,0,turn]){ 
     translate([motor_screw_diagonal/2,0,0])
     cylinder(r = M3_r, h = height_all, $fa=1, $fs=0.5);
     //access holes    
     translate([motor_screw_diagonal/2,0,platethickness-motorscrews_access_heightbelowbaseplate])    
     cylinder(r = motorscrews_access_r, h = height_all, $fa=1, $fs=0.5);    
     }    
//motor - middle hole
   cylinder(r = middlemotor_r, h = height_all, $fa=1, $fs=0.5);}   
//centerhole to fix optics plate
   cylinder(r = M6baseholes_r, h = height_all, $fa=1, $fs=0.5);
   translate ([0,0,-platethickness+M6_sinking_depth])
   cylinder(r = M6baseholeaccess_r, h = platethickness, $fa=1, $fs=0.5);
   //make three more
       
    for(turn = [60 : 120 : 420])
        rotate([0,0,turn]){  
        translate([opticsplate_fixhole_r,0,0])            
        cylinder(r = M6baseholes_r, h = platethickness, $fa=1, $fs=0.5);
        translate([opticsplate_fixhole_r,0,-platethickness+M6_sinking_depth])
        cylinder(r = M6baseholeaccess_r, h = platethickness, $fa=1, $fs=0.5);
        }     
   
//subtract hiwin-slides and make M4-holes
//=======================================
for(turn2 = [0 : 120 : 360])
     rotate([0,0,turn2]){ 
     //this is the rail   
     translate([base_r+slider_distance-2*tolerance,-(slide_width+2*tolerance)/2,move_slide_from_Zzero])       
     cube([slide_thickness+2*tolerance,slide_width+2*tolerance,slide_length],center=false);//2*tolerance added in width and towards center so that rail fits through baseplate, should not inflict with kinematics
     //cut out hiwin-carriage (drawn from top to bottom)
     translate([base_r+slider_distance-hiwin_carrierheight+2*tolerance,-hiwin_carrier_width/2,platethickness+reinforcementheight]) //tolerance added so that movement is smooth (not at slider of course to keep kinematics 'right')           
     cube([hiwin_carrier_thickness,hiwin_carrier_width,slide_length-platethickness],center=false);
     //these are the screws 
     for( M4hole = [0 : M4_distance : slide_length])    
     translate([base_r+slider_distance,0,M4hole+move_slide_from_Zzero])     
     rotate([0,90,0])    
     cylinder(r = M4_r, h = M4length, $fa=1, $fs=0.5);    
     }       
//subtract cylindrical shape from walls
//=====================================

for(turn = [60 : 120 : 420])
     rotate([0,0,turn]){ 
     hull (){    
     translate([cutout_r,0,height_all]) 
     rotate([0,90,0])        
     cylinder(r = cylinder_dia, h = cylinder_length, $fa=1, $fs=0.5);
     translate([cutout_r,0,wallheight_hole+platethickness+cylinder_dia]) 
     rotate([0,90,0])        
     cylinder(r = cylinder_dia, h = cylinder_length, $fa=1, $fs=0.5);}    
     }            
}
//===================================================
//===============
//begin TOP-Deltapart
//===============   
//====================
//begin baseunit
//====================
difference (){
union (){
difference (){ 
//make it    
hull (){
  for(turn0 = [0 : 120 : 360])
    rotate([0,0,turn0]){ 
     translate([base_r+movewallfrombase_r,edge_y_distance/2,height_all]) 
     cylinder(r = edge_r, h = move_slide_from_Zzero+slide_length-height_all, $fa=1, $fs=0.5);
     translate([base_r+movewallfrombase_r,-edge_y_distance/2,height_all]) 
     cylinder(r = edge_r, h = move_slide_from_Zzero+slide_length-height_all, $fa=1, $fs=0.5);
    }}
//subtract inside
hull (){
  for(turn1 = [0 : 120 : 360])
    rotate([0,0,turn1]){ 
     translate([base_r+movewallfrombase_r-wallthickness,edge_y_distance/2-wallthickness/2,height_all]) 
     cylinder(r = edge_r, h = move_slide_from_Zzero+slide_length-height_all, $fa=1, $fs=0.5);
     translate([base_r+movewallfrombase_r-wallthickness,-(edge_y_distance/2-wallthickness/2),height_all]) 
     cylinder(r = edge_r, h = move_slide_from_Zzero+slide_length-height_all, $fa=1, $fs=0.5);
    }}   
//end baseunit
//=============  
      
//subtract cylindrical shape from walls
//=====================================

for(turn = [60 : 120 : 420])
     rotate([0,0,turn]){ 
     hull (){    
     translate([cutout_r,0,move_slide_from_Zzero+slide_length]) 
     rotate([0,90,0])        
     cylinder(r = cylinder_dia, h = cylinder_length, $fa=1, $fs=0.5);
     translate([cutout_r,0,wallheight_hole+platethickness+cylinder_dia]) 
     rotate([0,90,0])        
     cylinder(r = cylinder_dia, h = cylinder_length, $fa=1, $fs=0.5);}    
     }            
}
//=======================
//unite additional stuff
//center_circle
translate([0,0,move_slide_from_Zzero+slide_length-delta_topthickness])     
cylinder(r = delta_top_hole_r+delta_top_wallthickness, h = delta_topthickness, $fa=1, $fs=0.5);

for(turn = [0 : 120 : 240])    
     rotate([0,0,turn]){ 
         //center-connectors
         translate([0,-delta_top_wallthickness/2,move_slide_from_Zzero+slide_length-delta_topthickness])
         cube([delta_toplength,delta_top_wallthickness,delta_topthickness],center=false);
         //structure around rail
    hull (){
        translate ([base_r+slider_distance, slide_width/2, move_slide_from_Zzero+slide_length-delta_topthickness])
        cylinder(r = delta_top_wallthickness/2, h = delta_topthickness, $fa=1, $fs=0.5);
        translate ([base_r+slider_distance, -slide_width/2, move_slide_from_Zzero+slide_length-delta_topthickness])
        cylinder(r = delta_top_wallthickness/2, h = delta_topthickness, $fa=1, $fs=0.5);
        
        translate ([base_r+movewallfrombase_r+edge_r-delta_top_wallthickness/2, slide_width/2, move_slide_from_Zzero+slide_length-delta_topthickness])
        cylinder(r = delta_top_wallthickness/2, h = delta_topthickness, $fa=1, $fs=0.5);
        translate ([base_r+movewallfrombase_r+edge_r-delta_top_wallthickness/2, -slide_width/2, move_slide_from_Zzero+slide_length-delta_topthickness])
        cylinder(r = delta_top_wallthickness/2, h = delta_topthickness, $fa=1, $fs=0.5);
        }  
     } 
}
//==========================
//take away rails and centerhole
//take away the rail
for(turn = [0 : 120 : 240])    
     rotate([0,0,turn]){ 
     translate([base_r+slider_distance-2*tolerance,-(slide_width+2*tolerance)/2,move_slide_from_Zzero])       
     #cube([slide_thickness+2*tolerance,slide_width+2*tolerance,slide_length],center=false);//2*tolerance added in width and towards center so that rail fits through baseplate, should not inflict with kinematics
     }
//take away middle hole
translate([0,0,move_slide_from_Zzero+slide_length-delta_topthickness])     
cylinder(r = delta_top_hole_r, h = delta_topthickness, $fa=1, $fs=0.5);          
}

//=================================================
//draw sliders
//=================================================          
for(turn0 = [0 : 120 : 360])
rotate([0,0,turn0]){ 
    
difference (){
hull (){    
//leadscrew_hole    
translate ([base_r, 0, height_slider])  
cylinder(r = leadscrewnut_minradius+sliderwall, h = sliderpart_z_height, $fa=1, $fs=0.5);
//attachment M6+magnets    
translate ([base_r+magnetdistance_from_base_r, magnetdistance_to_sides/2, height_slider])  
cylinder(r = M6_r+sliderwall, h = sliderpart_z_height, $fa=1, $fs=0.5);
translate ([base_r+magnetdistance_from_base_r, -magnetdistance_to_sides/2, height_slider])  
cylinder(r = M6_r+sliderwall, h = sliderpart_z_height, $fa=1, $fs=0.5);    
}  
//take away stuff
//---------------
//leadscrew-hole (size of leadscrew-nut)
translate ([base_r, 0, height_slider])  
cylinder(r = leadscrewnut_minradius, h = sliderpart_z_height, $fa=1, $fs=0.5);
translate ([base_r, 0, height_slider+leadscrewnut_length]) 
rotate([0,0,45])
cylinder(r = leadscrewnut_accessdia, h = sliderpart_z_height-leadscrewnut_length, $fa=1, $fs=0.5);

//M6-holes for hex-screws
translate ([base_r+magnetdistance_from_base_r, magnetdistance_to_sides/2, height_slider])  
cylinder(r = M6_r, h = sliderpart_z_height, $fa=1, $fs=0.5);
translate ([base_r+magnetdistance_from_base_r, -magnetdistance_to_sides/2, height_slider])  
cylinder(r = M6_r, h = sliderpart_z_height, $fa=1, $fs=0.5); 

//make M6-magnet assembly lower
/*
translate ([base_r+magnetdistance_from_base_r, magnetdistance_to_sides/2, height_slider+sliderpart_z_height-M6magnet_cutout_height])  
rotate([0,0,45])
cylinder(r = M6magnet_cutout_dia, h = M6magnet_cutout_height, $fa=1, $fs=0.5);
translate ([base_r+magnetdistance_from_base_r, -magnetdistance_to_sides/2, height_slider+sliderpart_z_height-M6magnet_cutout_height])  
rotate([0,0,45])
cylinder(r = M6magnet_cutout_dia, h = M6magnet_cutout_height, $fa=1, $fs=0.5);
*/

//cut out hiwin-carriage (drawn from top to bottom)
translate([base_r+slider_distance-hiwin_carrierheight-2*tolerance,-hiwin_carrier_width/2,platethickness])//2*tolerance added with cutout - 1*tolerance to balance out bigger print 0.3mm from deltapart where slider is mounted & 1*tolerance added to compensate for bigger size of sliderpart ===> WITHOUT THIS HIWIN-SLIDER AND THORLABS SCREWS ARE NOT PARALLEL!!!!       
cube([hiwin_carrier_thickness+2*tolerance,hiwin_carrier_width,slide_length-platethickness],center=false); //2*tolerance added in thickness so that all of part is still cut 

//holes for M3 screws to connect carriage to hiwin-carrier
//--------------------------------------------------------

//screw1
translate([base_r+slider_distance-hiwin_carrierheight,-bolt_distance_carrier/2,height_slider+sliderpart_z_height/2+bolt_distance_carrier/2])
rotate([0,-90,0])
cylinder(r = M3_r, h = carrier_screwlength, $fa=1, $fs=0.5);
//screw-access1
translate([base_r+slider_distance-hiwin_carrierheight-screw_lengthinplastic,-bolt_distance_carrier/2,height_slider+sliderpart_z_height/2+bolt_distance_carrier/2])
rotate([0,-90,0])
cylinder(r = sliderscrewaccess_r_top, h = base_r+slider_distance, $fa=1, $fs=0.5);

//screw2
translate([base_r+slider_distance-hiwin_carrierheight,+bolt_distance_carrier/2,height_slider+sliderpart_z_height/2+bolt_distance_carrier/2])
rotate([0,-90,0])
cylinder(r = M3_r, h = carrier_screwlength, $fa=1, $fs=0.5);
//screw-access2
translate([base_r+slider_distance-hiwin_carrierheight-screw_lengthinplastic,+bolt_distance_carrier/2,height_slider+sliderpart_z_height/2+bolt_distance_carrier/2])
rotate([0,-90,0])
cylinder(r = sliderscrewaccess_r_top, h = base_r+slider_distance , $fa=1, $fs=0.5);

}
}

//===============
//begin baseplate
//===============
   
//====================
//begin baseunit
//====================
translate ([0,0,-62.5])
difference (){ 
//make it    
hull (){
  for(turn0 = [0 : 120 : 360])
    rotate([0,0,turn0]){ 
     translate([base_r+movewallfrombase_r,edge_y_distance/2,0]) 
     cylinder(r = edge_r, h = height_all_bottompart, $fa=1, $fs=0.5);
     translate([base_r+movewallfrombase_r,-edge_y_distance/2,0]) 
     cylinder(r = edge_r, h = height_all_bottompart, $fa=1, $fs=0.5);
    }}
//subtract inside
hull (){
  for(turn1 = [0 : 120 : 360])
    rotate([0,0,turn1]){ 
     translate([base_r+movewallfrombase_r-wallthickness,edge_y_distance/2-wallthickness/2,0]) 
     cylinder(r = edge_r, h = height_all_bottompart, $fa=1, $fs=0.5);
     translate([base_r+movewallfrombase_r-wallthickness,-(edge_y_distance/2-wallthickness/2),0]) 
     cylinder(r = edge_r, h = height_all_bottompart, $fa=1, $fs=0.5);
    }}    
//end baseunit
//=============  

//subtractions: begin holes
//=========================   
//subtract hiwin-slides and make M4-holes
//=======================================
for(turn2 = [0 : 120 : 360])
     rotate([0,0,turn2]){ 
     //this is the rail   
     translate([base_r+slider_distance-2*tolerance,-(slide_width+2*tolerance)/2,move_slide_from_Zzero])       
     cube([slide_thickness+2*tolerance,slide_width+2*tolerance,slide_length],center=false);//2*tolerance added in width and towards center so that rail fits through baseplate, should not inflict with kinematics
     
     for( M4hole = [0 : M4_distance : slide_length])    
     translate([base_r+slider_distance,0,M4hole+move_slide_from_Zzero])     
     rotate([0,90,0])    
     cylinder(r = M4_r, h = M4length, $fa=1, $fs=0.5);    
     }       
//subtract cylindrical shape from walls
//=====================================

for(turn = [60 : 120 : 420])
     rotate([0,0,turn]){ 
     hull (){    
     translate([cutout_r,0,cylinder_dia_bottompart+bottompart_base_correction]) 
     rotate([0,90,0])
     rotate([0,0,45])         
     cylinder(r = cylinder_dia_bottompart, h = cylinder_length, $fn=4);
     }  
     }            
}



//slide-holder=PLATFORM
//=====================

echo (field_of_view_diameter_outside_yellow=s_holder_FOV_r_outside*2);
echo (field_of_view_diameter_inside_green=s_holder_FOV_r_inside*2);

translate([0,0,platethickness+optics_plate_z+cageoptics_z+t1_tube1inch_length+c_to_1inch_adapter_height+olympus10x_parfocal_length-s_holder_height])  //translate to focal point of optics
difference (){
//make the ring  
 
cylinder(r = s_holder_r_out, h = s_holder_height, $fa=1, $fs=0.5);
cylinder(r = s_holder_r_in, h = s_holder_height-s_holder_r_top_height, $fa=1, $fs=0.5);
cylinder(r = s_holder_r_top, h = s_holder_height, $fa=1, $fs=0.5);    
//show field of view  
color("green")    
cylinder(r = s_holder_FOV_r_inside, h = s_holder_height, $fa=1, $fs=0.5);
color("yellow")    
cylinder(r = s_holder_FOV_r_outside, h = s_holder_height, $fa=1, $fs=0.5);    

//make holes for magnets    
for(turn0 = [0 : 120 : 360])
rotate([0,0,turn0]){ 
//attachment M6+magnets    
translate ([s_holder_M6_r, magnetdistance_to_sides/2,0])  
cylinder(r = M6_r, h = s_holder_height, $fa=1, $fs=0.5);
translate ([s_holder_M6_r, -magnetdistance_to_sides/2,0])  
cylinder(r = M6_r, h = s_holder_height, $fa=1, $fs=0.5);        
}    
}
 

//=======================
//draw mechanical parts
//=======================

for(turn = [0 : 120 : 360])
     rotate([0,0,turn]){ 
 
     //motor   
     //===== 
     color ("black")    
     translate ([base_r,0,-motor_length/2])
     rotate([0,0,45])    
     cylinder(h = motor_length, r=motor_halfdiagonal, $fn=4, center=true);
   
     //shaftcoupler
     //=============    
     color ("orange")
     translate ([base_r,0,0 ])
     cylinder(r = shaftcoupler_radius, h = shaftcoupler_length, $fa=1, $fs=0.5); 
     
     //Leadscrew
     //==========    
     color ("silver")
     translate ([base_r,0,0])
     cylinder(r = leadscrew_radius, h = leadscrew_length, $fa=1, $fs=0.5); 
   
     //Leadscrewnut
     //============
     color ("orange"){
     translate ([base_r, 0, height_slider])  
     cylinder(r = leadscrewnut_minradius, h = leadscrewnut_length, $fa=1, $fs=0.5);
     //topnut
     //======    
     translate ([base_r, 0, height_slider+leadscrewnut_length])  
     cylinder(r = leadscrewnut_top_bottom_r, h = leadscrewnut_top_bottom_thickness, $fa=1, $fs=0.5); 
     //bottomnut
     //=========    
     translate ([base_r, 0, height_slider-leadscrewnut_top_bottom_thickness])  
     cylinder(r = leadscrewnut_top_bottom_r, h = leadscrewnut_top_bottom_thickness, $fa=1, $fs=0.5);

     //rail
     //====    
     color ("orange")   
     translate([base_r+slider_distance,-slide_width/2,move_slide_from_Zzero])       
     cube([slide_thickness,slide_width,slide_length],center=false);     
        
     //carriage-platform connectors
     //============================
     
     color ("orange") { 
     //hex-heads on carriages  
     //-----------------------    
     translate ([base_r+magnetdistance_from_base_r, magnetdistance_to_sides/2, height_slider+sliderpart_z_height])  
     cylinder(r = hex_r, h = hex_height, $fa=1, $fs=0.5);
     translate ([base_r+magnetdistance_from_base_r, -magnetdistance_to_sides/2, height_slider+sliderpart_z_height])  
     cylinder(r = hex_r, h = hex_height, $fa=1, $fs=0.5);  
     //hex-heads on platform
     translate ([s_holder_M6_r, magnetdistance_to_sides/2,platethickness+optics_plate_z+cageoptics_z+t1_tube1inch_length+c_to_1inch_adapter_height+olympus10x_parfocal_length-s_holder_height-hex_height]) 
     cylinder(r = hex_r, h = hex_height, $fa=1, $fs=0.5); 
      translate ([s_holder_M6_r, -magnetdistance_to_sides/2,platethickness+optics_plate_z+cageoptics_z+t1_tube1inch_length+c_to_1inch_adapter_height+olympus10x_parfocal_length-s_holder_height-hex_height]) 
     cylinder(r = hex_r, h = hex_height, $fa=1, $fs=0.5);      
     }
     //make the sticks
     //===============
     //first side
     //----------
     hull (){
     //on carriage    
     translate ([base_r+magnetdistance_from_base_r, magnetdistance_to_sides/2, height_slider+sliderpart_z_height+magnet_in_hex_height])   
     sphere (magnet_r, $fa=1, $fs=0.5);
     //on platform 
     translate ([s_holder_M6_r, magnetdistance_to_sides/2,platethickness+optics_plate_z+cageoptics_z+t1_tube1inch_length+c_to_1inch_adapter_height+olympus10x_parfocal_length-s_holder_height-magnet_in_hex_height])  
      sphere (magnet_r, $fa=1, $fs=0.5);} 
      //other side
      //----------
      hull (){
     //on carriage    
     translate ([base_r+magnetdistance_from_base_r, -magnetdistance_to_sides/2, height_slider+sliderpart_z_height+magnet_in_hex_height])   
     sphere (magnet_r, $fa=1, $fs=0.5);
     //on platform 
     translate ([s_holder_M6_r, -magnetdistance_to_sides/2,platethickness+optics_plate_z+cageoptics_z+t1_tube1inch_length+c_to_1inch_adapter_height+olympus10x_parfocal_length-s_holder_height-magnet_in_hex_height])  
      sphere (magnet_r, $fa=1, $fs=0.5);}    
 
 

}}
//================================================================ 
// draw OPTICS
//================================================================
/*
translate ([0,0,platethickness]){//translates all of optics plate
//====================
//optics ground plate
//====================
color ("yellow")  
difference (){
    union (){
    //make round part
    cylinder(r = optics_plate_r, h = optics_plate_z_high, $fa=1, $fs=0.5);
    //add platepart that holds optics outside of delta-geometry
    //part1-connector to outside of deltapart    
    translate([-optics_addpart1_x-optics_addpart_movex,-optics_addpart1_y/2,0])
    cube([optics_addpart1_x,optics_addpart1_y,optics_plate_z],center=false);
    //part2 outside of deltapart
    translate([-optics_addpart2_x-optics_addpart1_x-optics_addpart_movex,-optics_addpart2_y/2,0])
    cube([optics_addpart2_x,optics_addpart2_y,optics_plate_z],center=false);    
    }   
    //subtractions start here
    //========================
    //part2 'outside' - make connector holes to add additional big plate for optics
    //middle hole
        translate([optics_addpart2_x/2-optics_addpart2_x-optics_addpart1_x-cutout_r,0,0])           
        cylinder(r = M6baseholes_r, h = optics_plate_z, $fa=1, $fs=0.5);
        translate([optics_addpart2_x/2-optics_addpart2_x-optics_addpart1_x-cutout_r,0,optics_plate_z-M6_sinking_depth]) 
        cylinder(r = M6baseholeaccess_r, h = optics_plate_z, $fa=1, $fs=0.5);
    //left hole
        translate([optics_addpart2_x/2-optics_addpart2_x-optics_addpart1_x-cutout_r,optics_addpart2_y/3,0])           
        cylinder(r = M6baseholes_r, h = optics_plate_z, $fa=1, $fs=0.5);
        translate([optics_addpart2_x/2-optics_addpart2_x-optics_addpart1_x-cutout_r,optics_addpart2_y/3,optics_plate_z-M6_sinking_depth]) 
        cylinder(r = M6baseholeaccess_r, h = optics_plate_z, $fa=1, $fs=0.5);
    //right hole
        translate([optics_addpart2_x/2-optics_addpart2_x-optics_addpart1_x-cutout_r,-optics_addpart2_y/3,0])           
        cylinder(r = M6baseholes_r, h = optics_plate_z, $fa=1, $fs=0.5);
        translate([optics_addpart2_x/2-optics_addpart2_x-optics_addpart1_x-cutout_r,-optics_addpart2_y/3,optics_plate_z-M6_sinking_depth]) 
        cylinder(r = M6baseholeaccess_r, h = optics_plate_z, $fa=1, $fs=0.5);
    //round part - take away stuff so that part fits inside (using wall-cutouts from delta-part)
    //subtract cylindrical shape from walls
    //======================================

     for(turn = [300 : 120 : 420])
        rotate([0,0,turn]){ 
        hull (){    
           translate([cutout_r,0,wallheight_hole+cylinder_dia]) 
           rotate([0,90,0])        
           cylinder(r = cylinder_dia, h = cylinder_length, $fa=1, $fs=0.5);
        }    
     } 
    //make holes for motors
    for(turn = [0 : 120 : 360])
     rotate([0,0,turn]) 
     translate([base_r,0,0]){ 
     cylinder(r = middlemotor_r, h = height_all, $fa=1, $fs=0.5);}  
    //make screwholes to fix delta part and optics plate together    
    //make centerhole
    cylinder(r = M6baseholes_r, h = optics_plate_z_high, $fa=1, $fs=0.5);
    translate([0,0,optics_plate_z-M6_sinking_depth])
    cylinder(r = M6baseholeaccess_r, h = optics_plate_z_high, $fa=1, $fs=0.5);
    //make three more
    for(turn = [60 : 120 : 420])
        rotate([0,0,turn]){  
        translate([opticsplate_fixhole_r,0,0])            
        cylinder(r = M6baseholes_r, h = optics_plate_z_high, $fa=1, $fs=0.5);
        translate([opticsplate_fixhole_r,0,optics_plate_z-M6_sinking_depth])
        cylinder(r = M6baseholeaccess_r, h = optics_plate_z_high, $fa=1, $fs=0.5);
        }
     //subtract optics-cage from middle plate - on front and back all stuff is additionally removed to allow for 1"-tube access
        union (){    
          translate ([-cageoptics_xy/2,-cageoptics_xy/2,optics_plate_z])     
          cube([cageoptics_xy,cageoptics_xy,cageoptics_z],center=false);
          translate ([-itemonside_xy/2,cageoptics_xy/2,optics_plate_z])     
          cube([itemonside_xy,itemonside_thickness,cageoptics_z],center=false); 
          translate ([cageoptics_xy/2,-itemonfront_width/2,optics_plate_z])     
          cube([itemonfront_thickness,itemonfront_width,cageoptics_z],center=false); 
          translate ([-cageoptics_xy/2-itemonfront_thickness,-itemonfront_width,optics_plate_z])     
          cube([itemonfront_thickness,2*itemonfront_width,cageoptics_z],center=false);     
      
      //make two holes for attaching holder-plate from top
          translate ([insert_x,-insert_y,optics_plate_z_high-M6insert_height])     
          cylinder(r = M6insert_r, h = M6insert_height, $fa=1, $fs=0.5);
          translate ([insert_x,insert_y,optics_plate_z_high-M6insert_height])     
          cylinder(r = M6insert_r, h = M6insert_height, $fa=1, $fs=0.5);      
 

//subtract sliders down to bottom plate - one should make a module from sliders
for(turn0 = [0 : 120 : 360])
rotate([0,0,turn0]){ 
hull (){    
//leadscrew_hole    
translate ([base_r,0,optics_plate_z])  
cylinder(r = leadscrewnut_minradius+sliderwall+8*tolerance, h = optics_plate_z_high, $fa=1, $fs=0.5);
//attachment M6+magnets    
translate ([base_r+magnetdistance_from_base_r, magnetdistance_to_sides/2, optics_plate_z])  
cylinder(r = M6_r+sliderwall+8*tolerance, h = optics_plate_z_high, $fa=1, $fs=0.5);
translate ([base_r+magnetdistance_from_base_r, -magnetdistance_to_sides/2, optics_plate_z])  
cylinder(r = M6_r+sliderwall+8*tolerance, h = optics_plate_z_high, $fa=1, $fs=0.5);    
}}
}
}}
//end of optics-groundplate
//==========================
//=============================
//optics-plate - fixture on top
//=============================
/*
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
*/

//====================
//optics ADDED plate
//====================
/*
translate ([0,0,0]){//translates all of optics plate    
//color ("yellow")  
difference (){
    union (){
    //part2 outside of deltapart
    translate([-optics_addpart2_x-optics_addpart1_x-optics_addpart_movex,-optics_addpart2_y/2,0])
    cube([optics_addpart2_x,optics_addpart2_y,optics_plate_z],center=false); 
    //added plate    
    translate ([-opticsaddedplate_x-optics_addpart2_x-optics_addpart1_x-optics_addpart_movex,-opticsaddedplate_y/2,0])    
    cube([opticsaddedplate_x,opticsaddedplate_y,2*optics_plate_z],center=false);     
    }
    //SUBTRACTIONS
    //CONNECTOR HOLES
        translate([optics_addpart2_x/2-optics_addpart2_x-optics_addpart1_x-cutout_r,0,0])           
        cylinder(r = M6baseholes_r, h = optics_plate_z, $fa=1, $fs=0.5);
        translate([optics_addpart2_x/2-optics_addpart2_x-optics_addpart1_x-cutout_r,0,0]) 
        cylinder(r = M6baseholeaccess_r, h = M6_sinking_depth, $fa=1, $fs=0.5);
    //left hole
        translate([optics_addpart2_x/2-optics_addpart2_x-optics_addpart1_x-cutout_r,optics_addpart2_y/3,0])           
        cylinder(r = M6baseholes_r, h = optics_plate_z, $fa=1, $fs=0.5);
        translate([optics_addpart2_x/2-optics_addpart2_x-optics_addpart1_x-cutout_r,optics_addpart2_y/3,0]) 
        cylinder(r = M6baseholeaccess_r, h = M6_sinking_depth, $fa=1, $fs=0.5);
    //right hole
        translate([optics_addpart2_x/2-optics_addpart2_x-optics_addpart1_x-cutout_r,-optics_addpart2_y/3,0])           
        cylinder(r = M6baseholes_r, h = optics_plate_z, $fa=1, $fs=0.5);
        translate([optics_addpart2_x/2-optics_addpart2_x-optics_addpart1_x-cutout_r,-optics_addpart2_y/3,0]) 
        cylinder(r = M6baseholeaccess_r, h = M6_sinking_depth, $fa=1, $fs=0.5);
    //M6_thorlabs-compatible holes
    translate ([-optics_addpart2_x-optics_addpart1_x-optics_addpart_movex, -opticsaddedplate_y/2+holestepsize, 0]){
    //rows in y
    for(step = [0 : holestepsize : opticsaddedplate_y-2*holestepsize ])
    translate ([0,step,0]){    
    //holes in x    
    for(step = [holestepsize : holestepsize : opticsaddedplate_x-holestepsize ])
    translate ([-step,0,0]){    
    #cylinder(r = M6_r, h = 2*optics_plate_z, $fa=1, $fs=0.5); 
    cylinder(r = M6baseholeaccess_r, h = M6_sinking_depth, $fa=1, $fs=0.5); 
    } } } } }   

translate ([0,0,optics_plate_z]){
*/
//translates everything optics    
//=========
//draw cage
//=========   
/*
    
rotate ([0,0,0]) 
color ("cyan") 
union (){    
translate ([-cageoptics_xy/2,-cageoptics_xy/2,optics_plate_z])     
cube([cageoptics_xy,cageoptics_xy,cageoptics_z],center=false);
translate ([-itemonside_xy/2,cageoptics_xy/2,optics_plate_z])     
cube([itemonside_xy,itemonside_thickness,cageoptics_z],center=false); 
 
}

//vertical
//========        
//vertical 1inch optics tube2
color ("orange")
translate ([-cageoptics_xy/2,0,cageoptics_z/2+optics_plate_z])
rotate ([0,-90,0])
difference (){ 
cylinder(r = tube1inch_outer_r, h = t2_tube1inch_length, $fa=1, $fs=0.5);
cylinder(r = tube1inch_inner_r, h = t2_tube1inch_length, $fa=1, $fs=0.5);} 

// draw Firefly-MV camera
translate ([-(cageoptics_xy/2+t2_tube1inch_length+ptgrey_z),0,cageoptics_z/2+optics_plate_z]){
rotate ([-90,0,-90])
color ("cyan")    
union (){    
//main camera body 
translate ([-ptgrey_x/2,-ptgrey_y/2,0])
cube([ptgrey_x,ptgrey_y,ptgrey_z],center=false);
//USB-port    
translate ([-ptgrey_x/2,-ptgrey_y_USB/2,-ptgrey_z_USB])
cube([ptgrey_x_USB,ptgrey_y_USB,ptgrey_z_USB],center=false);
//IO-port    
translate ([-ptgrey_x_IO/2-ptgrey_x/2+IO_from_left_edge,-ptgrey_y_IO/2+ptgrey_y/2-IO_from_top_edge,-ptgrey_z_IO])
cube([ptgrey_x_IO,ptgrey_y_IO,ptgrey_z_IO],center=false);   
//c-mount to 1inch optics adapter
translate ([-0,0,ptgrey_z])
difference (){ 
cylinder(r = c_to_1inch_adapter_r_outer, h = c_to_1inch_adapter_height, $fa=1, $fs=0.5);
cylinder(r = c_to_1inch_adapter_r_inner, h = c_to_1inch_adapter_height, $fa=1, $fs=0.5);}   
}}


//horizontal
//==========
//1inch optics tube1
color ("orange")
translate ([-0,0,optics_plate_z+cageoptics_z])
difference (){ 
cylinder(r = tube1inch_outer_r, h = t1_tube1inch_length, $fa=1, $fs=0.5);
cylinder(r = tube1inch_inner_r, h = t1_tube1inch_length, $fa=1, $fs=0.5);} 
//RMS-mount to 1inch optics adapter (same like c-mount adapter)
color ("cyan")
translate ([-0,0,optics_plate_z+cageoptics_z+t1_tube1inch_length])
difference (){ 
cylinder(r = c_to_1inch_adapter_r_outer, h = c_to_1inch_adapter_height, $fa=1, $fs=0.5);
cylinder(r = c_to_1inch_adapter_r_inner, h = c_to_1inch_adapter_height, $fa=1, $fs=0.5);}
    
//10xolympus_objective
color ("orange"){
translate ([0,0,optics_plate_z+cageoptics_z+c_to_1inch_adapter_height+t1_tube1inch_length])
union (){ 
cylinder(r = olympus10x_body1_r, h = olympus10x_bodylength1, $fa=1, $fs=0.5);
cylinder(r = olympus10x_body2_r, h = olympus10x_bodylength2, $fa=1, $fs=0.5);
cylinder(r = olympus10x_body3_r, h = olympus10x_bodylength3, $fa=1, $fs=0.5);
cylinder(r = olympus10x_parfocal_r, h = olympus10x_parfocal_length, $fa=1, $fs=0.5);} 
}

}

*/
