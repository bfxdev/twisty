:py:mod:`cube`
==============

.. py:module:: cube

.. autodoc2-docstring:: cube
   :allowtitles:

Module Contents
---------------

Classes
~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`Piece <cube.Piece>`
     - .. autodoc2-docstring:: cube.Piece
          :summary:
   * - :py:obj:`Cube <cube.Cube>`
     - .. autodoc2-docstring:: cube.Cube
          :summary:

Data
~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`c <cube.c>`
     - .. autodoc2-docstring:: cube.c
          :summary:

API
~~~

.. py:class:: Piece(colors: str, orientation: list[int] = [0, 0, 0])
   :canonical: cube.Piece

   .. autodoc2-docstring:: cube.Piece

   .. rubric:: Initialization

   .. autodoc2-docstring:: cube.Piece.__init__

   .. py:attribute:: colors
      :canonical: cube.Piece.colors
      :type: set[str]
      :value: None

      .. autodoc2-docstring:: cube.Piece.colors

   .. py:attribute:: orientation
      :canonical: cube.Piece.orientation
      :type: list[int]
      :value: None

      .. autodoc2-docstring:: cube.Piece.orientation

   .. py:method:: __str__()
      :canonical: cube.Piece.__str__

      .. autodoc2-docstring:: cube.Piece.__str__

   .. py:method:: __repr__()
      :canonical: cube.Piece.__repr__

      .. autodoc2-docstring:: cube.Piece.__repr__

.. py:class:: Cube()
   :canonical: cube.Cube

   .. autodoc2-docstring:: cube.Cube

   .. rubric:: Initialization

   .. autodoc2-docstring:: cube.Cube.__init__

   .. py:attribute:: pieces
      :canonical: cube.Cube.pieces
      :type: list[list[list[cube.Piece | None]]]
      :value: None

      .. autodoc2-docstring:: cube.Cube.pieces

   .. py:method:: __str__()
      :canonical: cube.Cube.__str__

      .. autodoc2-docstring:: cube.Cube.__str__

   .. py:method:: __repr__()
      :canonical: cube.Cube.__repr__

      .. autodoc2-docstring:: cube.Cube.__repr__

.. py:data:: c
   :canonical: cube.c
   :value: 'Cube(...)'

   .. autodoc2-docstring:: cube.c
