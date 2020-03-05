from copy import copy
from copy import deepcopy
import time
import sys
import pdb
sys.setrecursionlimit(1500)

# Number of moves ahead for predictions
NUM_MOVES_PREDICT = 6

"""
Define Classes

"""
# Define a class for a piece
class Piece:
	def __init__(self,type='k',player='w',position=[-1,-1]):
		self.type = type;
		self.player = player;
		self.position = position;

# Define a class for a square
class Square:
	def __init__(self,position=[0,0],piece = None):
		self.position = position;
		self.piece = piece;
		if piece is not None:
			piece.position = self.position;

# Define a class for the board
class Board:
	def __init__(self, size=4):
		self.size = size
		self.squares = [[Square([i,j]) for j in range(size)] for i in range(size)]
		self.moves = 0
		self.onlyKingsNumMoves = 0

	# Print current piece placement on board
	def printBoard(self):
		for s_line in self.squares:
			for s in s_line:
				print('0' if s.piece is None else s.piece.type+s.piece.player, end =" ");
			print();
		print();

	# Get the position of a given piece in the board. Returns None if said piece is not currently on the board
	def getPiecePosition(self,p_type,p_player):
		for s_line in self.squares:
			for s in s_line:
				if s.piece is not None and s.piece.type == p_type and s.piece.player == p_player:
					s.piece.position = s.position
					return s.position;
		return None;

	# Returns piece at a given position
	def getPieceAtPosition(self,position):
		if position is None or self.squares[position[0]][position[1]] is None:
			return None
		if self.squares[position[0]][position[1]].piece is not None:
			self.squares[position[0]][position[1]].piece.position = self.squares[position[0]][position[1]].position
		return self.squares[position[0]][position[1]].piece;

	def getPiece(self,p_type,p_player):
		for s_line in self.squares:
			for s in s_line:
				if s.piece is not None and s.piece.type == p_type and s.piece.player == p_player:
					s.piece.position = s.position
					return s.piece;
		return None;

	# Get the payoff of the zero-sum game
	def getPayoffs(self):
		types = ['r','k','b'];
		weights = {
			'r': 5,
			'b': 3,
			'k': 10000
		}
		payoff = 0;
		for t in types:
			pw = 0 if self.getPiecePosition(t,'w') is None else weights[t];
			pb = 0 if self.getPiecePosition(t,'b') is None else weights[t];

			payoff += pw-pb;
		return payoff;

	# Init pieces with a default placement on board
	def initPieces(self):
		self.squares[0][0].piece = Piece('r','w',[0,0]);
		self.squares[0][1].piece = Piece('k','w',[0,1]);
		self.squares[0][2].piece = Piece('b','w',[0,2]);

		self.squares[3][1].piece = Piece('b','b',[3,1]);
		self.squares[3][2].piece = Piece('k','b',[3,2]);
		self.squares[3][3].piece = Piece('r','b',[3,3]);

	# Get possible actions for a given player in the board
	def getPossibleActions(self,player):
		types = ['r','k','b'];
		actions = [];
		la = 0;

		for t in types:
			piece = self.getPiece(t,player);

			if piece is not None:
				for i in range(self.size):
					for j in range(self.size):

						act = Action(piece,[i,j],self);
						if act.is_valid:
							actions.insert(la,act);
							la+=1;
		return actions;

	# Update the board after a given action
	def updateBoard(self,action):
		self.squares[action.init_position[0]][action.init_position[1]] = Square(action.init_position,None);
		self.squares[action.final_position[0]][action.final_position[1]] = Square(action.final_position, action.piece);
		if self.onlyKingsLeft():
			self.onlyKingsNumMoves +=1

	# Check if the game is over
	def is_over(self):
		if self.moves<NUM_MOVES_PREDICT and self.getPiecePosition('k','w') is not None and self.getPiecePosition('k','b') is not None and self.onlyKingsNumMoves<3:
			return None;
		return self.getPayoffs();

	def onlyKingsLeft(self):
		if self.getPiecePosition('r','w') is None and self.getPiecePosition('r','b') is None and self.getPiecePosition('b','w') is None and self.getPiecePosition('b','b'):
			return True;
		return False;

