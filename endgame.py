# Feb 7 2015
# Coconut Delivery
#
# A swallow has an assignment to deliver a coconut to a possibly-insane king. To save energy for the fight,
# the swallow will take advantage of jet streams that will lower his flying energy consumption.
# Before the flight, the delivery service gave the swallow an input file in the following format:
#
# First line contains only 1 integer, which is the constant energy it takes to fly 1 mile WITHOUT jet streams.
#
# Every subsequent line contains 3 space-separated integers: the start mile marker of the jet stream,
# the end mile marker of the jet stream, and lastly an integer denoting the overall energy needed to fly
# that jet streams distance.
#
# For instance, the line 3 7 12 means it takes 12 energy units to fly the 4 miles
# between mile-markers 3 and 7. Jet streams can overlap, but the swallow cannot be on more
# than one jet stream at a time, and it cannot fly partial jet streams.
#
# For simplicity, consider the end mile marker of the farthest jet stream as the end of the flight.
#
# Write a python program that takes in an input file flight_paths to plan out the optimal sequence of jet streams
# the swallow should fly on to minimize his energy consumption throughout the entire flight.
# All integers in the input file are non-negative. As output, print out the minimum total energy and a
# list of tuples denoting the jet streams' endpoints.
#
# For example, given this sample, the minimum total energy needed to fly all 24 miles is 352 energy units,
# and the optimal sequence of jet streams is [(0,5), (6,11), (14,17), (19,24)].

import sys


class Vertex():
    def __init__(self, id):
        self.id = id
        self.successors = {}

    def add_outgoing_edge(self, id, weight):
        self.successors[id] = weight


class Graph():
    def __init__(self):
        self.vertices = {}
        self.lastVertex = 0
        self.defaultEdgeWeight = None

    def add_edge(self, start, end, weight):
        if start not in self.vertices.keys():
            startVertex = Vertex(id=start)
            self.vertices[start] = startVertex
        else:
            startVertex = self.vertices[start]

        if end not in self.vertices.keys():
            endVertex = Vertex(id=end)
            self.vertices[end] = endVertex

        startVertex.add_outgoing_edge(end, weight)

    def build_graph_from_file(self, file):
        with open(file, 'r') as f:
            self.defaultEdgeWeight = int(f.readline())

            for line in f.readlines():
                start, end, weight = [int(item) for item in line.split(' ')]

                if weight/(end-start) < self.defaultEdgeWeight:
                    if (start not in self.vertices.keys() and end not in self.vertices.keys()) or \
                        (start in self.vertices.keys() and end in self.vertices[start].successors.keys() and
                        self.vertices[start].successors[end] > weight):
                        self.add_edge(start, end, weight)

                if end > self.lastVertex:
                    self.lastVertex = end

        # add missing default vertices and edges
        for i in range(0, self.lastVertex, 1):
            if i in self.vertices.keys() and (i + 1) not in self.vertices[i].successors.keys():
                self.add_edge(i, i + 1, self.defaultEdgeWeight)

    def find_optimal_path(self):
        shortest = [sys.maxsize] * (self.lastVertex + 1)
        pred = [None] * (self.lastVertex + 1)
        shortest[0] = 0
        for vertexId in range(0, self.lastVertex + 1, 1):
            for adjacentVertexId in self.vertices[vertexId].successors.keys():
                if shortest[vertexId] + self.vertices[vertexId].successors[adjacentVertexId] < shortest[adjacentVertexId]:
                    shortest[adjacentVertexId] = shortest[vertexId] + self.vertices[vertexId].successors[adjacentVertexId]
                    pred[adjacentVertexId] = vertexId

        destination = self.lastVertex
        optimalPathReversed = []
        totalWeight = 0
        while destination > 0:
            optimalPathReversed.append((pred[destination], destination))
            totalWeight = totalWeight + self.vertices[pred[destination]].successors[destination]
            destination = pred[destination]

        print 'totalWeight',
        print totalWeight
        optimalPathReversed.reverse()
        for route in optimalPathReversed:
            print route


graph = Graph()
graph.build_graph_from_file('sample_paths.txt')
graph.find_optimal_path()