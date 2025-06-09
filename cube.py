#!/usr/bin/python
# -*- coding: utf-8 -*-

""" A piece-based representation of a Rubik's cube for experimentation """

import sys, os
from math import pi, cos, sin
from typing import Any, Self

class Vector:
  """ Vector in 3D space with (x, y, z) coordinates and kept original values for later comparison, featuring formulas
      for rotation around an arbitrary axis """

  EPSILON = 1e-6
  "Floating point precision threshold for comparing vector changes"

  _original_x: float
  "Original X coordinate of the vector, used for comparison"

  _original_y: float
  "Original Y coordinate of the vector, used for comparison"

  _original_z: float
  "Original Z coordinate of the vector, used for comparison"

  x: float
  "Current X coordinate of the vector"

  y: float
  "Current Y coordinate of the vector"

  z: float
  "Current Z coordinate of the vector"

  def __init__(self, input:tuple[float,float,float]|list[float]|Self):
    """ Initializes a vector with given coordinates
        :param x: X coordinate
        :param y: Y coordinate
        :param z: Z coordinate
        :return: None """

    # Stores the given coordinates from the input
    if isinstance(input, (tuple, list)):
      if len(input) != 3:
        raise ValueError("Input must be a 3-element tuple or list")
      self.x, self.y, self.z = input
    elif isinstance(input, Vector):
      self.x, self.y, self.z = input.x, input.y, input.z
    else:
      raise TypeError("Input must be a 3-element tuple, list, or Vector")

    # Stores the original vector position for comparison later
    self._original_x = self.x
    self._original_y = self.y
    self._original_z = self.z

  def changed(self) -> bool:
    """ Checks if the vector has changed from its original position
        :return: True if the vector has changed, False otherwise """

    # Compares the current vector with the original vector taking
    # into account the floating point precision issues
    diff = abs(self.x-self._original_x)+abs(self.y-self._original_y)+abs(self.z-self._original_z)
    return diff > self.EPSILON
  
  def rotate(self, rotation_axis:tuple[float,float,float]|list[float]|Self, angle:float=-pi/2):
    """ Rotates the vector by a given `angle` around the given `rotation_axis`
        :param rotation_axis: Axis of rotation given as a 3-element tuple, list, or Vector
        :param angle: Angle of rotation in radians, default is -pi/2 (90 degrees clockwise)
        :return: None """

    # Checks if the rotation axis is a valid 3D vector and gets the components
    if isinstance(rotation_axis, (tuple, list)):
      if len(rotation_axis) != 3:
        raise ValueError("Rotation axis must be a 3-element tuple or list")
      rax, ray, raz = rotation_axis
    elif isinstance(rotation_axis, Vector):
      rax, ray, raz = rotation_axis.x, rotation_axis.y, rotation_axis.z
    else:
      raise TypeError("Rotation axis must be a 3-element tuple, list, or Vector")

    # Normalizes the rotation axis vector
    length = (rax**2 + ray**2 + raz**2)**0.5
    if length == 0:
      raise ValueError("Axis vector cannot be zero")
    rax /= length
    ray /= length
    raz /= length

    # Computes the rotation matrix (using Rodrigues' rotation formula)
    c = cos(angle)
    s = sin(angle)
    matrix = [[rax*rax*(1-c) + c,     rax*ray*(1-c) - raz*s, rax*raz*(1-c) + ray*s],
              [ray*rax*(1-c) + raz*s, ray*ray*(1-c) + c,     ray*raz*(1-c) - rax*s],
              [raz*rax*(1-c) - ray*s, raz*ray*(1-c) + rax*s, raz*raz*(1-c) + c    ]]

    # Applies the rotation matrix to the vector
    x_new = matrix[0][0] * self.x + matrix[0][1] * self.y + matrix[0][2] * self.z
    y_new = matrix[1][0] * self.x + matrix[1][1] * self.y + matrix[1][2] * self.z
    z_new = matrix[2][0] * self.x + matrix[2][1] * self.y + matrix[2][2] * self.z

    # Updates the vector with the new coordinates
    self.x = x_new
    self.y = y_new
    self.z = z_new

  def __mul__(self, scalar: float):
    """Returns a new Vector scaled by the given scalar (v * scalar)"""
    if not isinstance(scalar, (int, float)):
      return NotImplemented
    return Vector((self.x * scalar, self.y * scalar, self.z * scalar))

  def __rmul__(self, scalar: float):
    """Returns a new Vector scaled by the given scalar (scalar * v)"""
    return self.__mul__(scalar)

  def __neg__(self):
    """Returns a new Vector with all components negated (-v)"""
    return Vector((-self.x, -self.y, -self.z))

  def __str__(self):
    """ Returns a string representation of the vector in the format (x, y, z) """

    return f"({self.x:.2f}, {self.y:.2f}, {self.z:.2f})"
  
  def __repr__(self):
    """ Returns a string representation of the vector for debugging """

    return f"Vector(({self.x}, {self.y}, {self.z}))"

