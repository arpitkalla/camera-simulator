import json
import numpy as np
from PIL import Image
from rtree import index

import util
from target import Target

class Controller():

    def __init__(self, json_file):
        self.targets = []
        self.idx = index.Index()

        with open(json_file) as target_json:
            target_data = json.load(target_json)
            for i, target in enumerate(target_data):
                t = Target(target["lat"], target["lon"], target, target["size"])
                self.targets.append(t)
                diff = util.feet_to_gps(t.size)/2
                left, bottom, right, top = (t.lon - diff, t.lat - diff, t.lon + diff, t.lat + diff)
                self.idx.insert(i, (left, bottom, right, top), obj=t)

        # Plane Telemetry
        self.x, self.y, self.z = 0.0, 0.0, 60.0

        # Gimbal Orientation
        self.roll, self.pitch, self.yaw = 0.0, 0.0, 0.0

        # Image resolution
        self.width, self.height = 200, 100

        # Camera Setting
        self.fov_x = 78 * np.pi / 180
        self.fov_y = np.arctan(self.height * np.tan(self.fov_x/2) / self.width) * 2

    def update_plane(self, x, y, z):
        self.x, self.y, self.z = x, y, z

    def update_gimbal(self, roll, pitch, yaw):
        self.roll, self.pitch, self.yaw = roll, pitch, yaw

    def update_camera(self, fov_x, fov_y):
        self.fov_x, self.fov_y = fov_x, fov_y

    def generate_image(self, points, target_size=300,color=(0, 255, 0, 255)):
        left, bottom, right, top = util.get_bouding_box(points)
        targets = self.idx.intersection((left, bottom, right, top), objects=True)
        
        if len(targets) == 0:
            img = Image.new('RGBA', (self.width, self.height), color)
            return img, False

        targets = sorted(targets)
        pixel_per_latlon = target_size/util.feet_to_gps(targets[0].size)
        width, height = right - left, bottom - top
        points[:,0] -= left
        points[:,1] -= top

        width *= pixel_per_latlon
        height *= pixel_per_latlon
        points*= pixel_per_latlon

        img = Image.new('RGBA', (width, height), color)
        for target in targets:
            offset = ((t.lon - left)*pixel_per_latlon, (t.lat - top)*pixel_per_latlon)
            target_img = t.create_target((target_size, target_size))
            img = util.compose(img, target_img, offset)

        return img, True

    def capture(self):
        ground_pts = util.get_points(self.x, self.y, self.z, 
                                     self.roll, self.pitch, self.yaw, 
                                     self.fov_x, self.fov_y)

        im, flag = self.generate_image(ground_pts)

        plt.imshow(im)
        plt.plot(pts[:,0], pts[:,1], "-")
        plt.plot(pts[0,0], pts[0,1], "ro")

        plt.plot(pts[3,0], pts[3,1], "go")
        plt.show()

        if flag:
            image_pts = np.array([[self.width, 0],
                                  [self.width, self.height], 
                                  [0, self.height], 
                                  [0,0]])

            h, status = cv2.findHomography(ground_pts, image_pts)
            im2 = cv2.warpPerspective(im, h, (self.width, self.height))
            return im2

        return im 

if __name__ == "__main__":
    Controller("targets.json")