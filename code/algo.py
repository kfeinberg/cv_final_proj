frisbee_diameter = 18.5

def get_distance(pixel_width, pixel_centroid_dist, dt):
    ppi = pixel_width / frisbee_diameter
    world_centroid_dist = pixel_centroid_dist / ppi # maybe multiply? idk
    speed = world_centroid_dist / dt
    return speed