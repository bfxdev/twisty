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
# +--------+                 RB
# |   <2   |             +------+
# | 1    ^ |             |   T  |
# | V    3 |      +------+------+------+------+
# |   4>   |   BR |  BL  |   L  |   R  |  BR  | BL
# +--------+      +------+------+------+------+
#                        |   B  |
#                        +------+
#                            RB


import copy

class Cube:
  'Rubiks cube with face turn, print and get as string functions'
  def __init__(self):
    'Inits data with classical colors, not scrambled, white on bottom'
    
    # Inits cube with classical colors
    self.cube = {'B' :[['W','W','W'],['W','W','W'],['W','W','W']],
                 'L' :[['B','B','B'],['B','B','B'],['B','B','B']],
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
    res += '        +-------+'

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

    
  def toString(self):
    'Returns a string with concatenated square face colors in bottom-up order'
    
    c = self.cube
    
    # Starts with the lower edges (8 squares)
    res =         c['B'][0][1] +  c['L'][2][1]                                  # Edge B/L
    res += '|' +  c['B'][1][2] +  c['R'][2][1]                                  # Edge B/R
    res += '|' +  c['B'][2][1] + c['BR'][2][1]                                  # Edge B/BR
    res += '|' +  c['B'][1][0] + c['BL'][2][1]                                  # Edge B/BL

    # Lower corners (12 squares)
    res += '|' +  c['B'][0][2] +  c['R'][2][0] +  c['L'][2][2]                  # Corner B/R/L
    res += '|' +  c['B'][0][0] +  c['L'][2][0] + c['BL'][2][2]                  # Corner B/L/BL
    res += '|' +  c['B'][2][2] + c['BR'][2][0] +  c['R'][2][2]                  # Corner B/BR/R
    res += '|' +  c['B'][2][0] + c['BL'][2][0] + c['BR'][2][2]                  # Corner B/BL/BR

    # Middle edges
    res += '|' +  c['L'][1][2] +  c['R'][1][0]                                  # Middle edge L/R
    res += '|' +  c['R'][1][2] + c['BL'][1][0]                                  # Middle edge R/BL
    res += '|' + c['BL'][1][2] + c['BR'][1][0]                                  # Middle edge BL/BR
    res += '|' + c['BR'][1][2] +  c['L'][1][0]                                  # Middle edge BR/L

    # Top edges
    res += '|' +  c['T'][2][1] +  c['L'][0][1]                                  # Top edge T/L
    res += '|' +  c['T'][1][2] +  c['R'][0][1]                                  # Top edge T/R
    res += '|' +  c['T'][0][1] + c['BR'][0][1]                                  # Top edge T/BR
    res += '|' +  c['T'][1][0] + c['BL'][0][1]                                  # Top edge T/BL

    # Top layer corners
    res += '|' +  c['T'][2][2] +  c['L'][0][2] +  c['R'][0][0]                  # Top corner T/L/R
    res += '|' +  c['T'][2][0] + c['BL'][0][2] +  c['L'][0][0]                  # Top corner T/BL/L
    res += '|' +  c['T'][0][0] +  c['R'][0][2] + c['BR'][0][0]                  # Top corner T/R/BR
    res += '|' +  c['T'][0][2] + c['BR'][0][2] + c['BL'][0][0]                  # Top corner T/BR/BL
          
    return res
    
    
  def getDiffs(self):
    'Returns the differences compared to an untouched cube, as a dictionnary LE, LC, ME, TE, TC'

    # Inits variables
    fs = 'WB|WR|WG|WO|WRB|WBO|WGR|WOG|BR|RO|OG|GB|YB|YR|YG|YO|YBR|YOB|YRG|YGO'
    fsl = fs.split('|')
    csl = self.toString().split('|')
    res = {}
    ids = ['LE', 'LC', 'ME', 'TE', 'TC']

    # Checks for differences and fills dictionary with number of diffs per group
    for i in range(len(csl)):
      if csl[i] != fsl[i]:
        j = ids[i / 4]
        if j in res.keys(): 
          res[j] += 1
        else:
          res[j] = 1

    return res
    
    
  def initTurn(self):
    self.old = copy.deepcopy(self.cube)


  def copyLine(self, face, x, y, dx, dy, tface, tx, ty, tdx, tdy):
    'Elementary copy of 3 squares to another place'
    for i in range(3):
      self.cube[tface][tx+i*tdx][ty+i*tdy] = self.old[face][x+i*dx][y+i*dy]


  def copyLineNorm(self, face, ldir, tface, tldir):
    'Elementary copy of line using normalized line directions 1234'
    
    # Determines the exact change vector according to the inout number
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
    
    # Performs copy
    self.copyLine(face,  r[0][0], r[0][1], r[0][2], r[0][3], \
                  tface, r[1][0], r[1][1], r[1][2], r[1][3])


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
      self.copyLineNorm(face, 2, face, 1)
      self.copyLineNorm(face, 3, face, 2)
      self.copyLineNorm(face, 4, face, 3)
      
      # Turns adjacent lines
      self.copyLineNorm(faces['R'][0], faces['R'][1], faces['U'][0], faces['U'][1])
      self.copyLineNorm(faces['U'][0], faces['U'][1], faces['L'][0], faces['L'][1])
      self.copyLineNorm(faces['L'][0], faces['L'][1], faces['D'][0], faces['D'][1])
      self.copyLineNorm(faces['D'][0], faces['D'][1], faces['R'][0], faces['R'][1])


  def turnSequenceOld(self, s):
    'Turns cube according to a complete sequence in a concatenated string'
    i = 0;
    while i < len(s):
      if s[i] == 'R' or s[i] == 'L' or s[i] == 'T' or s[i+1] == 'A' or s[i+1] == 'E':
        self.turn(s[i], s[i+1])
        i += 2
      else:
        self.turn(s[i]+s[i+1], s[i+2])
        i += 3

  def turnSequence(self, s):
    'Turns cube according to a complete sequence in a list'
    
    for t in s:
      self.turn(t[0],t[1])


##################################################################################################

# Recursive function to test algorithms
def testAlgorithm(seq, num, advancement):

  if num == 0:

    # Creates a temporary cube and applies turn sequence
    c = Cube()
    c.turnSequence(seq)
    s = c.getDiffs()

    # If the differences are low enough, displays cube ['LE', 'LC', 'ME', 'TE', 'TC']
    if len(s) > 0 and 'LE' not in s.keys() and 'LC' not in s.keys() and 'ME' not in s.keys() \
       and 'TE' in s.keys():

      # Prints results
      print '\n'
      seqstr = ''
      for m in seq:
        seqstr += m[0] + m[1] + ' '
      print seqstr

      c.printCube()
      print s
      print '\n'

  else:
    for f in ['L','R','T']: # ,'BL']: #, 'B', 'BR']:
      for d in ['E','A']:

        # Recurses by adding another step in the sequence
        l = len(seq)
        if seq == [[]] :
          ns = [[f, d]]
        else:
          ns = copy.deepcopy(seq)
          ns.append([f,d])

        # Prepars sorting out the trivial move sequences
        ok = True
        l = len(ns)
        
        # 3 same moves equals one move in the other direction
        if l >= 3 and ns[l-1] == ns[l-2] and ns[l-2] == ns[l-3] :
          ok = False

        # 2 moves forth and back
        if l >= 2 and ns[l-1][0] == ns[l-2][0] and ns[l-1][1] != ns[l-2][1]:
          ok = False

        if ok:
          # Recurses
          advancement = 1 + testAlgorithm(ns, num-1, advancement)
          
          # Prints advancement
          if advancement % 2000 == 0:
            print seq

  return advancement



###################################################################

c = Cube()
c.turnSequence([['T','E'],['T','E']])
#c.printCube()

# Search for turn sequences
for l in [4,5,6,7,8,10,12,14,16]:
  testAlgorithm([[]], l, 0)
    

