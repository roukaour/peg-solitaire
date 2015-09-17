##############################################
#
# In this file we have imported our game state,
# from specified command line txt file.
#
##############################################

def readGameState(filePath):
	#Reading file
	fileHandle = open(filePath, 'r')
	rawState = fileHandle.readline().strip().split(',')
	#updating game state with all 0
	pegHolder = [[0 for x in range(7)] for x in range(7)]
	
	#check for dimension of given board
	if len(rawState) != 7:
		print "Wrong gameState given, check txt file"
		exit(0)
	else:
		for i in range(7):
			if len(rawState[i]) != 7:
				print "Wrong gameState given, check txt file"
				exit(0)
	
	#update peg and corner positions
	for i in range(7):
		for j in range(7):
			if rawState[i][j] == '-':
				pegHolder[i][j] = -1
			elif rawState[i][j] == 'X':
				pegHolder[i][j] = 1
			elif rawState[i][j] == '0':
				pegHolder[i][j] == 0
			else:
				print "Invalid Charachter in game state, check txt file"
				exit(0)
	
	return pegHolder
