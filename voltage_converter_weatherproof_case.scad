difference(){
    cube([24, 24, 48]);
    translate([2, 2, 2]){
        cube([20, 20, 48]);
    }
    translate([1, 1, 47]){
        cube([22, 22, 3]);
    }
}

translate([26, 0, 0]){
    difference(){
        cube([21, 21, 2]);
        translate([0, 8, -1]){
            cube([3, 3, 4]);
        }
        translate([3, 10.5, -1]){
            cylinder(r=1.5, h=4);
        }
    }
}