class Orientation:
  """ Orientation of a piece in 3D space, represented by normal vectors for each axis """

  ax: Vector
  "Normal vector for the X axis"

  ay: Vector
  "Normal vector for the Y axis"

  az: Vector
  "Normal vector for the Z axis"

  def __init__(self, ax:Vector=Vector((1,0,0)), ay:Vector=Vector((0,1,0)), az:Vector=Vector((0,0,1))):
    """ Initializes the orientation with given normal vectors
        :param ax: Normal vector for the X axis
        :param ay: Normal vector for the Y axis
        :param az: Normal vector for the Z axis
        :return: None """

    self.ax = Vector(ax)
    self.ay = Vector(ay)
    self.az = Vector(az)

  def rotate(self, rotation_axis:tuple[float,float,float]|list[float]|Vector, angle:float=pi/2):
    """ Rotates the orientation around the given axis by the given angle
        :param rotation_axis: Axis of rotation (X, Y, Z)
        :param angle: Angle of rotation in radians, default is pi/2 (90 degrees)
        :return: None """

    # Rotates each normal vector of the orientation
    self.ax.rotate(rotation_axis, angle)
    self.ay.rotate(rotation_axis, angle)
    self.az.rotate(rotation_axis, angle)

  def changed(self) -> bool:
    """ Checks if the orientation has changed from its original position
        :return: True if the orientation has changed, False otherwise """

    return self.ax.changed() or self.ay.changed() or self.az.changed()

  def __repr__(self):
    """ Returns a string representation of the orientation with the normals of each axis """

    return f"Orientation(ax={self.ax}, ay={self.ay}, az={self.az})"

