# Implementation of an Alpha-Beta Pruning algorithm to play a simplified version of chess

The objective of this activity is to apply the knowledge acquired during the discipline of Game Theory in Computing. Thus, a non-trivial scenario will be proposed, which will be described informally and formally modeled in a game according to the models seen during the course. The proposed activity for this task, therefore, comprises the study and modeling of an * alpha-beta pruning * algorithm for its application in a modified version of a chess game.

## Introduction

There are several ways of representing games, the simplest of which may be the normal way. However, representations of games in normal form do not incorporate any notion of sequence, or time, of players' actions. The extended form (or tree) is an alternative representation that makes the temporal structure explicit.

One way of classifying games in the extensive form is between games of perfect information and games of imperfect information. Informally, a perfect information game in extensive form (or, more simply, a perfect information game) is a tree in the sense of graph theory, in which each node represents the choice of one of the players, each edge represents a possible action , and the sheets represent final results on which each player has a utility function. In fact, in certain circles (in particular, in artificial intelligence), they are known simply as hunting trees. Formally, we define them as follows: [[1]](#mas)


## References
<a id="mas">[1]</a> 
Yoav Shoham, Kevin Leyton Brown. 
Multi Agent Systems, 
Algorithmic, Game-Theoretic, and Logical Foundations. 2010.