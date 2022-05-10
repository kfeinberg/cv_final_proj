import math

frisbee_diameter = 18.5 # unit is inches
dt = .05
inches_to_meters = .0254

def get_physics_algo_speed(frisbee_pixel_width, centroid1, centroid2):
    ppi = frisbee_pixel_width / frisbee_diameter
    centroid_pixel_dist = math.sqrt( ((centroid1[0]-centroid2[0])**2)+((centroid1[1]-centroid2[1])**2))

    world_centroid_dist = centroid_pixel_dist / ppi
    speed = world_centroid_dist / dt
    return speed * .0254 # current unit is meters/second