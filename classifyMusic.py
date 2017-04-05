from sklearn import cluster
import json
import pickle

list = []
data = []
nameList = []

with open('music_metadata.json') as data_file:    
	data = json.load(data_file)

for song in data:
	nameList.append(str(song["name"]))
	list.append((float(song["energy"]), float(song["tempo"]), float(song["centroid"]), float(song["vocals"])))#,  float(song["chroma"])))

"""
k_means = cluster.KMeans(n_clusters=11)
k_means.fit(list)

songTuple = [(nameList[i], k_means.labels_[i]) for i in range(len(nameList))]
"""

mean_shift = cluster.Birch(n_clusters=7)
mean_shift.fit(list)

songTuple = [(nameList[i], mean_shift.labels_[i]) for i in range(len(nameList))]

songTuple.sort(key=lambda tup:tup[1])

for i in range(len(nameList)):
	print(songTuple[i][0] + " : " + str(songTuple[i][1]))

pickleFile = open('music_cluster.dat', 'wb')
pickle.dump(mean_shift, pickleFile)

"""
print(nameList)
print(k_means.labels_)
"""