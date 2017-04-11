import os
from subprocess import Popen, call, PIPE
import random
import time
from pprint import pprint
import json
from typeclassifier import TypeClassifier

class MusicControl:
	def __init__(self, xmlDir):

		self.classifier = TypeClassifier("fastText/voiceai-music.bin", "fastText/fasttext")

		self.cvlc_loaded = False
		self.list = []
		data = []
		with open('music_metadata.json') as data_file:    
			data = json.load(data_file)


		for song in data:
			self.list.append([str(song["album"]), str(song["artist"]), str(song["name"]), str(song["location"])])
		#self.list.sort(key=lambda tup:tup[1])

	def textFilter(self, tagged):
		keep_words = ['xVB', 'xRP', 'xNN']
		change_tags = ['xNNP']
		# change tags -> keep tags -> return array of tuple

		filtered_tags = []
		for tup in tagged:
			for k_w in keep_words:
				if tup[1] == k_w:
					filtered_tags.append(tup)
					break

			for c_t in change_tags:
				if tup[1] == c_t:
					filtered_tags.append((tup[1], tup[1]))
					break

		return filtered_tags

	def functionFilter(self, tagged, pure_entities):
		keep_words = ['xVB', 'xRP', 'xNN']
		change_tags = ['xNNP']

		modifier = ""
		no_more_modifier = False
		# change tags -> keep tags -> return array of tuple

		filtered_tags = []
		for tup in tagged:
			for k_w in keep_words:
				if tup[1] == k_w:
					filtered_tags.append(tup)
					break

			if tup[1] == 'xJJ' and no_more_modifier == False:
				modifier = tup[0]
				no_more_modifier = True

			for c_t in change_tags:
				if tup[1] == c_t:
					filtered_tags.append((tup[1], tup[1]))
					break

		text = [tup[0] for tup in filtered_tags]
		f_type, prob = self.classifier.classifyText(" ".join(text))

		msg = " ".join(text)

		if f_type > -1:
			print("Prob : "+str(prob))
		else:
			return "I'm sorry I didn't get that, Vidur"

		good_words = ['good', 'nice', 'best', 'amazing', 'great', 'hot', 'hottest']
		bad_words = ['bad', 'boring', 'worst', 'shitty']
		next_words = ['next', 'upcoming']
		last_words = ['previous', 'last']

		if f_type == 1:
			if modifier in last_words:
				f_type = 5
			else:
				if modifier in next_words:
					f_type = 4
				else:
					if modifier in good_words:
						#Do something to modify play
						pass
					else:
						if modifier in bad_words:
							#Do something to modify play
							pass 

		album_entity = None
		artist_entity = None
		song_entity = None

		for entity in pure_entities:
			text = [tup[0] for tup in entity]
			if entity[0][1] == 'TRK':
				song_entity = ' '.join(text)
				continue
			if entity[0][1] == 'ALB':
				album_entity = ' '.join(text)
				continue
			if entity[0][1] == 'PER':
				artist_entity = ' '.join(text)
				continue

		if f_type == 2:
			return "\n".join([msg, self.Stop()])
		if f_type == 3:
			return "\n".join([msg, self.Pause()])
		if f_type == 1:
			return "\n".join([msg, "Playing song :", self.Play(song_entity, artist_entity, album_entity)])#self.mp.Play(song_name, artist_name, album_name)])
		if f_type == 4:
			return "\n".join([msg, self.Next()])
		if f_type == 5:
			return "\n".join([msg, self.Prev()])

		return "I'm sorry, I didn't get that"

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

			return "No Song Found"

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

			return "No Song Found"
				
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
				
			return "Artist not found"

		if song_name == None and artist_name == None and album_name != None:
			#SEARCH ALBUMS
			#albumFound = False
			#startIndex = 0
			#endIndex = 0
			album_name = album_name.lower()
			albumList = []
			#self.list.sort(key=lambda tup:tup[0])
			for i, song in enumerate(self.list):
				index = (song[0].lower()).find(album_name)
				if index > -1:
					albumList.append(self.list[i])

			if len(albumList) > 0:
				random.shuffle(albumList)
				return self.PlayList(albumList)
			
			return "No Album Found"

		if song_name == None and artist_name != None and album_name != None:
			artist_name = artist_name.lower()
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

			return "No Album Found"

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
		return "Paused the song"

	def Stop(self):
		os.system(" ".join(['./mprisvlc.sh', 'vlc', 'stop']))
		return "Stopped the song"

	def Next(self):
		os.system(" ".join(['./mprisvlc.sh', 'vlc', 'next']))
		return "Skipping this song. Playing next one"		
	
	def Prev(self):
		os.system(" ".join(['./mprisvlc.sh', 'vlc', 'prev']))
		return "Playing the previous song"
	
