Coconut Delivery Solution
=========================

The solution to Coconut Delivery problem uses Dijkstra algorithm to find
the jet-streams with least energy consumption in a topologically sorted graph
with jet-stream and non-jet-stream edges and mile markers as vertices.

The trick for making it efficient was in how the graph is built:

1. I did not add jet-streams with more energy consumption than required for
flying without jet-streams.

2. For jet-streams with the same start and end markers, I only added a jet
stream with least energy consumption.

3. When filling in the gaps between unconnected jet-stream edges, I only
used ONE non-jet-stream edge instead of creating multiple edges between
each mile marker


Installation
------------
    git clone https://github.com/ElenaHenderson/endgame-challenge.git

Usage
-----
    cd endgame-challenge
    ./endgame.py