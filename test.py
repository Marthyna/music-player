import music

parser = music.MusicParser()

# input = 'A.A.A...A\nC Ee e!aFa;Eaa'
input = '7E. G.... E.. G;...FCG .G'
# input = '7E. G.... E.. ;G...FCG .G'
# input = f'\nA. G.... E.. ;G...FCG .G'

song = parser.parseInput(input, debug=True)
# song = parser.parseInput(input)

# Save .MID file
fp = song.write('midi', fp='test_output.mid')
print(f'\n= Saved as {fp}')
