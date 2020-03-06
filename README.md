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
	+ <img src = "https://render.githubusercontent.com/render/math?math=h_i=h_j"> and <img src="https://render.githubusercontent.com/render/math?math=u=(u_1,\cdots,u_n)">, where <img src="https://render.githubusercontent.com/render/math?math=u_i:Z\mapsto R"> is a utility function for player i on the Z terminal nodes

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

While in a traditional game the movement shown in the figure was not valid due to the existence of pieces between the start and end position of the tower, in the modified version this movement is allowed.

## Modeling in extensive form

As mentioned earlier, the proposed game will be modeled as a zero-sum game of perfect information in extensive form. Game rules in the extensive form are defined by legal positions (or legal states) and legal moves for all legal positions. For each legal position, it is possible to effectively determine all legal movements. Some legal positions are starting positions and others are ending.

The best way to describe these terms is to use a tree chart whose nodes are legal positions and whose borders are legal movements. The graph is directed, as it does not necessarily mean that we will be able to go back exactly where we came from in the previous move. For example, in classical chess, a pawn can only advance. This graph is called a game tree. Moving down the game tree represents one of the players making a move, and the state of the game changes from one legal position to another.

![mod_chess_ext_form](doc/imgs/mod_chess_ext_form.png)

In the figure above, each vertex of the graph represents a possible state of the game, while each edge represents the possible actions to be taken in a given state. The odd levels correspond to the states where the player with the white pieces must take action, while at the even levels, the player with the black pieces must act.

The complete game tree is a game tree whose root is in the starting position and all leaves are in the ending positions. Each complete game tree has as many nodes as the game has possible results for each legal move made. It is easy to notice that, for the game in question, the complete tree is huge and the number of possible states grows exponentially at each level. For this reason, it is not a good practice to explicitly create an entire game tree as a structure when writing a program that should predict the best move at any time. However, nodes must be created implicitly in the visiting process.

## The Algorithm

The purpose of this section is to implement an algorithm that finds the best strategy for the game modeled in the previous section.

The *Backpropagation* algorithm has a systematic search, or more precisely, it uses brute force and a simple evaluation function. In a two-player zero-sum game, one player seeks to minimize the final payoff of the game, while the other seeks to maximize the same. To decide the action to be taken in a given state, the algorithm in its original form performs a search in a complete tree down to the leaves. Effectively, we would analyze all possible results and always be able to determine the best possible move.

However, for non-trivial games, this practice is inapplicable. Even the search to a certain depth sometimes takes an unacceptable amount of time. The *Alpha-Beta Pruning* algorithm optimizes this process by eliminating the search in unnecessary paths and considerably reducing the execution time of the algorithm. Even so, for games like chess, searching the entire tree is not feasible.

To solve this problem, the algorithm used applies the search to a reasonably low tree depth, aided by appropriate heuristics and to a well-designed, but simple, evaluation function. With this approach, we lose the certainty of finding the best possible move, but in most cases the decision made by the algorithm is much better than any human being.

The applied heuristic is as follows:

* Each piece of the game is assigned a value, with positive values for white pieces, and equivalent negative values for black pieces;
* In each state of the game, the *payoff* is calculated according to the sum of the values of the pieces still present on the board;
* The values defined for each piece are:

	+ **Bishop**: <img src = "https://render.githubusercontent.com/render/math?math=\pm\ 3">
	+ **Tower**: <img src = "https://render.githubusercontent.com/render/math?math=\pm\ 5">
	+ **King**: <img src = "https://render.githubusercontent.com/render/math?math=\pm\ 10000">

The implemented algorithm therefore applies the heuristic described to the *Alpha-Beta Pruning* algorithm. With this, it is able to view only a limited number of future moves, but it is able to estimate the best possible move given the *payoffs* of the most distant states viewed.

## Results

The game and the learning algorithm were implemented in Python. The final product consists of a simple game, which allows a human player to play against the computer. The human player plays with the white pieces, and has access to a move suggestion that corresponds to the best move found by the algorithm. That player can follow the algorithm's suggestion or not. The computer, which plays with the black pieces, will always follow the best solution found by the algorithm.

The figures below show the result of a game when both players follow the moves suggested by the algorithm, which can analyze up to 6 future moves.

![pos_ini](doc/imgs/pos_ini.png)

![move_1](doc/imgs/move_1.png)
![move_2](doc/imgs/move_2.png)
![move_3](doc/imgs/move_3.png)
![move_4](doc/imgs/move_4.png)
![move_5](doc/imgs/move_5.png)
![move_6](doc/imgs/move_6.png)
![move_7](doc/imgs/move_7.png)
![move_8](doc/imgs/move_8.png)
![move_9](doc/imgs/move_9.png)
![move_10](doc/imgs/move_10.png)
![move_11](doc/imgs/move_11.png)
![move_12](doc/imgs/move_12.png)
![move_13](doc/imgs/move_13.png)
![move_14](doc/imgs/move_14.png)
![move_15](doc/imgs/move_15.png)
![move_16](doc/imgs/move_16.png)
![move_17](doc/imgs/move_17.png)
![move_18](doc/imgs/move_18.png)
![move_19](doc/imgs/move_19.png)

## Conclusion

Even though the white pieces have the initiative due to the fact of making the initial move, when both players play the  "best" move, the result is always a tie. Due to the simplicity of the game, an experienced human player can tie with the implemented algorithm, but it will hardly come out victorious, even when the algorithm can visualize only 6 future steps. In a more complex game, like classic chess, and with more powerful algorithms and capable of visualizing dozens of future steps, a human player will hardly be able to achieve results that would come close to a computer's.

An interesting point to note is that the *Alpha-Beta Pruning* algorithm achieved an average execution time of around 15 seconds for each evaluation. This value was reduced considerably as the game approached its end, due to the reduction in the number of pieces on the board and, consequently, possible future states. On the other hand, the traditional *Backpropagation* algorithm, obtained much worse results, taking several minutes to find the same result that the *Alpha-Beta Pruning* obtained in seconds. This shows the great optimization and computational advantage that *Alpha-Beta Pruning* offers over the original *Backpropagation* algorithm.

Finally, we can conclude that several real-world situations can be modeled in the form of a game in the extensive form. The *Backpropagation* algorithm is able to find the best solution for any game modeled in this way in exponential time. The *Alpha-Beta Pruning* algorithm is composed of a modified version of the *Backpropagation* and manages to obtain the same optimal result in a much shorter average time. Despite its great results, even the *Alpha-Beta Pruning* algorithm has difficulty finding the optimal result in a timely manner from a sufficiently complex game, such as chess. In these cases, a heuristic is applied to the search algorithm. With a sufficiently well-developed heuristic, the algorithm is able to visualize only a limited number of future moves, but it manages to estimate the best possible move given the *payoffs* of the most distant states viewed.



## References
<a id="mas">[1]</a> 
Yoav Shoham, Kevin Leyton Brown. 
Multi Agent Systems, 
Algorithmic, Game-Theoretic, and Logical Foundations. 2010.