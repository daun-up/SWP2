import pickle
with open("assignment3.dat",'rb') as f:
	data = pickle.load(f)

dbfilename = 'assignment3.dat'

def readScoreDB():
	try:
		fH = open(dbfilename, 'rb')
	except FileNotFoundError as e:
		print("New DB: ", dbfilename)
		return []

	scdb = []
	try:
		scdb =  pickle.load(fH)
	except:
		print("Empty DB: ", dbfilename)
	else:
		print("Open DB: ", dbfilename)
	fH.close()
	return scdb


# write the data into person db
def writeScoreDB(scdb):
    fH = open(dbfilename, 'wb')
    pickle.dump(scdb, fH)
    fH.close()

def doScoreDB(scdb):
	while(True):
		inputstr = (input("Score DB > "))
		if inputstr == " ": continue
		parse = inputstr.split(" ")

		if parse[0] == 'add':
			record = {'Name':parse[1], 'Age':parse[2], 'Score':parse[3]}
			scdb += [record]
			
		elif parse[0] == 'del':
			try:
				for p in scdb[:]:
					if p['Name'] == parse[1]:
						scdb.remove(p)
						if p['Name'] != parse[1] :
							break
			except IndexError as e:
				print("Input Name")

		elif parse[0] == 'show':
			sortKey ='Name' if len(parse) == 1 else parse[1]
			showScoreDB(scdb, sortKey)

		elif parse [0] == 'find':
			try:
				for p in scdb:
					if p['Name'] == parse[1]:
						print(p)
			except IndexError as e:
				print("Input Name")

		elif parse[0] == 'inc':
			try:
				for p in scdb:
					if p['Name'] == parse[1]:
						p['Score'] = str(int(p['Score']) + int(parse[2]))
			except IndexError as e:
				print("Input Name,score")

		elif parse[0] == 'quit':
			break
		else:
			print("Invalid command: " + parse[0])
			

def showScoreDB(scdb, keyname): 
	for p in sorted(scdb, key=lambda person: person[keyname]): #sorted <-정렬된 결과를 반환. 변형 없음
		for attr in sorted(p):
			print(str(attr) + "=" + str(p[attr]), end=' ')
		print()
	


scoredb = readScoreDB()
doScoreDB(scoredb)
writeScoreDB(scoredb)

#parmeter 매개변수
# def 함수 이름 (매개 변수1,매개 변수2)
#	 실행 구문
#	 return 반환값
