class Scale:
    def __init__(self, root_note, notes, chords):
        self.root_note = root_note
        self.notes = notes
        self.chords = chords

    def get_notes(self):
        return self.notes