class Piece:
  """ Single piece of a twisty puzzle with its `position` in 3D space, a set of string-based
      `properties` such as colors to recognize the piece and an `orientation` around the axes """

  position: Vector
  "Position of the piece in 3D space"

  properties:  set[str]
  "Properties of this piece such as colors, e.g. {'W', 'R', 'G'}"

  orientation: Orientation
  "Orientation of the piece represented as an Orientation object"

  _orientation_check: bool
  "If True, the orientation of the piece is important to check if the puzzle is solved"

  def __init__(self, position: Vector|tuple[float,float,float]|list[float],
               properties: str|set[str]='', orientation_check:bool=True):
    """ Initializes a single piece, part of a twisty puzzle, at its original `position` within the
        puzzle, keeping track of its orientation using a set of `normals`, plus some `properties`
        used to recognize the piece, e.g. a set of letter-coded colors.

        :param position: A Vector or a tuple of 3 floats representing the position of the piece
        :param properties: A set of strings or a string of space-separated properties of this
        piece e.g. colors like 'O Y B' or 'W R G'
        :param orientation_check: If True, the orientation of the piece is important to check if
        the puzzle is solved, otherwise the piece can have any orientation (given other constraints
        on its position), in the standard 3x3x3 Rubik's cube, the orientation of the center pieces
        does not matter, but the orientation of the edge and corner pieces does matter
        :return: None """

    # Stores directly some provided values
    self._orientation_check = orientation_check

    # Initializes the position of the piece
    self.position = Vector(position)

    # Initializes the properties of the piece
    if isinstance(properties, str):
      self.properties = {x for x in properties.split(' ')}
    else:
      self.properties = properties

    # Initializes the orientation of the piece
    self.orientation = Orientation()

  def rotate(self, rotation_axis:tuple[float,float,float]|list[float]|Vector,
             clockwise:bool=True):
    """ Rotates the piece 90° around the given `rotation_axis`
        :param rotation_axis: Axis of rotation (X, Y, Z)
        :param clockwise: If True, rotates clockwise, otherwise counter-clockwise
        :return: Nothing, modifies the piece in place """

    # Computes angle
    angle = -pi/2 if clockwise else pi/2

    # Rotates the position vector of the piece
    self.position.rotate(rotation_axis, angle)

    # Rotates the orientation normals of the piece
    self.orientation.rotate(rotation_axis, angle)


  def _position_changed(self) -> bool:
    """ Checks if the position of the piece has changed
        :return: True if the position has changed, False otherwise """

    return self.position.changed()

  def _orientation_changed(self) -> bool:
    """ Checks if the orientation of the piece has changed
        :return: True if the orientation has changed, False otherwise """

    # If the orientation does not matter, we can skip the check
    if not self._orientation_check:
      return False

    # Checks if any of the normal vectors have changed
    return self.orientation.changed()

  def changed(self) -> bool:
    """ Checks if the piece has changed from its original position and orientation
        :return: True if the piece has changed, False otherwise """

    return self._position_changed() or self._orientation_changed()

  def __str__(self):
    """ Returns a string representation of the piece with a "~" prefix if the orientation has
        changed, a concatenation of the properties, and a "." suffix if the position has changed """

    res = "~" if self._orientation_changed() else " "
    res += ''.join(sorted(self.properties))
    res += "." if self._position_changed() else ""

    return res

  def __repr__(self):
    """ Returns a string representation of the piece for debugging """

    res = f"position={self.position}, properties={self.properties}, "
    res += f"orientation_check={self._orientation_check}, orientation={self.orientation}"
    res = f"Piece({res})"
    return res

