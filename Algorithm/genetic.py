import random
import networkx as nx

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
def calculate_total_distance(plan, trucks, taskjobs, graph, containers):
    total_distance = 0
    for truck_id, taskjob_id in plan.items():
        taskjob = next(tj for tj in taskjobs if tj["TaskJobID"] == taskjob_id)
        truck_location = trucks[truck_id]

        if taskjob["TaskJobType"] == "Book_1":
            container_locations = [container["Location"] for container in containers if container["isAvailable"]]
            min_distance = float('inf')
            for container_location in container_locations:
                try:
                    distance = nx.dijkstra_path_length(graph, truck_location, container_location) + \
                               nx.dijkstra_path_length(graph, container_location, taskjob["Locations"][1])
                    if distance < min_distance:
                        min_distance = distance
                except nx.NetworkXNoPath:
                    continue
            total_distance += min_distance
        else:
            try:
                distance = nx.dijkstra_path_length(graph, truck_location, taskjob["Locations"][0]) + \
                           nx.dijkstra_path_length(graph, taskjob["Locations"][0], taskjob["Locations"][1])
            except nx.NetworkXNoPath:
                distance = float('inf')
            total_distance += distance

    return total_distance

# Function to perform crossover between two parents
def crossover(parent1, parent2):
    child = {}
    for truck_id in parent1.keys():
        if truck_id in parent2:
            if random.random() > 0.5:
                child[truck_id] = parent1[truck_id]
            else:
                child[truck_id] = parent2[truck_id]
        else:
            child[truck_id] = parent1[truck_id]
    return child

# Function to perform mutation on a child
def mutate(child, mutation_rate, taskjob_ids):
    if random.random() < mutation_rate:
        truck_id = random.choice(list(child.keys()))
        child[truck_id] = random.choice(taskjob_ids)
    return child

# Function to select the best individuals from the population
def selection(population, graph, trucks, taskjobs, containers, selection_size):
    population = sorted(population, key=lambda individual: calculate_total_distance(individual, trucks, taskjobs, graph, containers))
    return population[:selection_size]

# Genetic algorithm function
def genetic_algorithm(trucks, taskjobs, graph, containers, population_size=100, generations=1000, mutation_rate=0.01):
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

        population = selection(new_population, graph, trucks, taskjobs, containers, population_size)

    best_individual = population[0]
    best_distance = calculate_total_distance(best_individual, trucks, taskjobs, graph, containers)
    
    return best_individual, best_distance
