* encode game state as tensor
  * grid with each cell as a 1 hot for empty, (stack) tile, (ghost, piece of current)
  * 8-length 1 hot for hold, 3 7-length 1 hots for next
  * 1 nat (real) for level number (gravity)
  * can also literally grab the pygame screen surface as a numpy array. might want to downscale and monochrome it though
* NN stuff
  * conv for grid?
  * REINFORCE, Q, actor-critic
    * all can share conv guy