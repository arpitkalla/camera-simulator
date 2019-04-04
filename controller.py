from rtree import index
import numpy as np
from target import Target
import json
import util

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
                self.idx.insert(i, (left, bottom, right, top))

if __name__ == "__main__":
    Controller("targets.json")