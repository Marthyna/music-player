import music

parser = music.MusicParser()

input = 'Aaaa\nC Eee!aFa;Eaa'

stream = parser.parseInput(input)

# Save .MID file
fp = stream.write('midi', fp='test_output.mid')
