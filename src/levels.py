'''
    levels.py

    load levels from either a Blender model or a Level object
        Level object can store data for making a level using assets
        stored in assets.py

    custom level generator for making levels to put into the game
        or for users to create their own maps
    
'''

class LevelLoader:
    def __init__(self, level=""):
        if level:
            self.load(level)
    def load(self, level):
        with open(level, "r") as f:
            for line in f.readlines():
                self.parse(line)
    def parse(self, line):
        try:
            asset = int(line[:3])
            x = int(line[3:6])
            y = int(line[6:9])
            z = int(line[9:12])
        except Exception as e:
            print("Error {e}: failed to parse level {lv}.".format(
                lv=self.level,e=e))

class LevelEditor:
    pass
