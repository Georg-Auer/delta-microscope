magnetdistance_to_sides=56; //USE THIS TO MAXIMISE MOVEMENT POSSIBLE + s_holder_r_in & s_holder_M6_r
magnetdistance_from_base_r=21; //distance in x from base_r to magnets   
M6_r=3.3; //+0.3 for 3d-printing

M6magnet_cutout_dia=6;//can put magnets lower, now commented out
M6magnet_cutout_height=7;//can put magnets lower, now commented out

s_holder_r_top=28;  //s_holder_r_in; //only needed to differ from s_holder_r_in if uscope slide is to small... 
s_holder_r_top_height=3;//holding structure smaller than air-gap between objective and sample

s_holder_height=14;
s_holder_r_out=58;
// MAX MOVEMENT ADJUSTMENT: s_holder_r_in & s_holder_M6_r & magnetdistance_to_sides
// s_holder_r_in=35.5 in original size
s_holder_r_in=5.5;//ADJUST THIS TO MAXIMISE MOVEMENT "when the objective crushes into platform" 
//to find best place for screws and the dimensions of the place iterate manually until both ECHO messages (or green and yellow inner circles match and are at max
s_holder_M6_r=28.5; //ADJUST THIS TO MAXIMISE MOVEMENT "where the hex-screws are" 

/*
//make cylindical platform
difference (){
cylinder(r = s_holder_r_out, h = s_holder_height, $fa=1, $fs=0.5);
cylinder(r = s_holder_r_in, h = s_holder_height-s_holder_r_top_height, $fa=1, $fs=0.5);
cylinder(r = s_holder_r_top, h = s_holder_height, $fa=1, $fs=0.5);  

for(turn0 = [0 : 120 : 360])
rotate([0,0,turn0]){
//attachment M6+magnets    
translate ([s_holder_M6_r, -magnetdistance_to_sides/2,0])  
cylinder(r = M6_r, h = s_holder_height, $fa=1, $fs=0.5);
translate ([s_holder_M6_r, magnetdistance_to_sides/2,0])  
cylinder(r = M6_r, h = s_holder_height, $fa=1, $fs=0.5);
}
}

*/

//tolerance due to fff printing method
tolerance = 0.2;
slide_tolerance = 0.1;

//to avoid the need for supports during printing:
slide_holder_overhang = 5;

//size of an typical slide
// slide 2 is unused 
single_slide_lenght_1 = 85+tolerance;
single_slide_lenght_2 = 75+tolerance;
single_slide_width_1 = 29.7+tolerance;
single_slide_width_2 = 25+tolerance;

ring_widening = 5;

//create slide holding platform
color("red"){
translate ([0,0,20]){
difference(){

union(){



for(turn0 = [0 : 120 : 360])
rotate([0,0,turn0]){
//attachment poles    
translate ([s_holder_M6_r, -magnetdistance_to_sides/2,0])
cylinder(r = M6_r-tolerance, h = s_holder_height/8, $fa=1, $fs=0.5);
translate ([s_holder_M6_r, magnetdistance_to_sides/2,0])  
cylinder(r = M6_r-tolerance, h = s_holder_height/8, $fa=1, $fs=0.5);
}
translate ([0,0,s_holder_height/8])

//platform
difference(){
cylinder(r = s_holder_r_out+ring_widening, h = s_holder_height/8, $fa=1, $fs=0.5);
cylinder(r = s_holder_r_in, h = s_holder_height-s_holder_r_top_height, $fa=1, $fs=0.5);
cylinder(r = s_holder_r_top, h = s_holder_height, $fa=1, $fs=0.5);




}
}//end of union

// single slide frame
/*
rotate([0,0,15]){
cube(size = [single_slide_lenght_1,single_slide_width_1,s_holder_height], center = true);
}
rotate([0,0,-15]){
cube(size = [single_slide_lenght_2,single_slide_width_2,s_holder_height], center = true);
}
*/
// double slide frame
cube(size = [single_slide_width_1*2+slide_tolerance,single_slide_lenght_1+slide_tolerance,s_holder_height], center = true);
}
}
}