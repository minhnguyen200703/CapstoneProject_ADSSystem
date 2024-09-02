import itertools
import json

# Helper function to get distance between two locations
def get_distance(start, end, distances):
    return distances.get((start, end), float('inf'))

# Function to generate all permutations of locations
def generate_all_paths(start, end, locations):
    all_paths = []
    for perm in itertools.permutations(locations):
        if perm[0] == start and perm[-1] == end:
            all_paths.append(perm)
    return all_paths

# Function to calculate the distance of a given path
def calculate_path_distance(path, distances):
    total_distance = 0
    for i in range(len(path) - 1):
        total_distance += get_distance(path[i], path[i+1], distances)
    return total_distance

# Brute force approach to find the shortest path
def find_shortest_path(start, end, locations, distances):
    paths = generate_all_paths(start, end, locations)
    min_distance = float('inf')
    best_path = None
    
    for path in paths:
        distance = calculate_path_distance(path, distances)
        if distance < min_distance:
            min_distance = distance
            best_path = path
    
    return best_path, min_distance
