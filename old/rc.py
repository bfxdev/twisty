#!/usr/bin/python

# Faces: Top, Bottom, Left, Right, Back Left, Back Right
# Colors: White, Red, Yellow, Green, Blue, Orange
#
#        +------+
#        |      |
#        | T  Y |
#        |      |
# +------+------+------+------+
# |      |      |      |      |
# | BL O | L  B | R  R | BR G |
# |      |      |      |      |
# +------+------+------+------+
#        |      |
#        | B  W |
#        |      |
#        +------+
#

class Cube:
  'Rubiks cube with rotate and compare functions'
  
  def __init__(self):
    'Inits data with classical colors, not scrambled, white on bottom'
    self.cube = {'B' :[['W','W','W'],['W','W','W'],['W','W','W']],
                 'L' :[['1','B','2'],['B','B','B'],['4','B','3']],
                 'T' :[['Y','Y','Y'],['Y','Y','Y'],['Y','Y','Y']],
                 'R' :[['R','R','R'],['R','R','R'],['R','R','R']],
                 'BR':[['G','G','G'],['G','G','G'],['G','G','G']],
                 'BL':[['O','O','O'],['O','O','O'],['O','O','O']]}

  def printCube(self):
    'Prints the current state of the cube in ASCII form'

    # Creates a canvas with strings to replace
    res =  '        +-------+\n'
    res += '        | T0 |\n'
    res += '        | T1 |\n'
    res += '        | T2 |\n'
    res += '+-------+-------+-------+-------+\n'
    res += '| BL0 | L0 | R0 | BR0 |\n'
    res += '| BL1 | L1 | R1 | BR1 |\n'
    res += '| BL2 | L2 | R2 | BR2 |\n'
    res += '+-------+-------+-------+-------+\n'
    res += '        | B0 |\n'
    res += '        | B1 |\n'
    res += '        | B2 |\n'
    res += '        +-------+\n'

    # Get the keys and sorts them to start with BL/BR, otherwise replaced by L/R
    keys = self.cube.keys()
    keys.sort()
    
    # Iterates over the keys and 9 positions to create string and replace it
    for k in keys:
      for i in range(3):
        s = ''
        for j in range(3):
          if j != 0:
            s += ' '
          s += self.cube[k][i][j]
        res = res.replace(k + "%d" % i, s)

    # Prints results
    print res

  def initTurn(self):
    self.old = self.cube

  def copyLine(self, face, x, y, dx, dy, tface, tx, ty, tdx, tdy):
    'Elementary copy of 3 squares to another place'
    for i in range(3):
      self.cube[tface][tx+i*tdx][ty+i*tdy] = self.old[face][x+i*dx][y+i*dy]

  def copyLineNorm(self, face, ldir, tface, tldir):
    'Elementary copy of line using normalized line directions 1234'
    ldirs = [ldir, tldir]
    r = [[0,0,0,0],[0,0,0,0]]
    for i in range(2):
      l = ldirs[i]
      if   l == 1:
        r[i] = [0, 0, 1, 0]
      elif l == 2:
        r[i] = [0, 2, 0, -1]
      elif l == 3:
        r[i] = [2, 2, -1, 0]
      elif l == 4:
        r[i] = [2, 0, 0, 1]
    
    self.copyLine(face,  r[0][0], r[0][1], r[0][2], r[0][3], \
                  tface, r[1][0], r[1][1], r[1][2], r[1][3])

# +-----------------+
# |   5>       <2   |
# | 1             6 |
# | V             V |
# |                 |
# | ^             ^ |
# | 8             3 |
# |   4>       <7   |
# +-----------------+

  def turn(self, face, direction):
    'Turns face (B, L, T, R, BR, BL) clockwise (E) or anti-clockwise (A)'
    
    # Creates a list of adjacent faces on Right, Down, Left, Up, with normalized line coordinates
    if face == 'L':
      faces = {'R':['R', 1], 'D':['B', 2], 'L':['BL', 3], 'U':['T', 4]}
    elif face == 'R':
      faces = {'R':['BR', 1], 'D':['B', 3], 'L':['L', 3], 'U':['T', 3]}
    elif face == 'T':
      faces = {'R':['R', 2], 'D':['L', 2], 'L':['BL', 2], 'U':['BR', 2]}
    elif face == 'B':
      faces = {'R':['R', 4], 'D':['BR', 4], 'L':['BL', 4], 'U':['L', 4]}
    elif face == 'BR':
      faces = {'R':['BL', 1], 'D':['B', 4], 'L':['R', 3], 'U':['T', 2]}
    elif face == 'BL':
      faces = {'R':['L', 1], 'D':['B', 1], 'L':['BR', 3], 'U':['T', 1]}

    # Stores the current state of the cube to copy from
    self.initTurn()

    # Different copyLine sequence depending on directions
    if direction == 'E':

      # Turns main face
      self.copyLineNorm(face, 1, face, 2)
      self.copyLineNorm(face, 2, face, 3)
      self.copyLineNorm(face, 3, face, 4)
      self.copyLineNorm(face, 4, face, 1)
      
      # Turns adjacent lines
      self.copyLineNorm(faces['R'][0], faces['R'][1], faces['D'][0], faces['D'][1])
      self.copyLineNorm(faces['D'][0], faces['D'][1], faces['L'][0], faces['L'][1])
      self.copyLineNorm(faces['L'][0], faces['L'][1], faces['U'][0], faces['U'][1])
      self.copyLineNorm(faces['U'][0], faces['U'][1], faces['R'][0], faces['R'][1])
      
    elif direction == 'A':
    
      # Turns main face
      self.copyLineNorm(face, 1, face, 4)
      #self.copyLineNorm(face, 2, face, 1)
      #self.copyLineNorm(face, 3, face, 2)
      #self.copyLineNorm(face, 4, face, 3)
      
      # Turns adjacent lines
      self.copyLineNorm(faces['R'][0], faces['R'][1], faces['U'][0], faces['U'][1])
      self.copyLineNorm(faces['U'][0], faces['U'][1], faces['L'][0], faces['L'][1])
      self.copyLineNorm(faces['L'][0], faces['L'][1], faces['D'][0], faces['D'][1])
      self.copyLineNorm(faces['D'][0], faces['D'][1], faces['R'][0], faces['R'][1])
    
    
    
    
     
# +-----------------+
# |   5>       <2   |
# | 1             6 |
# | V             V |
# |                 |
# | ^             ^ |
# | 8             3 |
# |   4>       <7   |
# +-----------------+


#               RB
#           +------+
#           |   T  |
#    +------+------+------+------+
# BR |  BL  |   L  |   R  |  BR  | BL
#    +------+------+------+------+
#           |   B  |
#           +------+
#               RB


c = Cube()


c.printCube()


c.turn('L','E')


c.printCube()


c.turn('B','E')

c.printCube()





