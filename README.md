# Checkers Endgame

This is a Checkers AI that simulates an endgame of checkers using alpha-beta pruning to determine the optimal moves in a checkers game. 
The rules follow the Standard English Draughts version. A standard 8x8 checkers board is represented by a grid of string characters, for example: 

........

....b...

.......R

..b.b...

...b...r

........

...r....

....B...

The red players are denoted by 'r', and red kings are represented with 'R'. Similarly, a black player is 'b' and a black king is 'B'. 
It is assumed that the red player will always start, and the code writes into an output file the solution to the game - it will print 
the sequence of states from the given initial state to the terminal state. The regular red players can only travel up the board, while the regular black players
can only travel down. Once a player reaches the opposite end of the board, it becomes a king and can travel in any direction. 

A state is considered terminal if there is a winning and losing player; a player wins if the other player has no pieces left on the 
board, or if the other player has no legal moves left. 

The game is solved using an alpha beta search with a depth limit. The evaluation function to estimate the utility of a given state is 
based off of the number and type of pieces on the board for a given player. For example, a regular player is worth 1 point while a 
king is worthh 2.5 points. 

## Running the Code

The code can be run by inputting a board of the previous format into a file (input.txt) and saving it. The solution will be written 
into the output file (output.txt), and the terminal can also print the time it takes to find a solution, the number of total moves taken, etc.
The terminal command is: 


       python3 checkers.py --inputfile input.txt --outputfile output.txt
