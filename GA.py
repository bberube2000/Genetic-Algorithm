"""
Name: Ben Berube
Date: 09/25/2021
Course: ELEC 494
Genetic Algorithm 

"""
import random
 #Initialize the gene pool
def randomGenome(length):
    sequence = list() #Create new empty sequence
    i = 0
    while(i < length):
        sequence.append(random.randint(0,1)) #Fill the list
        i += 1
    return sequence

def makePopulation(size, length):
    j = 0
    geneList = []
    while (j < size):
        #Generate a random gene sequence
        geneList.append(randomGenome(length))
        j += 1
    return geneList

#Sum the collective bit values in a single gene sequence
def fittness(genome):
    total = 0
    for i in range(len(genome)):
        total += genome[i]
    return total

#Uses roulette-wheel selection to return a random genome from the population 
def selectPair(population):
    i = 0
    fittness_sum = 0
    #Generate random number representing a genome in population
    r = random.randint(0, len(population) - 1)
    for i in range(len(population)-1):
        #Accumulate fittness of genomes in population
        fittness_sum += fittness(population[i])
        if fittness_sum > r:
            #Return genome at desired random index of population
            return population[i]
        i += 1
      
#Combine multiple functions in order to run an interation of replacement within the population
def replace(population, CROSSOVER_RATE, MUTATION_RATE):
    #Random variables between 0-1 to decide possibilty of mutation and crossover
    r = random.random()
    b = random.random()
    #Find the two worst perforoming genomes in the population
    i = 0
    #Loop through the population to find weakest genome (simulate sorting)
    min_fittness = fittness(population[i])
    temp_one = population[i]
    for i in range(len(population) - 1):
        if (min_fittness > fittness(population[i + 1])):
            min_fittness = fittness(population[i + 1])
            temp_one = population[i + 1]
            i += 1
        else:
            i += 1
    #Remove weakest genome found
    population.remove(temp_one)
    #Repeate process to remove second worst genome
    j = 0
    second_min_fittness = fittness(population[j])
    temp_two = population[j + 1]
    #Loop through the population again to find the second worst genome
    for j in range(len(population)-1):
        if (second_min_fittness > fittness(population[j + 1])):
            second_min_fittness = fittness(population[j + 1])
            temp_two = population[j + 1]
            j += 1
        else:
            j += 1
    #Remove second weakest genome
    population.remove(temp_two)
    #Runs both crossover and mutation
    if ((r <= CROSSOVER_RATE) & (b <= MUTATION_RATE)):
        #Perorm crossover on the genomes selected from the population
        genome_one = selectPair(population)
        genome_two = selectPair(population)
        #Return the new genes after crossover is performed
        new_gene_one, new_gene_two = crossover(genome_one, genome_two)
        #Call mutation function on both of the altered genomes
        population.append(mutate(new_gene_one))
        population.append(mutate(new_gene_two))

    #Runs just crossover
    elif ((r <= CROSSOVER_RATE) & (b > MUTATION_RATE)):
        #Perorm crossover on the genomes selected from the population
        genome_one = selectPair(population)
        genome_two = selectPair(population)
        #Return the new genes after crossover is performed
        new_gene_one, new_gene_two = crossover(genome_one, genome_two)
        population.append(mutate(new_gene_one))
        population.append(mutate(new_gene_two))

    #Runs just mutation 
    elif ((r > CROSSOVER_RATE) & (b <= MUTATION_RATE)):
        genome_one = selectPair(population)
        genome_two = selectPair(population)
        population.append(mutate(genome_one))
        population.append(mutate(genome_two))

    #No crossover or mutation occurs
    elif ((r > CROSSOVER_RATE) & (b > MUTATION_RATE)):
        genome_one = selectPair(population)
        genome_two = selectPair(population)
        population.append(genome_one)
        population.append(genome_two)

    #Return population after having removed the two weakest genomes and replaced two more into the population
    return population 
    
def crossover(genome1, genome2):
    #Calculate random index to cross over
    flip_index = random.randint(0, len(genome1)-1)
    #Initialize head and tail sections of both genomes 
    tail_one = genome1[flip_index:len(genome1)]
    tail_two = genome2[flip_index:len(genome2)]
    head_one = genome1[0:flip_index]
    head_two = genome2[0:flip_index]

    #Initialize new offspring
    offspring_one = []
    offspring_two = []
    #Concatenate the respective head and tails to generate new offspring
    offspring_one = head_one + tail_two
    offspring_two = head_two + tail_one
    #Return altered genomes 
    return offspring_one, offspring_two


#Randomly flip a bit of a genome if permitted by mutation rate
def mutate(genome):
    #Find a random location within the genome
    bit = random.randint(0,len(genome)-1)
    #Flip the bit
    if genome[bit] == 1:
        genome[bit] = 0
    else:
        genome[bit] = 1   
    return genome


#Analyze the current population, finding both the average fitness of the pool as well as
#the highest performing (most fit) genome
def evaluateFitness(population):
    i = 0
    max = fittness(population[i])
    #Calculate the highest fittness of the population
    while (i < (len(population) - 1)):
        if (max < fittness(population[i + 1])):
            max = fittness(population[i + 1])
            i += 1
        else:
            i += 1

    #Calculate the average fittness of the population
    j = 0
    mass = 0.0
    while (j < (len(population) - 1)):
        mass += fittness(population[j])
        j += 1
    #Divide mass by size of population to find average
    avg = (mass / len(population))
    return round(avg,2), max

def runGA(SIZE, LENGTH, CROSSOVER_RATE, MUTATION_RATE, logFile):
    #Initialize the population
    population = makePopulation(SIZE, LENGTH)
    generation = 0
    #Run fittness calculation over initial population
    fittness_results = evaluateFitness(population)
    while (generation < 500):
        #The desired fittness result from the population was found
        if (fittness_results[1] == LENGTH):
            #Write to logFile and terminate GA
            logFile.write(str(generation) + "\t" + str(fittness_results[0]) + "\t" + str(fittness_results[1]))
            logFile.write("\n")
            print("Generation  ",generation,": average fittness =",fittness_results[0],", best fittness = ",fittness_results[1])
            return True #GA successfully completed
        #Continue to the next generation and write to logFile
        else:
            print("Generation  ",generation,": average fittness =",fittness_results[0],", best fittness = ",fittness_results[1])
            logFile.write(str(generation) + "\t" + str(fittness_results[0]) + "\t" + str(fittness_results[1]))
            logFile.write("\n")
            #Run replacement again since optimal solution was not found
            new_population = replace(population, CROSSOVER_RATE, MUTATION_RATE)
            fittness_results = evaluateFitness(new_population)
            generation += 1
    
    


if __name__ == "__main__":
    #Set initial parameters for GA simulation
    CROSSOVER_RATE = 0.7
    MUTATION_RATE = 0.01
    LENGTH = 20
    SIZE = 100
    #Initialize output logFile
    outF = open("GAlog.txt", "w")
    print("GENETIC ALGORITHM")
    print("Population size: ",SIZE)
    print("Genome length: ",LENGTH)
    #Run simulation
    success = runGA(SIZE, LENGTH, CROSSOVER_RATE, MUTATION_RATE, outF)
    #Test for success of finding optimal solution, report error if not found witin 500 generations
    if (success == 1):
        print("GA Successfully executed")
    else:
        print("Failed to reach optimal solution")
    outF.close()

    
    
