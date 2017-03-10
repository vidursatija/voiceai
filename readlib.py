from pyItunes import *
import json

l = Library('iml.xml')

f = open('music_metadata.json', 'w')
list = []
for id, song in l.songs.items():
	if song:
		list.append({"name" : str(song.name), "artist" : str(song.artist), "album" : str(song.album), "genre" : str(song.genre), "location" : str(song.location), "time_sig" : -1, "energy" : -1, "tempo" : -1, "mode" : -1, "key" : -1, "duration" : -1, "loudness" : 1, "dance" : -1, "rating" : song.rating})

json.dump(list, f)
"""
list.sort(key=lambda tup:tup[0])
prevArtist = ""
prevAlbum = ""
for songs in list:
	artistName = songs[1]
	songName = songs[2]
	albumName = songs[0]
	
	albumWords = albumName.split()
	songWords = songName.split()
	artistWords = artistName.split()
	if prevArtist == artistName:
		if prevAlbum != albumName:
			prevAlbum = albumName
			
			for aw in albumWords:
				f.write(aw)
				f.write('\tART\n')
			f.write('\n')
		
		for aw in songWords:
			f.write(aw)
			f.write('\tART\n')
		f.write('\n')

	else:
		for aw in artistWords:
			f.write(aw)
			f.write('\tPER\n')
		f.write('\n')
		prevArtist = artistName
	"""
f.close()
