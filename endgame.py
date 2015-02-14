#!/usr/bin/env python2.7
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


class Marker():
    def __init__(self, id):
        self.id = id
        self.destinations = {}

    def get_destinations(self):
        return self.destinations.keys()

    def add_destination(self, id, energy, isJetStream):
        self.destinations[id] = {'energy': energy, 'isJetStream': isJetStream}


class GraphOfFlightPaths():
    def __init__(self):
        self.markers = {}
        self.lastMarker = 0
        self.energyPerMileWithoutJetStream = None
        
    def get_markers(self):
        return self.markers.keys()

    def add_flight_path(self, start, end, energy, isJetStream):
        if start not in self.get_markers():
            startMarker = Marker(id=start)
            self.markers[start] = startMarker
        else:
            startMarker = self.markers[start]

        if end not in self.get_markers():
            endMarker = Marker(id=end)
            self.markers[end] = endMarker

        startMarker.add_destination(end, energy, isJetStream)

    def build_graph_from_file(self, file):
        with open(file, 'r') as f:
            self.energyPerMileWithoutJetStream = int(f.readline())

            for line in f.readlines():
                start, end, energy = [int(item) for item in line.split(' ')]

                if energy/(end-start) < self.energyPerMileWithoutJetStream and end > start:
                    if (start not in self.get_markers()) or \
                        (start in self.get_markers() and end not in self.markers[start].get_destinations()) or \
                        (start in self.get_markers() and end in self.markers[start].get_destinations() and
                        self.markers[start].destinations[end]['energy'] > energy):
                        self.add_flight_path(start, end, energy, isJetStream=True)

                if end > self.lastMarker:
                    self.lastMarker = end

        self.fill_gaps_in_path()

    def fill_gaps_in_path(self):
        # Add non-jet-stream edges between unconnected jet-stream edges
        markerIds = self.get_markers()
        markerIds.sort()
        if 0 not in markerIds:
            start = 0
            end = min(markerIds)
            energy = self.energyPerMileWithoutJetStream * (end - start)
            self.add_flight_path(start, end, energy, isJetStream=False)

        for i in range(1, len(markerIds)-1):
            if markerIds[i+1] not in self.markers[markerIds[i]].get_destinations():
                energy = self.energyPerMileWithoutJetStream * (markerIds[i+1] - markerIds[i])
                self.add_flight_path(markerIds[i], markerIds[i+1], energy, isJetStream=False)

    def get_minimum_total_energy_and_optimal_sequence_of_jet_streams(self):
        # DAG Shortest Path algorithm to calculate the shortest path using a topologically sorted graph
        minimumEnergyToMarker = [sys.maxsize] * (self.lastMarker + 1)
        predMarker = [None] * (self.lastMarker + 1)
        minimumEnergyToMarker[0] = 0

        markerIds = self.get_markers()
        markerIds.sort()

        for markerId in markerIds:
            for adjacentMarkerId in self.markers[markerId].get_destinations():
                if minimumEnergyToMarker[markerId] + self.markers[markerId].destinations[adjacentMarkerId]['energy'] < minimumEnergyToMarker[adjacentMarkerId]:
                    minimumEnergyToMarker[adjacentMarkerId] = minimumEnergyToMarker[markerId] + self.markers[markerId].destinations[adjacentMarkerId]['energy']
                    predMarker[adjacentMarkerId] = markerId

        destination = self.lastMarker
        optimalSequenceOfJetStreams = []
        minimumTotalEnergy = 0
        while destination > 0:
            if self.markers[predMarker[destination]].destinations[destination]['isJetStream']:
                optimalSequenceOfJetStreams.append((predMarker[destination], destination))
            minimumTotalEnergy = minimumTotalEnergy + self.markers[predMarker[destination]].destinations[destination]['energy']
            destination = predMarker[destination]

        optimalSequenceOfJetStreams.reverse()
        return minimumTotalEnergy, optimalSequenceOfJetStreams

if __name__ == "__main__":
    inputFiles = ['sample_paths.txt', 'flight_paths.txt']

    for file in inputFiles:
        graph = GraphOfFlightPaths()
        print "Input {file}".format(file=file)
        graph.build_graph_from_file(file)
        energy, jetStreams = graph.get_minimum_total_energy_and_optimal_sequence_of_jet_streams()
        print "the minimum total energy needed to fly all {lastMarker} miles is {energy} energy units "\
              "and the optimal sequence of jet streams is {jetStreams}".format(lastMarker=graph.lastMarker,
                                                                               energy=energy,
                                                                               jetStreams=jetStreams)