import readGame


# I separated the given game class into two classes, game and gameNode.
# The game class is mutable, and only one exists for each search. It stores
# overall data like the parsed game state, count of nodes expanded, and
# move trace. Its rootNode method returns a gameNode to search from.
# The gameNode class is immutable, and returns new instances from its
# getNextState method (which increments the nodesExpanded count of the
# associated game object). It implements all the required methods as well as
# its own helper methods. Note that while gameNode uses a 1D list to store
# its game state, the game class's gameState is unmodified.
class game(object):
	"""
	Stores the global state for a single game of Peg Solitaire.
	When a search function is applied to a game, the game state is replaced by
	a solved state; the count of nodes expanded is incremented for every time
	the search function expanded a node in the game tree; and the trace is
	set to a list of old and new positions for pegs that will solve the game.
	"""

	def __init__(self, filePath):
		"""Initialize a game from a text file."""
		self.gameState = readGame.readGameState(filePath)
		self.nodesExpanded = 0
		self.trace = []

	def __str__(self):
		"""Return a printable string representation of the game."""
		return ','.join(''.join('0X-'[t] for t in row) for row in self.gameState)

	def rootNode(self, heuristic=id):
		"""Return a root node of the game tree for this game."""
		# gameNode uses a flat list, not a 2D list of lists, for efficiency
		rootState = sum(self.gameState, [])
		return gameNode(rootState, self.trace, rootState.count(1), heuristic)


