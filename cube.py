#!/usr/bin/python

# -*- coding: utf-8 -*-
""" A simple representation of a Rubik's cube with pieces and their colors """

# The cube is represented as a 3D list of pieces, where each piece is an instance of the Piece class.



#from typing import List, Dict, Set, Any

class Piece:
  """ Single piece of the Rubik's cube with colors and orientation """

  colors:      set[str]
  "Constant colors on the faces of this piece"

  orientation: list[int]
  "Orientation of the piece around the axes, equal to 0,0,0 when the cube is solved"

  def __init__(self, colors: str, orientation: list[int]=[0,0,0]):
    """ Initializes a piece with given colors and orientation
        :param colors: A string of space-separated colors, e.g. 'W R G O B Y'
        :param orientation: A list of three integers representing the original relative orientation
        of the piece
        :return: None """

    self.colors = {x for x in colors.split(' ')}
    self.orientation = orientation

  def __str__(self):
    """ Returns a string representation of the piece """
    return ' '.join(sorted(self.colors))

  def __repr__(self):
    """ Returns a string representation of the piece for debugging """
    return f'Piece(colors={self.colors}, orientation={self.orientation})'

#                A
#                | \_/
#                |  |
#                |
#       +-------+|------+-------+
#      /       / |     /       /|
#     +-------+--|----+-------+ |
#    /       /      /        /| |
#   +-------+-------+-------+ | +
#  /       /       /       /| |/|
# +-------+-------+-------+ | + |
# |       |       |       | |/| |
# |       |       |       | + | +
# |       |       |       |/| -------->
# +-------+-------+-------+ | + |  \/
# |       |       |       | |/| |  /\
# |       |       |       | + | +
# |       |  /    |       |/| |/
# +-------+-/-----+-------+ | +
# |       |/      |       | |/
# |       /       |       | +
# |      /|       |       |/
# +-----/-+-------+-------+
#      /    __
#     /      /
#    L      /_

class Cube:
  """ Rubik's cube with its pieces and methods to manipulate it """

  pieces: list[list[list[Piece|None]]]
  "3D list of pieces, where each piece is a Piece object"

  def __init__(self):

    # Initializes the empty structure
    self.pieces = [[[None for z in range(-1, 2)] for y in range(-1, 2)] for x in range(-1, 2)]

    # Standard WCA orientation for 3x3x3: white up, green front
    self.pieces[-1][-1][-1] = Piece('O Y B')
    self.pieces[-1][-1][ 0] = Piece('O Y')
    self.pieces[-1][-1][ 1] = Piece('O Y G')
    self.pieces[-1][ 0][-1] = Piece('O B')
    self.pieces[-1][ 0][ 0] = Piece('O')
    self.pieces[-1][ 0][ 1] = Piece('O G')
    self.pieces[-1][ 1][-1] = Piece('O W B')
    self.pieces[-1][ 1][ 0] = Piece('O W')
    self.pieces[-1][ 1][ 1] = Piece('O W G')
    self.pieces[ 0][-1][-1] = Piece('Y B')
    self.pieces[ 0][-1][ 0] = Piece('Y')
    self.pieces[ 0][-1][ 1] = Piece('Y G')
    self.pieces[ 0][ 0][-1] = Piece('B')
    self.pieces[ 0][ 0][ 0] = Piece('') # Center piece, no colors
    self.pieces[ 0][ 0][ 1] = Piece('G')
    self.pieces[ 0][ 1][-1] = Piece('W B')
    self.pieces[ 0][ 1][ 0] = Piece('W')
    self.pieces[ 0][ 1][ 1] = Piece('W G')
    self.pieces[ 1][-1][-1] = Piece('R Y B')
    self.pieces[ 1][-1][ 0] = Piece('R Y')
    self.pieces[ 1][-1][ 1] = Piece('R Y G')
    self.pieces[ 1][ 0][-1] = Piece('R B')
    self.pieces[ 1][ 0][ 0] = Piece('R')
    self.pieces[ 1][ 0][ 1] = Piece('R G')
    self.pieces[ 1][ 1][-1] = Piece('R W B')
    self.pieces[ 1][ 1][ 0] = Piece('R W')
    self.pieces[ 1][ 1][ 1] = Piece('R W G')

  def __str__(self):
    """ Returns a string representation of the cube """

    res = ""
    for x in range(-1, 2):
      for y in range(-1, 2):
        for z in range(-1, 2):
          if self.pieces[x][y][z] is not None:
            res += f'Piece at ({x}, {y}, {z}): {self.pieces[x][y][z]}\n'

    return res.strip()

  def __repr__(self):
    """ Returns a string representation of the cube for debugging """
    return f'Cube(pieces={self.pieces})'


c = Cube()
print(c)
