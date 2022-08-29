class Chord:
    def __init__(self, root, third, fifth, name):
        self.root = root
        self.third = third
        self.fifth = fifth
        self.name = name

    def get_chord(self):
        return [self.root, self.third, self.fifth]

    def get_root(self):
        return self.root

    def get_third(self):
        return self.third

    def get_fifth(self):
        return self.fifth

    def get_name(self):
        return self.name