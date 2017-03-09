from pyItunes import *
import os
from subprocess import Popen, call, PIPE
import random
import pathlib
import time
from pprint import pprint

class MusicControl:
	def __init__(self, xmlDir, musicDir):
		self.l = Library(xmlDir)
		self.cvlc_loaded = False
		self.list = []
		self.defLoc = musicDir#'/run/media/vidur/Kachra/Music/'
		for id, song in self.l.songs.items():
			if song:
				self.list.append([str(song.album), str(song.artist), str(song.name), "".join([self.defLoc, str(song.location[9:])])])
		#self.list.sort(key=lambda tup:tup[1])

	def processText(self, textArray):
		return "Processed"

	def PlayList(self, SongList=None):
		firstSongLoc = SongList[0][3]
		os.system("./mprisvlc.sh vlc quit")
		cvlc_p = Popen(['cvlc', '--started-from-file', '--playlist-enqueue', firstSongLoc])
		self.cvlc_loaded = True
		time.sleep(3)
		for i in range(1, min(50, len(SongList))):
			eachSong = SongList[i]
			os.system("".join(['cvlc ', '--started-from-file ', '--playlist-enqueue "', eachSong[3], '"']))
		return firstSongLoc

	def SearchSong(self, song_name=None, artist_name=None, album_name=None):
		
		if song_name != None and artist_name == None and album_name == None:
			#SEARCH SONGS
			song_name = song_name.lower()
			for song in self.list:
				index = (song[2].lower()).find(song_name)
				if index > -1:
					random.shuffle(self.list)
					self.list[0], song = song, self.list[0]
					return self.PlayList(self.list)

			#SEARCH ALBUMS
			#albumFound = False
			#startIndex = 0
			#endIndex = 0
			albumList = []
			#self.list.sort(key=lambda tup:tup[0])
			for i, song in enumerate(self.list):
				index = (song[0].lower()).find(song_name)
				if index > -1:
					albumList.append(self.list[i])

			if len(albumList) > 0:
				random.shuffle(albumList)
				return self.PlayList(albumList)
				
			return "No Song/Album Found"

		if song_name != None and artist_name != None and album_name == None:
			song_name = song_name.lower()
			#EITHER SONG+ARTIST or ALBUM+ARTIST
			artist_name = artist_name.lower()
			for song in self.list:
				index1 = (song[2].lower()).find(song_name)
				index2 = (song[1].lower()).find(artist_name)
				if index1 > -1 and index2 > -1:
					random.shuffle(self.list)
					self.list[0], song = song, self.list[0]
					return self.PlayList(self.list)

			#albumFound = False
			#startIndex = 0
			#endIndex = 0
			albumList = []
			#self.list.sort(key=lambda tup:tup[0])
			for i, song in enumerate(self.list):
				index1 = (song[0].lower()).find(song_name)
				index2 = (song[1].lower()).find(artist_name)
				if index1 > -1 and index2 > -1:
					albumList.append(self.list[i])
			if len(albumList) > 0:
				random.shuffle(albumList)
				return self.PlayList(albumList)
				
			return "No Song/Album Found"
				
		if song_name != None and artist_name == None and album_name != None:
			return "Feature Not Available"

		if song_name != None and artist_name != None and album_name != None:
			return "Feature Not Available"
			
		if song_name == None and artist_name == None and album_name == None:
			random.shuffle(self.list)
			return self.PlayList(self.list)

		if song_name == None and artist_name != None and album_name == None:
			artist_name = artist_name.lower()
			#artistFound = False
			#startIndex = 0
			#endIndex = 0
			artistList = []
			#self.list.sort(key=lambda tup:tup[1])
			for i, song in enumerate(self.list):
				index = (song[1].lower()).find(artist_name)
				if index > -1:
					artistList.append(self.list[i])					
			if len(artistList) > 0:
				random.shuffle(artistList)
				return self.PlayList(artistList)
				
			return "No Song/Album Found"

		if song_name == None and artist_name == None and album_name != None:
			return "Feature Not Available"

		if song_name == None and artist_name != None and album_name != None:
			return "Feature Not Available"

		return "Something"		

	def Play(self, song_name=None, artist_name=None, album_name=None):
		process = Popen(['./mprisvlc.sh', 'vlc', 'status'], stdout=PIPE, stderr=PIPE)
		out, err = process.communicate()
		out = str(out, 'utf-8')
		#return "bleh"
		if song_name==None and artist_name==None and album_name==None and out!='':
			os.system(" ".join(['./mprisvlc.sh', 'vlc', 'play']))
			return self.SearchSong(song_name, artist_name, album_name)#"Resuming music"
		else:
			return self.SearchSong(song_name, artist_name, album_name)

	def Pause(self):
		os.system(" ".join(['./mprisvlc.sh', 'vlc', 'pause']))

	def Stop(self):
		os.system(" ".join(['./mprisvlc.sh', 'vlc', 'stop']))

	def Next(self):
		os.system(" ".join(['./mprisvlc.sh', 'vlc', 'next']))		
	
	def Prev(self):
		os.system(" ".join(['./mprisvlc.sh', 'vlc', 'prev']))
	
