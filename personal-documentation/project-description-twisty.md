
# Twisty!

This is a list of things I had in mind while thinking about how to learn solving the Rubik's cube and how to help to solve other twisty puzzles.

Many papers exist on twisty puzzles, most often to give an example for group theory, but this is not really helping to solve the cube or to assess if a resolution method may lead to annoying parity cases, and how to avoid such cases from the beginning.

The idea of the software would be to provide a way to describe _completely_ any given resolution methods, in order to ease learning such methods and to test if the method has flaws.

This needs to be articulated around a **domain-specific language** based on cube turn sequences plus loops and conditional branching.

## Expected features

In random order:

- Absolute vs relative moves on rotation surfaces
- Orient whole TP e.g. white face down
- Basis is an extended WCA notation see https://www.worldcubeassociation.org/regulations/#12a, see SiGN notation https://www.mzrg.com/rubik/nota.shtml
- Other notations to be supported, output in various notations, see https://rubiks.fandom.com/wiki/Notation
- Include Conjugates [A: B] and Commutators [A, B] in notation see https://www.speedsolving.com/wiki/index.php/Commutators_and_Conjugates
- Space/tab character(s) to separate moves of several characters, accept "." or "*" as multiplication of permutation
- Include support for parenthesis followed by "'" or an integer to repeat moves
- Reduction to be supported https://www.speedsolving.com/wiki/index.php/Reduction_Method
- Gather all used algorithms and display them in a consolidated list to learn the method
- Support canonical/simplest way of defining algorithms, including algorithms with variable moves
- Support creation of reflections and inverses see https://www.mzrg.com/rubik/mirrors.shtml


https://ruwix.com/twisty-puzzles/

https://www.reddit.com/r/Cubers/

https://freshcuber.de/zauberwuerfel-notation/

http://cushan.io/



## WCA Notation

From https://www.worldcubeassociation.org/regulations/#12a

12a) Notation for NxNxN Cubes:

12a1) Face Moves (outer slice):
12a1a) Clockwise, 90 degrees: F (front face), B (back face), R (right face), L (left face), U (upper face), D (bottom face).
12a1b) Counter-clockwise, 90 degrees: F', B', R', L', U', D'.
12a1c) 180 degrees: F2, B2, R2, L2, U2, D2.

12a2) Outer Block Moves (outer slice with adjacent inner slices). For each of the moves defined below, n is the total number of slices to move, which must be in the range 1 < n < N (where N is the number of layers in the puzzle). n may also be omitted, for an implicit value of n = 2 slices. Outer Block Moves are:
12a2a) Clockwise, 90 degrees: nFw, nBw, nRw, nLw, nUw, nDw.
12a2b) Counter-clockwise, 90 degrees: nFw', nBw', nRw', nLw', nUw', nDw'.
12a2c) 180 degrees: nFw2, nBw2, nRw2, nLw2, nUw2, nDw2.

12a4) Rotations (entire puzzle):
12a4a) Clockwise, 90 degrees: x (same direction as R or L'), y (same direction as U or D'), z (same direction as F or B').
12a4b) Counter-clockwise, 90 degrees: x' (same direction as R' or L), y' (same direction as U' or D), z' (same direction as F' or B).
12a4c) 180 degrees: x2, y2, z2.

12a5) Outer Block Turn Metric (OBTM) is defined as:
12a5a) Each move of the categories Face Moves and Outer Block Moves is counted as 1 move.
12a5b) Each move of the Rotations category is counted as 0 moves.

12a6) Execution Turn Metric (ETM) is defined as: Each move of the categories Face Moves, Outer Block Moves, and Rotations is counted as 1 move.


12c) Notation for Square-1:

12c1) Moves are applied with one of the two smallest surfaces of the equatorial slice on the left side of the front face.
12c2) (x, y) means: turn upper layer x times 30 degrees clockwise, turn bottom layer y times 30 degrees clockwise. x and y must be integers from -5 to 6, and cannot be both equal to 0.
12c3) "/" means: turn the right half of the puzzle 180 degrees.
12c4) Metric for Square-1: (x, y) counts as one move, "/" counts as one move.


12d) Notation for Megaminx (scrambling notation only):

12d1) Face Moves:
12d1a) Clockwise, 72 degrees: U (upper face).
12d1b) Counter-clockwise, 72 degrees: U' (upper face).
12d2) Other moves are applied while keeping 3 pieces fixed at the top left of the puzzle:
12d2c) Clockwise 144 degrees move of the whole puzzle except for the slice of top left three pieces: R++ (vertical slices), D++ (horizontal slices).
12d2d) Counter-clockwise 144 degrees move of the whole puzzle except for the slice of top left three pieces: R-- (vertical slices), D-- (horizontal slices).


12e) Notation for Pyraminx:
12e1) The puzzle is oriented with the bottom face completely horizontal and the front face facing the person who is holding the Pyraminx.
12e2) Clockwise, 120 degrees: U (upper 2 layers), L (left 2 layers), R (right 2 layers), B (back 2 layers), u (upper vertex), l (left vertex), r (right vertex), b (back vertex).
12e3) Counter-clockwise, 120 degrees: U' (upper 2 layers), L' (left 2 layers), R' (right 2 layers), B' (back 2 layers), u' (upper vertex), l' (left vertex), r' (right vertex), b' (back vertex).


12g) Notation for Clock:
12g1) The puzzle is oriented with 12 o'clock on top, and either side in front.
12g2) Move pins up: UR (top-right), DR (bottom-right), DL (bottom-left), UL (top-left), U (both top), R (both right), D (both bottom), L (both left), ALL (all).
12g3) Turn a wheel next to an up-position pin and move all pins down afterwards: x+ (x clockwise turns), x- (x counter-clockwise turns).
12g4) Turn around the puzzle so that 12 o'clock stays on top, and then move all pins down: y2.


12h) Notation for Skewb:
12h1) The puzzle is oriented with three faces fully visible, where the upper face is on top.
12h2) Clockwise, 120 degrees: R (the layer around the farthest visible bottom-right vertex), U (the layer around the farthest visible upper vertex), L (the layer around the farthest visible bottom-left vertex), B (the layer around the farthest non-visible back vertex).
12h3) Counter-clockwise, 120 degrees: R' (the layer around the farthest visible bottom-right vertex), U' (the layer around the farthest visible upper vertex), L' (the layer around the farthest visible bottom-left vertex), B' (the layer around the farthest non-visible back vertex).

https://meep.cubing.net/wcanotation.html

https://www.cubelelo.com/blogs/cubing/understanding-rubik-s-cube-notation-for-every-wca-puzzle

https://ruwix.com/the-rubiks-cube/different-rubiks-cube-solving-methods/roux-method/

https://www.speedsolving.com/wiki/index.php/Commutators_and_Conjugates
