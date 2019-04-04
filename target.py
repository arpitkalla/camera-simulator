import generator
import matplotlib.pyplot as plt

class Target():
    def __init__(self, lat, lon, param, size):
        self.target_img = generator.create_target(shape=param["shape"],
                                        alpha=param["alpha"],
                                        shape_color=param["shape_color"],
                                        alpha_color=param["alpha_color"],
                                        orientation=param["orientation"],
                                        size=size)
        self.postion = [lat, lon]

    def _show(self):
        plt.imshow(self.target_img)
        plt.show()


if __name__ == "__main__":
    param = {
        "shape" : "triangle",
        "alpha" : "A",
        "shape_color" : "red",
        "alpha_color" : "orange",
        "orientation" : 60
    }
    t = Target(100,100,param, (100,100))
    t._show()


