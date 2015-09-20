import pegSolitaireUtils
import config
import heapq


# Returned by a search function that was cut off before exhausting itself
CUTOFF = object()
# Returned by a search function that exhausted itself without solving a game
FAILURE = object()


def recordFailure(pegSol):
	"""
	Mark a Peg Solitaire game as failed (impossible to solve) by setting the
	trace to an error message instead of a list of moves.
	"""
	pegSol.trace = "Impossible to solve"


def ItrDeepSearch(pegSol):
	"""
	Perform an iterative-deepening depth-first search on the game tree of the
	given Peg Solitaire game, and return whether or not the game could be solved.
	Based on textbook figure 3.18 (section 3.4, page 89), but with an additional
	set of failed nodes (modulo symmetry) to avoid revisiting, which is reused
	over succesive depth-limited searches and roughly halves the count of
	expanded nodes. (A cut-off result may succeed at a greater depth, but a
	failed result will not and can safely be pruned.)
	"""
	#################################################
	# Must use functions:
	# getNextState(self,oldPos, direction)
	#
	# we are using this function to count,
	# number of nodes expanded, If you'll not
	# use this grading will automatically turned to 0
	#################################################
	#
	# using other utility functions from pegSolitaireUtility.py
	# is not necessary but they can reduce your work if you
	# use them.
	# In this function you'll start from initial gameState
	# and will keep searching and expanding tree until you
	# reach goal using Iterative Deepning Search.
	# you must save the trace of the execution in pegSolitaireObject.trace
	# SEE example in the PDF to see what to save
	#
	#################################################
	failed = set()
	# Without a maximum depth, impossible games would infintely loop
	maxDepth = sum(row.count(1) for row in pegSol.gameState)
	for depth in xrange(maxDepth):
		# DepthLimitedSearch eventually calls getNextState and saves the move trace
		result = DepthLimitedSearch(pegSol, depth, failed)
		if result is not CUTOFF and result is not FAILURE:
			return True
	recordFailure(pegSol)
	return False

	# Since the depth of a Peg Solitaire solution is known to be one less than
	# the number of initial pegs, iterative deepening does not actually perform
	# better than depth-limited search.
	# To test this, replace the function body with this:
	# limit = sum(row.count(1) for row in pegSol.gameState) - 1
	# return DepthLimitedSearch(pegSol, limit, set())


def DepthLimitedSearch(pegSol, limit, failed):
	"""
	Perform a depth-limited search on the game tree of the given Peg Solitaire
	game, and return either the updated game, CUTOFF (if the game cannot be
	solved within the depth limit), or FAILURE (if the game cannot be solved
	at all, given the available actions).
	Based on textbook figure 3.17 (section 3.4, page 88), but with an additional
	set of failed nodes (modulo symmetry) to avoid revisiting, which is reused
	for future depth-limited searches.
	"""
	root = pegSol.rootNode()
	# RecursiveDLS eventually calls getNextState and saves the move trace
	return RecursiveDLS(root, pegSol, limit, set(failed), failed)


def RecursiveDLS(node, pegSol, limit, explored, failed):
	"""
	Perform a recursive depth-limited search on the game tree of the given Peg
	Solitaire game, and return either the updated game, CUTOFF (if the game
	cannot be solved within the depth limit), or FAILURE (if the game cannot be
	solved at all, given the available actions).
	Based on textbook figure 3.17 (section 3.4, page 88), but with an additional
	set of explored nodes (modulo symmetry) to avoid revisiting, and a set of
	failed nodes to avoid revisiting even at a greater depth.
	"""
	if node.is_solved():
		# copySolution saves the move trace
		node.copySolution(pegSol)
		return node
	elif limit == 0:
		return CUTOFF
	explored.add(node.key)
	cut_off = False
	for (oldPos, dir) in node.validMoves():
		# getNextState updates the game's nodesExpanded count
		childNode = node.getNextState(oldPos, dir, pegSol)
		if childNode.key in explored:
			continue
		result = RecursiveDLS(childNode, pegSol, limit - 1, explored, failed)
		if result is CUTOFF:
			cut_off = True
		elif result is FAILURE:
			failed.add(childNode.key)
		else:
			return result
	if cut_off:
		return CUTOFF
	failed.add(node.key)
	return FAILURE


def aStarOne(pegSol):
	"""
	Perform an A* search using heuristic #1 on the game tree of the given Peg
	Solitaire game, and return either the updated game or FAILURE.
	"""
	#################################################
	# Must use functions:
	# getNextState(self,oldPos, direction)
	#
	# we are using this function to count,
	# number of nodes expanded, If you'll not
	# use this grading will automatically turned to 0
	#################################################
	#
	# using other utility functions from pegSolitaireUtility.py
	# is not necessary but they can reduce your work if you
	# use them.
	# In this function you'll start from initial gameState
	# and will keep searching and expanding tree until you
	# reach goal using A-Star searching with first Heuristic
	# you used.
	# you must save the trace of the execution in pegSolitaireObject.trace
	# SEE example in the PDF to see what to return
	#
	#################################################
	# UniformCostSearch eventually calls getNextState and saves the move trace
	if UniformCostSearch(pegSol, heuristicOne) is FAILURE:
		recordFailure(pegSol)
		return False
	return True


