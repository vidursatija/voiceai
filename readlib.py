from pyItunes import *
import json
from testLIBROSA import Songlysis

l = Library('iml.xml')

f = open('music_metadata.json', 'w')
list = []
count = 0
total_S_time = 0
for id, song in l.songs.items():
	if song:
		if song.disabled == None:
			song.location = "/run/media/vidur/Kachra/Music" + song.location[49:]
			energy, chroma, centroid, vocals, tempo = Songlysis.getFeatures(song.location)
			"""energy = -1
			vocals = -1
			tempo = -1
			chroma = -1
			centroid = -1"""
			list.append({"name" : str(song.name), "artist" : str(song.artist), "album" : str(song.album), 
				"genre" : str(song.genre), "location" : str(song.location),
				"energy" : energy, "vocals" : vocals, "tempo" : tempo, 
				"chroma" : chroma, "centroid" : centroid, "rating" : song.rating})
			#if song.total_time != None:
				#total_S_time = total_S_time + int(song.total_time)
			print(str(100/502) + "% Completed")
			#print(song.total_time)
			#break

#print(total_S_time)
print(len(list))
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