class Game:
	def __init__(self, board=None, white_play=True, moves=0):
		self.board = board;
		self.white_play = white_play;
		self.alpha = -float('Inf')
		self.beta = float('Inf')

		if self.board is None:
			self.board = Board();
			self.board.initPieces();
			self.white_play = True;

		self.result = None

	# White pieces is max, in this case AI
	def max(self,board,alpha= -float('Inf'),beta=float('Inf')):
		# We're initially setting it to -inf as worse than the worst case:
	    max_payoff = -float('Inf');

	    sugeste_piece = None
	    sugested_movement = None

	    result = board.is_over();

	    # If the game came to an end, the function needs to return
	    # the evaluation function of the end.
	    if result is not None:
	        return (result, None, None)

	    possible_actions = board.getPossibleActions('w')

	    for action in possible_actions:
	    	# For each possible action, W player makes a move and calls Min
	    	# That's one branch of the game tree.
	    	new_board = deepcopy(board)
	    	new_board.updateBoard(action);
	    	new_board.moves += 1
	    	
	    	(m,sp,sm) = self.min(new_board,alpha,beta)

	    	# Fixing the max value if needed
	    	if m > max_payoff:
	    		max_payoff = m
	    		sugeste_piece = action.piece.type
	    		sugested_movement = action.final_position

	    return (max_payoff,sugeste_piece,sugested_movement)

	# Black pieces is min
	def min(self,board,alpha= -float('Inf'),beta=float('Inf')):
		# We're initially setting it to inf as worse than the worst case:
	    min_payoff = float('Inf');

	    sugeste_piece = None
	    sugested_movement = None

	    result = board.is_over();

	    # If the game came to an end, the function needs to return
	    # the evaluation function of the end.
	    if result is not None:
	        return (result, None, None)

	    possible_actions = board.getPossibleActions('b')

	    for action in possible_actions:
	    	# For each possible action, W player makes a move and calls Min
	    	# That's one branch of the game tree.
	    	new_board = deepcopy(board)
	    	new_board.updateBoard(action);
	    	new_board.moves += 1
	    	
	    	(m,sp,sm) = self.max(new_board,alpha,beta)

	    	# Fixing the max value if needed
	    	if m < min_payoff:
	    		min_payoff = m
	    		sugeste_piece = action.piece.type
	    		sugested_movement = action.final_position

	    return (min_payoff,sugeste_piece,sugested_movement)

	def play(self):
		while True:
			self.board.printBoard()
			self.result = self.board.is_over()

			# Printing the appropriate message if the game has ended
			if self.result is not None:
				if self.result > 0:
					print('White wins!');
				elif self.result < 0:
					print('Black wins!');
				elif self.result == 0:
					print("It's a tie!");
				return;

			if self.white_play:
				print('White plays, Evaluating possible moves...')
				start = time.time()
				(m, sp, sm) = self.max(self.board)
				end = time.time()
				print('Evaluation time: {}s'.format(round(end - start, 7)))
				print('Recommended move: Piece = {}, X = {}, Y = {}'.format(sp,sm[0], sm[1]))

				while True:

					pt = str(input('Insert the piece you would like to move - King (k), Bishop (b) or Rook (r): '))
					px = int(input('Insert the X coordinate: '))
					py = int(input('Insert the Y coordinate: '))

					(pp, pm) = (pt, [px,py])
					piece = self.board.getPiece(pp,'w')

					action = Action(piece,pm,self.board)

					if action.is_valid:
						print('{} to [{},{}]'.format(pp,pm[0],pm[1]));
						self.board.updateBoard(action)
						print()
						self.white_play = False
						break
					else:
					    print('The move is not valid! Try again.')

			else:
				print('Black plays, Evaluating possible moves...')
				(m, sp, sm) = self.min(self.board)
				piece = self.board.getPiece(sp,'b')
				action = Action(piece,sm,self.board)
				print('{} to [{},{}]'.format(sp,sm[0],sm[1]))
				self.board.updateBoard(action)
				self.white_play = True



# Define a class for a piece action
class Action:
	def __init__(self,piece=None,destination=[-1,-1],board=None):
		
		self.piece = piece;
		if type(piece) is Piece:
			self.init_position = piece.position;
		else:
			self.init_position = [-1,-1]

		self.final_position = destination;
		self.is_valid = self.isActionValid(board);

	# Defines if an action is valid
	def isActionValid(self,board):
		if type(board) is not Board:
			# print('board is of wrong type.')
			return False;

		if type(self.piece) is not Piece:
			# print('piece is of wrong type.')
			return False;

		if any(p<0 or p>=board.size for p in self.final_position) or any(p<0 or p>=board.size for p in self.init_position):
			# print('action positions are invalid.')
			return False;

		if self.init_position == self.final_position:
			# print('Initial and final positions must be different')
			return False;

		# If there is a piece of the same player at destination than it is not valid
		piece_at_destination = board.getPieceAtPosition(self.final_position);
		if piece_at_destination is not None and piece_at_destination.player == self.piece.player:
			# print('Piece at destination: ',self.final_position)
			# board.printBoard()
			return False;

		if self.piece.type == 'k':
			# print('Is King');
			# If is not a valid move for the King
			if not(abs(self.init_position[0]-self.final_position[0]) <= 1 and abs(self.init_position[1]-self.final_position[1]) <= 1):
					return False;

		elif self.piece.type == 'r':
			# If is not a valid move for Rook
			if self.init_position[0] != self.final_position[0] and self.init_position[1] != self.final_position[1]: 
				return False;
		elif self.piece.type == 'b':
			# If is not a valid move for Bishop
			if abs(self.init_position[0]-self.final_position[0]) != abs(self.init_position[1]-self.final_position[1]):
				# print('Not Valid for Bishop: [{},{}] to [{},{}]'.format(self.init_position[0],self.init_position[1],self.final_position[0],self.final_position[1]))
				return False;
		else:
			print('Not any kind')
			return False;

		return True;


"""
#################### Main code ##########################
"""
# Play game
Game().play()