def aStarTwo(pegSol):
	"""
	Perform an A* search using heuristic #2 on the game tree of the given Peg
	Solitaire game, and return either the updated game or FAILURE.
	This is the only search function capable of solving the "central game"
	(all holes filled with pegs except the center hole) in a reasonable
	amount of time (expanding only 225 nodes).
	"""
	#################################################
	# Must use functions:
	# getNextState(self,oldPos, direction)
	#
	# we are using this function to count,
	# number of nodes expanded, If you'll not
	# use this grading will automatically turned to 0
	#################################################
	#
	# using other utility functions from pegSolitaireUtility.py
	# is not necessary but they can reduce your work if you
	# use them.
	# In this function you'll start from initial gameState
	# and will keep searching and expanding tree until you
	# reach goal using A-Star searching with second Heuristic
	# you used.
	# you must save the trace of the execution in pegSolitaireObject.trace
	# SEE example in the PDF to see what to return
	#
	#################################################
	# UniformCostSearch eventually calls getNextState and saves the move trace
	if UniformCostSearch(pegSol, heuristicTwo) is FAILURE:
		recordFailure(pegSol)
		return False
	return True


def aStarThree(pegSol):
	"""
	Perform an A* search using heuristic #3 on the game tree of the given Peg
	Solitaire game, and return either the updated game or FAILURE.
	"""
	#################################################
	# Must use functions:
	# getNextState(self,oldPos, direction)
	#
	# we are using this function to count,
	# number of nodes expanded, If you'll not
	# use this grading will automatically turned to 0
	#################################################
	#
	# using other utility functions from pegSolitaireUtility.py
	# is not necessary but they can reduce your work if you
	# use them.
	# In this function you'll start from initial gameState
	# and will keep searching and expanding tree until you
	# reach goal using A-Star searching with first Heuristic
	# you used.
	# you must save the trace of the execution in pegSolitaireObject.trace
	# SEE example in the PDF to see what to return
	#
	#################################################
	if UniformCostSearch(pegSol, heuristicThree) is FAILURE:
		recordFailure(pegSol)
		return False
	return True


def aStarFour(pegSol):
	"""
	Perform an A* search using heuristic #4 on the game tree of the given Peg
	Solitaire game, and return either the updated game or FAILURE.
	"""
	#################################################
	# Must use functions:
	# getNextState(self,oldPos, direction)
	#
	# we are using this function to count,
	# number of nodes expanded, If you'll not
	# use this grading will automatically turned to 0
	#################################################
	#
	# using other utility functions from pegSolitaireUtility.py
	# is not necessary but they can reduce your work if you
	# use them.
	# In this function you'll start from initial gameState
	# and will keep searching and expanding tree until you
	# reach goal using A-Star searching with first Heuristic
	# you used.
	# you must save the trace of the execution in pegSolitaireObject.trace
	# SEE example in the PDF to see what to return
	#
	#################################################
	if UniformCostSearch(pegSol, heuristicFour) is FAILURE:
		recordFailure(pegSol)
		return False
	return True


def UniformCostSearch(pegSol, heuristic=None):
	"""
	Perform a uniform-cost search (with an optional cost heuristic) of the game
	tree of the given Peg Solitaire game, and return either the updated game
	or FAILURE.
	Based on textbook figure 3.14 (section 3.4, page 84), but with the set of
	explored nodes taken modulo symmetry. (One board state can be solved iff
	its seven symmetrical states can be solved, so when one has been expanded
	the other seven can be pruned.)
	"""
	root = pegSol.rootNode(heuristic)
	frontier = [root]
	frontierLookup = {root.key}
	explored = set()
	while True:
		if not frontier:
			return FAILURE
		node = heapq.heappop(frontier)
		frontierLookup.remove(node.key)
		if node.is_solved():
			# copySolution saves the move trace
			node.copySolution(pegSol)
			return node
		explored.add(node.key)
		for (oldPos, dir) in node.validMoves():
			# getNextState updates the game's nodesExpanded count
			childNode = node.getNextState(oldPos, dir, pegSol)
			# This only checks if childNode is in explored or frontier, and if
			# not, adds it to frontier. True A* would also check if a node in
			# frontier has the same state but a higher path cost, and would
			# replace that node with childNode. However, in Peg Solitaire,
			# the path cost from states P to Q will be the number of moves from
			# P to Q, i.e. the number of pegs removed. So if nodes Q and Q' have
			# the same state, they must have the same path cost from any node P,
			# and there is no need to replace one with the other.
			if childNode.key not in explored and childNode.key not in frontierLookup:
				heapq.heappush(frontier, childNode)
				frontierLookup.add(childNode.key)


