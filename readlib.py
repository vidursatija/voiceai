from pyItunes import *
import json
from testLIBROSA import Songlysis
import pickle
import multiprocessing as mp
import numpy as np

l = Library('iml.xml')

f = open('music_metadata.json', 'w')
songs_item = [song for id,song in l.songs.items()]

def returnPartialList(startIndex, song_items, parts):
	lists = []
	count = 1
	for index in range(startIndex, min(startIndex+parts, len(song_items))):
		song = song_items[index]
		if song:
			if song.disabled != None or song.movie != None or song.has_video != None or song.podcast != None:
				continue
			else:
				if song.genre != None and song.genre == 'iTunes U':
					continue
				try:
					song.location = "/run/media/vidur/Kachra/Music" + song.location[49:]
					energy, chroma, centroid, vocals, tempo = Songlysis.getFeatures(song.location)
					"""energy = -1
					vocals = -1
					tempo = -1
					chroma = -1
					centroid = -1"""
				except Exception as e:
					print("Error1 occured at this song" + str(e) + str(song.location))
					continue
				
				try:
					lists.append({"name" : str(song.name), "artist" : str(song.artist), "album" : str(song.album), 
						"genre" : str(song.genre), "location" : str(song.location),
						"energy" : float(energy), "vocals" : float(vocals), "tempo" : float(tempo), 
						"chroma" : float(chroma), "centroid" : float(centroid), "rating" : song.rating})
				except Exception as e:
					print("Error2 occured at this song" + str(e) + str(song.location))
					continue
				
				try:	
					print(str(count) + " Completed")
					count = count + 1
				except Exception as e:
					print("Error3 occured at this song" + str(e) + str(song.location))

				continue

	return lists

total_list = returnPartialList(0, songs_item, 700)
"""
pool = mp.Pool(processes=2)
results = [pool.apply_async(returnPartialList, args=(x, songs_item, 350,)) for x in [0, 350]]
listk = [p.get() for p in results]

total_list = []
for small_list in listk:
	total_list = total_list + small_list
"""
"""
inputs = tuple(range(0, 4))
jobs = [(input, job_server.submit(returnPartialList,(input,song_items,), (), () )) for input in inputs]
for input, job in jobs:
    listk = listk + [job()]
"""
#list = returnPartialList(675)
"""
try:
	listk = np.reshape(listk, total_songs)
except Exception as e:
	print("Reshape error" + str(e))
"""
try:
	json.dump(total_list, f)
except Exception as e:
	print("JSON Error"+str(e))

print(len(total_list))

pickleFile = open('music_pickle.dat', 'wb')
pickle.dump(total_list, pickleFile)

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
