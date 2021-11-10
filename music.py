
#================#
#    IMPORTS     #
#================#

# Internal imports
from note import *

# External imports
from music21 import stream as m21stream
from music21 import instrument as m21inst
from music21 import note as m21note

#================#
#   CONSTANTS    #
#================#

DEFAULT_MIDI_PROGRAM = 0
DEFAULT_VOLUME = 64
DEFAULT_OCTAVE = 4

MAX_MIDI_PROGRAM = 127
MAX_VOLUME = 127
MAX_OCTAVE = 8

VOGAIS = ['A', 'E', 'I', 'O', 'U']
DIGITOS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

#================#
#    CLASSES     #
#================#

class MusicParser:
    def __init__(self):
        self.last_state = None

        self.volume = DEFAULT_VOLUME
        self.octave = DEFAULT_OCTAVE
        self.midi_program = DEFAULT_MIDI_PROGRAM

    def parseInput(self, input: str):
        # A lista que vai conter as notas, silencios e instrumentos
        score = m21stream.Score()

        # Lista para lidar com cada instrumento
        current_inst = m21stream.Part()

        # Adiciona instrumento padrao
        current_inst.append(m21inst.instrumentFromMidiProgram(self.midi_program))


        self.last_state = None
        offset = -1

        print('= Input commands:')

        # Iterando sobre caracteres da entrada
        for char in input:
            offset += 1

            print(char) # debug

            print(offset)
            if str(char).upper() in VALID_NOTES:
                # A or a, B or b, C or c, ...

                if char in VALID_NOTES:
                    # A, B, C, ...
                    # Adiciona nota

                    # Não precisamos passar pela classe Note pra gerar uma nota
                    current_inst.insert(offset, m21note.Note(char, octave=self.octave))

                else:
                    # a, b, c, ...
                    if str(self.last_state).upper() in VALID_NOTES:
                        # Repete ultima nota
                        current_inst.insert(offset, m21note.Note(self.last_state, octave=self.octave))
                    else:
                        # Adiciona silencio
                        current_inst.insert(offset, m21note.Rest())

            elif char == ' ':
                # volume
                if self.volume != MAX_VOLUME:
                    aux_volume = 2*self.volume
                    if(aux_volume > MAX_VOLUME): aux_volume = MAX_VOLUME
                    self.volume = aux_volume

            elif char == '!':
                # Instrumento Agogo #114
                self.midi_program = 114

                score.append(current_inst)
                current_inst = m21stream.Part()
                current_inst.append(m21inst.instrumentFromMidiProgram(self.midi_program))

            elif str(char).upper() in VOGAIS:
                # Intrumento Harpischord #7
                self.midi_program = 7

                score.append(current_inst)
                current_inst = m21stream.Part()
                current_inst.append(m21inst.instrumentFromMidiProgram(self.midi_program))

            elif char in DIGITOS:
                # Instrumento por soma de valor
                aux_midi_prog = self.midi_program + int(char)
                if aux_midi_prog > MAX_MIDI_PROGRAM: aux_midi_prog = DEFAULT_MIDI_PROGRAM
                self.midi_program = aux_midi_prog

                score.append(current_inst)
                current_inst = m21stream.Part()
                current_inst.append(m21inst.instrumentFromMidiProgram(self.midi_program))

            elif char in ['?', '.'] :
                # Oitava ++
                aux_octave = self.octave + 1
                if aux_octave > MAX_OCTAVE: aux_octave = DEFAULT_OCTAVE
                self.octave = aux.octave

            elif char == '\n':
                # Instrumento Tubular Bells #15
                self.midi_program = 15

                score.append(current_inst)
                current_inst = m21stream.Part()
                current_inst.append(m21inst.instrumentFromMidiProgram(self.midi_program))

            elif char == ';':
                # Instrumento Pan Flute #76
                self.midi_program = 76

                score.append(current_inst)
                current_inst = m21stream.Part()
                current_inst.append(m21inst.instrumentFromMidiProgram(self.midi_program))

            elif char == ',':
                # Instrumento Church Organ #20
                self.midi_program = 20

                score.append(current_inst)
                current_inst = m21stream.Part()
                current_inst.append(m21inst.instrumentFromMidiProgram(self.midi_program))

            elif str(char).upper() not in VOGAIS:
                if str(self.last_state).upper() in VALID_NOTES:
                    # Repete ultima nota
                    current_inst.insert(offset, m21note.Note(self.last_state, octave=self.octave))
                else:
                    # Adiciona silencio
                    current_inst.insert(offset, m21note.Rest())

            else:
                if self.last_state.str.upper() in VALID_NOTES:
                    # Repete ultima nota
                    current_inst.insert(offset, m21note.Note(self.last_state, octave=self.octave))
                else:
                    # Adiciona silencio
                    current_inst.insert(offset, m21note.Rest())

            # Atualiza registro de ultimo estado
            self.last_state = char

        score.append(current_inst)

        print('\n= Output stream:')
        score.show('text')
        
        return score