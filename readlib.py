from pyItunes import *

l = Library('iml.xml')

f = open('stanford-ner/musicxml.tsv', 'w')
list = []
for id, song in l.songs.items():
	if song:
		list.append([str(song.album), str(song.artist), str(song.name)])

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

f.close()
