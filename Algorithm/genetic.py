# genetic.py
import random
import itertools

# Function to calculate the distance between two locations
def calculate_distance(loc1, loc2, distances):
    for distance in distances:
        if distance["LocationFromID"] == loc1 and distance["LocationToID"] == loc2:
            return float(distance["DistanceKm"])
    return float('inf')  # return a large number if distance is not found

# Function to initialize the population
def initialize_population(trucks, taskjobs, population_size):
    population = []
    truck_ids = list(trucks.keys())
    taskjob_ids = [taskjob["TaskJobID"] for taskjob in taskjobs]
    for _ in range(population_size):
        random.shuffle(truck_ids)
        individual = dict(zip(truck_ids, taskjob_ids))
        population.append(individual)
    return population

# Function to calculate the total distance for a given matching plan
def calculate_total_distance(plan, trucks, taskjobs, distances, containers):
    total_distance = 0
    for truck_id, taskjob_id in plan.items():
        taskjob = next(tj for tj in taskjobs if tj["TaskJobID"] == taskjob_id)
        truck_location = trucks[truck_id]

        if taskjob["TaskJobType"] == "Book_1":
            container_locations = [container["Location"] for container in containers if container["isAvailable"]]
            min_distance = float('inf')
            for container_location in container_locations:
                distance = calculate_distance(str(truck_location), str(container_location), distances) + \
                           calculate_distance(str(container_location), str(taskjob["Locations"][1]), distances)
                if distance < min_distance:
                    min_distance = distance
            total_distance += min_distance
        else:
            distance = calculate_distance(str(truck_location), str(taskjob["Locations"][0]), distances) + \
                       calculate_distance(str(taskjob["Locations"][0]), str(taskjob["Locations"][1]), distances)
            total_distance += distance

    return total_distance

# Function to perform crossover between two parents
def crossover(parent1, parent2):
    child = {}
    for truck_id in parent1.keys():
        if random.random() > 0.5:
            child[truck_id] = parent1[truck_id]
        else:
            child[truck_id] = parent2[truck_id]
    return child

# Function to perform mutation on a child
def mutate(child, mutation_rate, taskjob_ids):
    if random.random() < mutation_rate:
        truck_id = random.choice(list(child.keys()))
        child[truck_id] = random.choice(taskjob_ids)
    return child

# Function to select the best individuals from the population
def selection(population, distances, trucks, taskjobs, containers, selection_size):
    population = sorted(population, key=lambda individual: calculate_total_distance(individual, trucks, taskjobs, distances, containers))
    return population[:selection_size]

# Genetic algorithm function
def genetic_algorithm(trucks, taskjobs, distances, containers, population_size=100, generations=1000, mutation_rate=0.01):
    population = initialize_population(trucks, taskjobs, population_size)
    taskjob_ids = [taskjob["TaskJobID"] for taskjob in taskjobs]

    for generation in range(generations):
        new_population = []

        for _ in range(population_size):
            parent1 = random.choice(population)
            parent2 = random.choice(population)
            child = crossover(parent1, parent2)
            child = mutate(child, mutation_rate, taskjob_ids)
            new_population.append(child)

        population = selection(new_population, distances, trucks, taskjobs, containers, population_size)

    best_individual = population[0]
    best_distance = calculate_total_distance(best_individual, trucks, taskjobs, distances, containers)
    
    return best_individual, best_distance
