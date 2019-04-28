# Title: 
Monte Carlo Stimulation for Aeroplane Chess

## Team Member(s):
Mingyan Gong: wrote parts of functions/test/doctest and analyzed the results
Yifan Bao: Designed and wrote classes and functions/tests and comments/Output of the results/analysis

# Monte Carlo Simulation Scenario & Purpose:
Find the strategies for Aeroplane Chess game.

## Hypothesis:
For the players, stacking the planes can increase the chance to win the game
Controlling the number of planes on the track no more than 1 will be more likely to win the game

## Analytical Summary of your findings: 
When the player chooses to stack the planes or control the number of planes on the track, the wins ratio will increase compared to the situation that the player does not choose any strategies. Therefore, we can conclude that stacking the planes and controlling the number of planes on the track can increase the chance to win Aeroplane Chess. 
Since the wins ratio gets the highest if the player controls the maximum number of planes as 1. Therefore, we can conclude that maximum = 1 is the best option.

## Conclusions: 
Stacking the planes and controlling the number of planes on the track can increase the chance to win Aeroplane Chess. 
Controlling the maximum number of planes on the track as 1 is the best option.

## Instructions on how to use the program:
Please run the 'aeroplane_chess.py'. 
We similate the game with two classes: "Plane" & "Player" and then run it for 500,000 times.

## All Sources Used:
https://en.wikipedia.org/wiki/Aeroplane_Chess
