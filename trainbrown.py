cats = open('../nltk_data/corpora/brown/cats.txt', 'r')
fw = open("stanford-pos/brown_to_penn.tsv", "w")
for line in cats:
	lwords = line.split()
	filename = "".join(['../nltk_data/corpora/brown/', lwords[0]])
	f = open(filename, 'r')
	#fw = open("".join(['brownNER/', lwords[0]]), 'w')
	for l in f:
		l = l.strip()
		if l=='':
			continue

		words = l.split()
		for word in words:
			corp = word.split('/')
			wrd = corp[0]
			tags = corp[1]

			tag = tags[:2]
			wrdtag = ""

			if len(tags) > 4 and tags[-2]=="t" and tags[-1]=="l":
				wrdtag == "NNP"
			else:
				if tag=="np":
					wrdtag = "NNP"
				else:
					if tags=="pp$$" or tags=="ppl" or tags=="ppls" or tags=="ppo" or tags=="pps" or tags=="ppss" or tags=="prp":
						wrdtag = "PRP"
					else:
						if tag=="jj" or tag=="ap" or tag == "od" or tags=="qlp":
							wrdtag = "JJ"
						else:
							if tag=="at" or tag=="dt" or tags=="abn" or tags=="abx":
								wrdtag = 'DT'
							else:
								if tag=="be" or tag=="hv" or tag=="vb" or tag=="do":
									wrdtag = "VB"
								else:
									if tag=="cc":
										wrdtag = 'CC'
									else:
										if tags=="abl" or tags=="ql" or tag=="rb":
											wrdtag = "RB"
										else:
											if tag=="in" or tag=="cs":
												wrdtag = "IN"
											else:
												if tag=="nn" or tag=="nr" or tag=="rn" or tag=="pn":
													wrdtag = "NN"
												else:
													if tag=="uh":
														wrdtag = 'UH'
													else:
														if tag=="fw":
															wrdtag = "NNP"
														else:
															if tags=="wql" or tags=="wrb":
																wrdtag = 'WRB'
															else:
																if tag == "cd":
																	wrdtag = 'CD'
																else:
																	if tag=="md":
																		wrdtag = 'MD'
																	else:
																		if tag=="rp":
																			wrdtag = "RP"
																		else:
																			if tag=="to":
																				wrdtag = "TO"
																			else:
																				if tags=="pp$" or tags=="prp$":
																					wrdtag = "PRP$"
																				else:
																					if tag=="wd":
																						wrdtag = "WDT"
																					else:
																						if tags=="wp$":
																							wrdtag = "WP$"
																						else:
																							if tag=="wp":
																								wrdtag = "WP"
																							else:
																								if tag=="ex":
																									wrdtag = "EX"
																								else:
																									wrdtag = "."
			if wrdtag == "":
				wrdtag = "NNP"
			if wrd == "":
				continue
			wrdtag = "x" + wrdtag 
			if tags=="nn$" or tags=="nns$" or tags=="np$" or tags=="nps$" or tags=="pn$":
				wrd_pos = wrd.split("'")
				fw.write(wrd_pos[0])
				fw.write('_')
				fw.write(wrdtag)
				fw.write(' ')
				fw.write("'s")
				fw.write('_')
				fw.write('xPOS')
				fw.write(' ')
			else:	
				fw.write(wrd)
				fw.write('_')
				fw.write(wrdtag)
				fw.write(' ')
		fw.write('\n')
cats.close()
'''
cats = open('/home/vidur/Downloads/masc_tagged/categories.txt', 'r')
for line in cats:
	lwords = line.split()
	filename = "".join(['/home/vidur/Downloads/masc_tagged/', lwords[0]])
	f = open(filename, 'r')
	#fw = open("".join(['brownNER/', lwords[0]]), 'w')
	for l in f:
		l = l.strip()
		if l=='':
			continue

		words = l.split()
		lastWord = ""
		for word in words:
			corp = word.split('_')
			wrd = "-".join(corp[:-1])
			if lastWord != "":
				wrd = lastWord + wrd
				lastWord = ""
			if len(corp) == 1:
				lastWord = wrd
				continue
			wrdtag = corp[-1]

			if wrdtag == "PDT":
				wrdtag = "DT"
			else:
				if wrdtag == "JJR" or wrdtag == "JJS":
					wrdtag = "JJ"
				else:
					if wrdtag == "NNS":
						wrdtag = "NN"
					else:
						if wrdtag == "NNPS":
							wrdtag = "NNP"
						else:
							if wrdtag == "RBR" or wrdtag == "RBS":
								wrdtag = "RB"
							else:
								if wrdtag[:2] == "VB":
									wrdtag = "VB"
								else:
									if wrdtag == "LS":
										continue
									else:
										if wrdtag == "SYM":
											wrdtag = "DT"
										else:
											if wrdtag == "." or wrdtag == ',' or wrdtag == "?" or wrdtag == ";" or wrdtag == "*" or wrdtag == "(" or wrdtag == ")" or wrdtag == "--" or wrdtag == ":":
												wrdtag = "."
			fw.write(wrd)
			fw.write('_')
			fw.write(wrdtag)
			fw.write(' ')
		fw.write('\n')
cats.close()'''
#fw.close()
