import json
import generator
import matplotlib.pyplot as plt

class Target():
    def __init__(self, lat, lon, param, size):
        self.lat = lat
        self.lon = lon
        self.size = size
        self.param = param

    def create(self, size):
        self.target_img = generator.create_target(shape=self.param["shape"],
                                        alpha=self.param["alpha"],
                                        shape_color=self.param["shape_color"],
                                        alpha_color=self.param["alpha_color"],
                                        orientation=self.param["orientation"],
                                        size=size)

    def _show(self):
        plt.imshow(self.target_img)
        plt.show()


if __name__ == "__main__":

    with open("targets.json") as target_json:
        targets = json.load(target_json)
        for target in targets:
            t = Target(target["lat"], target["lon"], target, (200, 200))
            t._show()


# 10,000/90 * 3280.4