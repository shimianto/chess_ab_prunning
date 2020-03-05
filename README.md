# Implementation of an Alpha-Beta Pruning algorithm to play a simplified version of chess

The objective of this activity comprises the study and modeling of an *alpha-beta pruning* algorithm for its application in a modified version of a chess game.

## Introduction

There are several ways of representing games, the simplest of which may be the normal way. However, representations of games in normal form do not incorporate any notion of sequence, or time, of players' actions. The extended form (or tree) is an alternative representation that makes the temporal structure explicit.

One way of classifying games in the extensive form is between games of perfect information and games of imperfect information. Informally, a perfect information game in extensive form (or, more simply, a perfect information game) is a tree in the sense of graph theory, in which each node represents the choice of one of the players, each edge represents a possible action , and the sheets represent final results on which each player has a utility function. In fact, in certain circles (in particular, in artificial intelligence), they are known simply as hunting trees. Formally, we define them as follows: [[1]](#mas)

* **Perfect information games:** *A (finite) game of perfect information (in long form) is a tuple*
<img src="https://render.githubusercontent.com/render/math?math=G = (N, A, H, Z, \chi, \rho, \sigma, u)">, *where:*
	+ *N* is a set of n players;
	+ *A* is a set of actions;
	+ *H* is a set of non-terminal choice nodes;
	+ *Z* is a set of terminal choice nodes, dislocated from *H*;
	+ <img src = "https://render.githubusercontent.com/render/math?math=\chi: H \mapsto 2^A"> is the action function, which assigns each choice node a set of actions possible;
	+ <img src = "https://render.githubusercontent.com/render/math?math=\rho: H \mapsto N"> is the function of the player, who assigns to each non-terminal node of a given player <img src="https://render.githubusercontent.com/render/math?math=i\in N"> that chooses an action on that node;
	+ <img src = "https://render.githubusercontent.com/render/math?math=\sigma: H \times A \mapsto H \cup Z"> is the successor function, which maps a choice node and a action for a new choice node or terminal node, so that for all <img src = "https://render.githubusercontent.com/render/math?math=h_i,h_j\in H"> and <img src = "https://render.githubusercontent.com/render/math?math=a_i,a_j\in A"> if <img src = "https://render.githubusercontent.com/render/math?math=\sigma (h_i, a_i) = \sigma (h_j, a_j) "> then <img src =" https://render.githubusercontent.com/render/math?math=h_i=h_j "> and <img src =" https: //render.githubusercontent.com/render/math?math=a_i=a_j ">;
	+ <img src = "https://render.githubusercontent.com/render/math?math=$h_i=h_j"> and <img src="https://render.githubusercontent.com/render/math?math=u=(u_1,\cdots,u_n)">, where <img src="https://render.githubusercontent.com/render/math?math=u_i:Z\mapsto R"> is a utility function for player i on the Z terminal nodes

The proposal of this work deals with the modeling of a perfect information game in its extensive form and, then, with the application of a *alpha-beta pruning* algorithm modified to find the best action of a player given the state in which the same is found.

## The Game

The modeled game is a simplified version of a game of chess. In a traditional game of chess, two players (white and black pieces) start a game with a total of sixteen pieces each of six different types, on a board with 8x8 squares of alternating colors. The game modeled in this work consists of a 4x4 board, where each player has only three pieces: a king, a rook and a bishop. The figure bellow shows the starting position of the proposed game.

![pos_ini](doc/imgs/pos_ini.png)

In addition to the board size and number of pieces, some rules present in a traditional chess game were disregarded to ensure the simplicity of the model:

* Firstly, in a classic chess game, a player cannot make a move that puts the king himself in check, or that leaves his king in check. This rule has been disregarded and such moves are absolutely valid in the modified version;

* As a consequence of the previous modification, another modification was necessary: ​​under the rules of classical chess, a game ends when a player is in a check position and there are no possible valid moves for it. As positions that leave the king in check are valid in the modified version, in this case the game ends when a player captures the opposing king;

* To prevent the game from going on forever, a tie condition has been established: if the game is in a state where both players have only the king's pieces, the game will end after three moves and, if no player captures the opponent king at this time, the game ends in a draw;

* Finally, each piece has the same moves available in a classic chess game: rook moves horizontally, bishop diagonally and king can move a single square in any direction and no piece can end in a square where a piece of the same color is positioned. However, for the sake of simplicity, a small change to traditional rules was made. While in the game of chess only the horse can "jump" spaces between its home and destination squares that are occupied, this ability has been replicated for all pieces in this new version of the game (as the king can move only one square in a given direction, this rule is irrelevant to it). The figure bellow shows an example of this rule:

![skip_mov](doc/imgs/skip_mov.png)


## References
<a id="mas">[1]</a> 
Yoav Shoham, Kevin Leyton Brown. 
Multi Agent Systems, 
Algorithmic, Game-Theoretic, and Logical Foundations. 2010.