class gameNode(object):
	"""
	Stores a single node in the game tree of a game of Peg Solitaire.
	When a search function is applied to a game, it creates as many gameNodes
	as necessary to find a solved game state. Every time a new gameNode is
	created, it increments the game's nodesExpanded counter.
	"""

	# I do not use this method. Instead of writing something like:
	#     self.state[pos] if self.is_corner(pos) else -1
	# I implemented __getitem__ with a bounds check so I can write:
	#     self[pos]
	# and automatically avoid IndexErrors.
	def is_corner(self, pos):
		"""
		Return whether a position is a corner/wall, i.e. not a hole or peg.
		"""
		return 0 <= pos < 49 and self.state[pos] != -1

	@staticmethod
	def getNextPosition(oldPos, direction):
		"""
		Return the new position after moving in the given direction
		(7 is north/up, 1 is east/right, -7 is south/down, and -1 is west/left).
		Invalid movements outside the bounds of the board will return positions
		such that is_corner(position) returns True.
		"""
		newPos = oldPos + direction
		# If direction is 7 or -7 (changing rows), newPos is already correct
		return (newPos if direction == 7 or direction == -7 or
		# If direction is 1 or -1 (changing columns), the row should not change
			newPos // 7 == oldPos // 7 else -1)

	def __init__(self, state, trace, pegCount, heuristic=id):
		"""Initialize the game node."""
		self.state = state
		self.trace = trace
		# The peg count is cached so that validMoves can return early if only
		# one peg is left
		self.pegCount = pegCount
		# The heuristic being used, if any, is stored so that __cmp__ can use it
		self.heuristic = heuristic
		# The representative one of eight symmetric states is cached because
		# recalculating it is relatively expensive
		self.key = self.symmetricState()

	def __str__(self):
		"""Return a printable string representation of the game state."""
		return ','.join(''.join('0X-'[t] for t in self.state[i*7:i*7+7]) for i in xrange(7))

	def __getitem__(self, pos):
		"""node[pos] is bounds-checked shorthand for node.state[pos]."""
		return self.state[pos] if 0 <= pos < 49 else -1

	def __cmp__(self, other):
		"""
		Return the comparison of this node with another one (1, 0, or -1).
		Nodes have to be comparable by their estimated cost for informed
		searches to prioritize the lower-cost nodes. Cost may incorporate a
		heuristic function as well as a distance estimate.
		The default heuristic is the id function, so that comparisons without
		a heuristic act like default Python comparisons.
		"""
		# Store heuristic locally to avoid repeated LOAD_ATTR instructions
		heuristic = self.heuristic
		return heuristic(self) - heuristic(other)

	def is_solved(self):
		"""Return whether the game node is in a solved state (one central peg)."""
		# 24, or (3, 3), is the central position, and 1 is (coincidentally) the
		# number representing a peg and the required peg count
		return self.state[24] == self.pegCount # == 1

	def is_validMove(self, oldPos, direction):
		"""
		Return whether it is valid to move a peg from a given position in a
		given direction. The position must have a peg, the destination must be
		empty, and the intermediate position must have another peg.
		"""
		# Since self.getNextPosition and self.__getitem__ are bounds-checked.
		# the self.is_corner check is redundant, so I commented it out
		#########################################
		# DONT change Things in here
		# In this we have got the next peg position and
		# below lines check for if the new move is a corner
		#newPos = self.getNextPosition(oldPos, direction)
		#if self.is_corner(newPos):
		#	return False
		########################################
		# YOU HAVE TO MAKE CHANGES BELOW THIS
		# check for cases like:
		# if new move is already occupied
		# or new move is outside peg Board
		# Remove next line according to your convenience
		midPos = self.getNextPosition(oldPos, direction)
		newPos = self.getNextPosition(midPos, direction)
		# 1 is a peg, and 0 is a hole
		# Since oldPos is valid, don't use bounds-checked indexing for it
		return (self.state[oldPos] == self[midPos] == 1 and self[newPos] == 0)

	# Store xrange locally to use LOAD_FAST instead of LOAD_GLOBAL instructions
	def validMoves(self, xrange=xrange):
		"""Generate all the valid moves from the current game state."""
		if self.pegCount <= 1:
			raise StopIteration
		for oldPos in xrange(49):
			# Valid moves start with a peg (1)
			# Since oldPos is valid, don't use bounds-checked indexing for it
			if self.state[oldPos] != 1: continue
			# 7 is north/up and 1 is east/right
			directions = [7, 1]
			# -7 is south/down (only necessary if not vertically symmetric)
			if not self.vsym: directions.append(-7)
			# -1 is west/left (only necessary if not horizontally symmetric)
			if not self.hsym: directions.append(-1)
			for direction in directions:
				midPos = self.getNextPosition(oldPos, direction)
				# Valid moves jump over a peg (1)
				if self[midPos] != 1: continue
				newPos = self.getNextPosition(midPos, direction)
				# Valid moves jump to a hole (0)
				if self[newPos] != 0: continue
				yield (oldPos, direction)

	def getNextState(self, oldPos, dir, pegSol):
		"""
		Return a child node of the current one, created by a given valid move.
		The given game has its count of expanded nodes incremented.
		"""
		###############################################
		# DONT Change Things in here
		pegSol.nodesExpanded += 1
		if not self.is_validMove(oldPos, dir):
			print "Error, You are not checking for valid move"
			exit(0)
		###############################################
		# YOU HAVE TO MAKE CHANGES BELOW THIS
		# Update the gameState after moving peg
		# eg: remove crossed over pegs by replacing it's
		# position in gameState by 0
		# and updating new peg position as 1
		midPos = self.getNextPosition(oldPos, dir)
		newPos = self.getNextPosition(midPos, dir)
		# x[:] makes a copy of x (necessary to avoid mutating self.state
		# when updating childState)
		childState = self.state[:]
		childState[oldPos] = 0 # The peg moves from here, leaving a hole
		childState[midPos] = 0 # The jumped-over peg is removed
		childState[newPos] = 1 # The peg moves to this hole
		# Convert positions back into pairs for printing
		childTrace = self.trace + [(oldPos // 7, oldPos % 7), (newPos // 7, newPos % 7)]
		return gameNode(childState, childTrace, self.pegCount - 1, self.heuristic)

	def copySolution(self, pegSol):
		"""
		Copy a found solution to the given game by copying the solved game
		state and found move trace to it.
		"""
		# Convert the game state back into a 2D list
		pegSol.gameState = [self.state[i*7:i*7+7] for i in xrange(7)]
		pegSol.trace = self.trace

	# Store tuple, zip, and xrange locally to use LOAD_FAST instead of LOAD_GLOBAL instructions
	def symmetricState(self, tuple=tuple, zip=zip, xrange=xrange):
		"""
		Return a representative game state equivalent to this game state under
		rotation and reflection. For any game state, there are seven other
		symmetric ones; the minimum one of these, encoded with immutable tuples
		instead of mutable lists so they can be hashed and stored in a set,
		represents all eight.
		"""
		# Convert the game state into a 2D list of tuples
		r0 = [tuple(self.state[i*7:i*7+7]) for i in xrange(7)]
		# x[::-1] reverses x, or reflects a 2D list across the horizontal axis
		# zip(*x[::-1]) rotates a 2D list 90 degrees clockwise
		f0 = r0[::-1]
		# Cache vertical symmetry to prune validMoves
		self.vsym = r0 == f0
		r90 = zip(*f0)
		f90 = r90[::-1]
		r180 = zip(*f90)
		f180 = r180[::-1]
		# Cache horizontal symmetry to prune validMoves
		self.hsym = r0 == f180
		r270 = zip(*f180)
		f270 = r270[::-1]
		return tuple(min(r0, f0, r90, f90, r180, f180, r270, f270))

		# I also tried compressing states by treating holes and pegs as 0s and
		# 1s in a 33-bit integer, but this approach was slower without usefully
		# lowering memory usage. Even when an A* search expands 2 million nodes
		# to solve a 32-peg game, the Python process using tuples takes up
		# 100 MB RAM versus 20 MB when using integers, but runs 50% faster.
		# Saving 80% of the memory is significant, but neither quantity is
		# large compared to the gigabytes available on modern computers.
		# To test this approach anyway, replace the "return" line with this:
		# def binaryHash(state):
		# 	hash = 0
		# 	for row in state:
		# 		for t in row:
		# 			if t != -1:
		# 				hash = (hash << 1) | pos
		# 	return hash
		# return binaryHash(min(r0, f0, r90, f90, r180, f180, r270, f270))
