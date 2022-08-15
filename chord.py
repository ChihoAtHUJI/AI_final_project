class Chord:
    def __init__(self, root, third, fifth):
        self.root = root
        self.third = third
        self.fifth = fifth

    def get_chord(self):
        return [self.root, self.third, self.fifth]

    def get_root(self):
        return self.root