# Store sum and xrange locally to use LOAD_FAST instead of LOAD_GLOBAL instructions
def heuristicOne(node, sum=sum, xrange=xrange):
	"""
	Return a heuristic estimate of the cost of solving the given game node.
	This heuristic sums the Manhattan distances of each peg from the four holes
	surrounding the center hole. I chose this heuristic because the end goal
	is to have a single peg in the center, but in the middle stage of the game,
	it is preferable to have pegs just outside the center so that they can be
	used to remove other pegs.
	"""
	# A lookup table of Manhattan distances is faster than calculating them
	distances = [
		5, 4, 3, 2, 3, 4, 5,
		4, 3, 2, 1, 2, 3, 4,
		3, 2, 1, 0, 1, 2, 3,
		2, 1, 0, 1, 0, 1, 2,
		3, 2, 1, 0, 1, 2, 3,
		4, 3, 2, 1, 2, 3, 4,
		5, 4, 3, 2, 3, 4, 5
	]
	# Store node.state locally to avoid repeated LOAD_ATTR instructions
	state = node.state
	return sum(distances[k] for k in xrange(49) if state[k] == 1)

def heuristicTwo(node):
	"""
	Return a heuristic estimate of the cost of solving the given game node.
	This heuristic sums the estimated difficulty of removing each peg, where
	the difficulty is set at 4 for the outer corners of the plus-shaped board,
	3 for the inner corners, 1 for the center, and 0 for the other holes,
	and adds it to twice the number of pegs remaining on the board.
	I chose those values after some trial and error. Clearly the outer corners
	are the most difficult, since they are the least maneuverable. The inner
	corners are only slightly easier, since they have more neighbors but are
	still not in the ideal rows or columns. (Note that pegs in the outer and
	inner corners can only move within those positions, never to a non-corner
	hole.) The center peg is the end goal of the game, but prior to that having
	a peg sit there is not quite useful (since if you are left with two pegs
	and one is in the center, the game is unsolvable). I expected the edges
	between the corners to also be difficult to move, but in practice setting
	them to 1 caused longer runtimes.
	"""
	# Store node.state locally to avoid repeated LOAD_ATTR instructions
	state = node.state
	# Since pegs are 1s and holes are 0s, counting the pegs is equivalent to
	# summing the states, and the difficulty per peg can be factored out
	return node.pegCount * 2 + (
		# The eight outer corners are worth 4 each
		4 * (state[2] + state[4] + state[14] + state[20] +
			state[28] + state[34] + state[44] + state[46]) +
		# The four inner corners are worth 3 each
		3 * (state[16] + state[18] + state[30] + state[32]) +
		# The central hole is worth 1
		state[24]
	)

	# A less-optimized version of heuristicTwo would use the same kind of lookup
	# table as heuristicOne, but since most of the position difficulty values
	# are 0, this would be pointlessly slow.
	# difficulties = [
	# 	0, 0, 4, 0, 4, 0, 0,
	# 	0, 0, 0, 0, 0, 0, 0,
	# 	4, 0, 3, 0, 3, 0, 4,
	# 	0, 0, 0, 1, 0, 0, 0,
	# 	4, 0, 3, 0, 3, 0, 4,
	# 	0, 0, 0, 0, 0, 0, 0,
	# 	0, 0, 4, 0, 4, 0, 0,
	# ]
	# state = node.state
	# return node.pegCount * 2 + sum(difficulties[k] for k in xrange(49) if state[k] == 1)

def heuristicThree(node):
	"""
	Return a heuristic estimate of the cost of solving the given game node.
	This heuristic counts the number of "dangling" pegs (those without any
	neighbors) and adds it to the twice number of pegs remaining on the board.
	"""
	# Store node.state locally to avoid repeated LOAD_ATTR instructions
	state = node.state
	# Count the number of dangling pegs
	num_dangling = 0
	for i in xrange(49):
		if state[i] != 1:
			continue
		for direction in [7, 1, -7, -1]:
			if node[i + direction] == 1:
				break
		else:
			num_dangling += 1
	return node.pegCount * 2 + num_dangling

def heuristicFour(node):
	"""
	Return a heuristic estimate of the cost of solving the given game node.
	This heuristic counts the number of pegs in the four outer areas of the
	board and adds it to the twice number of pegs remaining on the board.
	"""
	# Store node.state locally to avoid repeated LOAD_ATTR instructions
	state = node.state
	# Instead of counting the pegs in the four outer areas, count the pegs in
	# the central area and subtract that from the total number of pegs, since
	# there are fewer central pegs to count
	return (node.pegCount * 3 - state[16] - state[17] - state[18] -
		state[23] - state[24] - state[25] - state[30] - state[31] - state[32])

	# A less-optimized version of heuristicFour would use the same kind of lookup
	# table as heuristicOne, but since most of the position difficulty values
	# are 0, this would be pointlessly slow.
	# corners = [
	# 	0, 0, 1, 1, 1, 0, 0,
	# 	0, 0, 1, 1, 1, 0, 0,
	# 	1, 1, 0, 0, 0, 1, 1,
	# 	1, 1, 0, 0, 0, 1, 1,
	# 	1, 1, 0, 0, 0, 1, 1,
	# 	0, 0, 1, 1, 1, 0, 0,
	# 	0, 0, 1, 1, 1, 0, 0,
	# ]
	# state = node.state
	# return node.pegCount * 2 + sum(corners[k] for k in xrange(49) if state[k] == 1)
