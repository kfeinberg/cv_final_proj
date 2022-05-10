frisbee_diameter = 18.5 # unit is inches
dt = .05
inches_to_meters = .0254

def get_physics_algo_speed(frisbee_pixel_width, centroid_pixel_dist):
    ppi = frisbee_pixel_width / frisbee_diameter
    world_centroid_dist = centroid_pixel_dist / ppi
    speed = world_centroid_dist / dt
    return speed * .0254 # current unit is meters/second