class Cube:
  r""" 3x3x3 Rubik's cube built from its `pieces` (3 dimensional array of `Piece` objects)

                     A
                     | \_/
                     |  |
                     |
            +-------+|------+-------+
           /       / |     /       /|
          +-------+--|----+-------+ |
         /       /       /       /| |
        +-------+-------+-------+ | +
       /       /       /       /| |/|
      +-------+-------+-------+ | + |
      |       |       |       | |/| |
      |       |       |       | + | +
      |       |       |       |/| -------->
      +-------+-------+-------+ | + |  \/
      |       |       |       | |/| |  /\
      |       |       |       | + | +
      |       |  /    |       |/| |/
      +-------+-/-----+-------+ | +
      |       |/      |       | |/
      |       /       |       | +
      |      /|       |       |/
      +-----/-+-------+-------+
           /    __
          /      /
         L      /_ """

  pieces: list[list[list[Piece]]]
  "3D list of pieces, where each piece is a `Piece` object"

  orientation: Orientation
  "Orientation of the cube used to apply the turns"

  def __init__(self):

    """ Initializes a 3x3x3 Rubik's cube with its pieces in their standard orientations """

    # Initializes the default orientation of the cube
    self.orientation = Orientation()

    # Initializes the empty structure
    dummy_piece = Piece((0, 0, 0), "DUMMY")
    self.pieces = [[[dummy_piece for z in range(-1, 2)] for y in range(-1, 2)] for x in range(-1, 2)]

    # Standard WCA orientation for 3x3x3: white up, green front
    self._add_piece(-1, -1, -1, 'O Y B')
    self._add_piece(-1, -1,  0, 'O Y')
    self._add_piece(-1, -1,  1, 'O Y G')
    self._add_piece(-1,  0, -1, 'O B')
    self._add_piece(-1,  0,  0, 'O', False)
    self._add_piece(-1,  0,  1, 'O G')
    self._add_piece(-1,  1, -1, 'O W B')
    self._add_piece(-1,  1,  0, 'O W')
    self._add_piece(-1,  1,  1, 'O W G')
    self._add_piece( 0, -1, -1, 'Y B')
    self._add_piece( 0, -1,  0, 'Y', False)
    self._add_piece( 0, -1,  1, 'Y G')
    self._add_piece( 0,  0, -1, 'B', False)
    self._add_piece( 0,  0,  0, '', False) # Center piece, no colors
    self._add_piece( 0,  0,  1, 'G', False)
    self._add_piece( 0,  1, -1, 'W B')
    self._add_piece( 0,  1,  0, 'W', False)
    self._add_piece( 0,  1,  1, 'W G')
    self._add_piece( 1, -1, -1, 'R Y B')
    self._add_piece( 1, -1,  0, 'R Y')
    self._add_piece( 1, -1,  1, 'R Y G')
    self._add_piece( 1,  0, -1, 'R B')
    self._add_piece( 1,  0,  0, 'R', False)
    self._add_piece( 1,  0,  1, 'R G')
    self._add_piece( 1,  1, -1, 'R W B')
    self._add_piece( 1,  1,  0, 'R W')
    self._add_piece( 1,  1,  1, 'R W G')

  def _add_piece(self, x: int, y: int, z: int, colors: str, orientation_check: bool = True):
    """ Adds a piece to the cube at the given coordinates with the given colors
        :param x: X coordinate of the piece
        :param y: Y coordinate of the piece
        :param z: Z coordinate of the piece
        :param colors: Space-separated string of colors for the piece
        :param orientation_check: If True, the orientation of the piece matters
        :return: None """
    
    if not (-1 <= x <= 1 and -1 <= y <= 1 and -1 <= z <= 1):
      raise ValueError("Coordinates must be in the range [-1, 1] for a 3x3x3 cube")

    self.pieces[x][y][z] = Piece(Vector((x, y, z)), colors, orientation_check=orientation_check)

  def __str__(self):
    """ Returns a string representation of the cube for printing it in a console, e.g.:

          Y
          |
          O---X
          /
        Z

              +-------+-------+-------+
            /  BOW  /  BW   /  BRW  / 
            +-------+-------+-------+  
          /  OW   /  W    /  RW   /   
          +-------+-------+-------+    
        /  GOW  /  GW   /  GRW  /     
        +-------+-------+-------+      

              +-------+-------+-------+
            /  BO   /  B    /  BR   / 
            +-------+-------+-------+  
          /  O    /       /  R    /   
          +-------+-------+-------+    
        /  GO   /  G    /  GR   /     
        +-------+-------+-------+      

              +-------+-------+-------+
            /  BOY  /  BY   /  BRY  / 
            +-------+-------+-------+  
          /  OY   /  Y    /  RY   /   
          +-------+-------+-------+    
        /  GOY  /  GY   /  GRY  /     
        +-------+-------+-------+     """

    res = ""

    # Draws the cube layers
    for y in range(1, -2, -1):
      res += "      +-------+-------+-------+\n"
      for z in range(-1, 2):
        res += " "*(2*(2-z) - 1) + "/ "
        for x in range(-1, 2):
          res += str(self.pieces[x][y][z]).ljust(5)[:5] + " / "
        res += "\n" + " "*(2*(2-z) - 2) + "+-------+-------+-------+\n"
      res += "\n"

    return res

  def __repr__(self):
    """ Returns a string representation of the cube for debugging """
    return f'Cube(pieces={self.pieces})'


  def solved(self) -> bool:
    """ Checks if the cube is solved (all pieces in original position and orientation) """
    for x in range(-1, 2):
      for y in range(-1, 2):
        for z in range(-1, 2):
          if self.pieces[x][y][z].changed():
            return False
    return True

  def rotate_face(self, face: str, clockwise: bool = True):
    """ Turns a face of the cube
        :param face: The face to turn (U, D, L, R, F, B)
        :param clockwise: If True, turn clockwise, else counter-clockwise
        :return: None """

    # Determines the rotation axis based on the face
    if face == 'U':
      rotation_axis = self.orientation.ay
    elif face == 'D':
      rotation_axis = -self.orientation.ay
    elif face == 'R':
      rotation_axis = self.orientation.ax
    elif face == 'L':
      rotation_axis = -self.orientation.ax
    elif face == 'F':
      rotation_axis = self.orientation.az
    elif face == 'B':
      rotation_axis = -self.orientation.az
    else:
      raise ValueError("Invalid face. Use 'U', 'D', 'L', 'R', 'F', or 'B'.")

    # Gets the rotation axis as indices
    rx = int(rotation_axis.x)
    ry = int(rotation_axis.y)
    rz = int(rotation_axis.z)

    print(f"\nRotating face {face} around {rotation_axis}")
    print(f"rx={rx}, ry={ry}, rz={rz}, clockwise={clockwise}")

    # Determines the pieces to be rotated
    pieces:list[Piece] = []
    for x in (range(-1, 2) if rx==0 else [rx]):
      for y in (range(-1, 2) if ry==0 else [ry]):
        for z in (range(-1, 2) if rz==0 else [rz]):
          pieces.append(self.pieces[x][y][z])

    # Rotates the pieces and replaces them in the 3D array
    for piece in pieces:
      piece.rotate(rotation_axis, clockwise)

      # Replaces the piece in the 3D array at its new position, taking into account the rounding
      # to avoid floating point precision issues
      x, y, z = round(piece.position.x), round(piece.position.y), round(piece.position.z)
      self.pieces[x][y][z] = piece

