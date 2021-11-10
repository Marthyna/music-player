import music21

VALID_NOTES = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

class Note:
    def __init__(self, sound, name):
        self.sound = sound
        self.name = name
