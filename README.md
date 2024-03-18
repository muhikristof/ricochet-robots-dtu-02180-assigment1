# ricochet-robots-dtu-02180-assigment1

02180 - Introduction to AI - DTU assignment 1

## Running the code

To run the code, simply run the following command in the terminal:

```bash
pip3 install -r requirements.txt
python3 main.py
```

You'll be greeted with the main menu, where you can choose a map to play on. Currently we have 4 maps: `default`, `easy`, `medium`, and `hard`.

After the game has started, you can select a robot (by pressing `1` to `3`) and then select a direction (by pressing `Arrow Up`, `Arrow Down`, `Arrow Left`, or `Arrow Right`). The goal is to move all robots to their respective targets in the fewest moves possible.

As soon as you've played enough, you can press `Reset` to reset the game, and run some of the algorithms we've implemented. For example, you can run the `BFS` algorithm to find a solution with the fewest moves. As alternative, we've also implemented the `DFS` algorithm, which in some cases might be faster than the `BFS` algorithm, but almost always finds a much, much longer solution. 
`A*` has also been implemented for quicker solving though less optimized solutions.