# Tests Vector class
v = Vector((1,0,0))
rv = Vector((0,1,0))
print(f"\nTesting Vector class, starting with vector {v}, rotation vector={rv}")

done = False
while not done:
  v.rotate(rv)
  print(f"After 90° rotation clockwise v={v}, v.changed={v.changed()}")
  done = not v.changed()

#sys.exit(0)

# Tests Piece class
rv = Vector((1,0,0))
piece = Piece(Vector((1,1,1)), 'W R G')
print(f"\nTesting Piece class {piece} rotation vector {rv}")
print(f"{repr(piece)}")

done = False
while not done:
  piece.rotate(rv)
  print(f"\nAfter 90° rotation clockwise:piece={piece}, changed={piece.changed()}",
        f"_position_changed={piece._position_changed()}",
        f"_orientation_changed={piece._orientation_changed()}")
  print(f"Position {piece.position}, {piece.orientation}")
  done = not piece.changed()

#sys.exit(0)

# Creates complete cube and prints it
cube = Cube()
print("\nTesting Cube class, starting with solved cube:\n" + str(cube))

cube.rotate_face('R')

print("After rotation on Right Red face clockwise:\n" + str(cube))

#sys.exit(0)

cube.rotate_face('R')
cube.rotate_face('R')
cube.rotate_face('R')

print("After completing rotation on Right Red face clockwise:\n" + str(cube))

print("Counts the turns to reach in the cube:")

done = False
turns = 0
while not done:

  cube.rotate_face('R')
  cube.rotate_face('U')

  turns += 1
  print(f"\nAfter {turns} time (R U) clockwise:\n" + str(cube))

  done = cube.solved()

print(f"\nCube is solved after {turns} turns (R U)")

