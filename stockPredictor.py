import numpy as np
import random
import time
import collections
import math

###################          SELECTION                #############################
def selection(populationUsingSelection, populationUsingCrossover, populationSize, scoredChromosomeList, selectionAlgo, crossOverAlgo):
    selectionList = []
    chromosome = collections.namedtuple('scoredChromosome', 'chromosome score')

    if selectionAlgo == 0:
        selectionList = selectionSort(populationUsingSelection, scoredChromosomeList)
        print("############################################     ELITIST OUTPUT     #######################################################")
        printList(selectionList)
    elif selectionAlgo == 1:
        selectionList = tournamentSort(populationUsingSelection, scoredChromosomeList)
        print("############################################     TOURNAMENT SORT OUTPUT     #######################################################")
        printList(selectionList)
    if crossOverAlgo == 0:
        for x in range(populationUsingCrossover):
            chromosome = uniform(selectionList)
            selectionList.append(chromosome)
        print("############################################     UNIFORM OUTPUT     #######################################################")
        printList(selectionList)
    elif crossOverAlgo == 1:
        #print("Starting K-Point \n")
        for x in range(populationUsingCrossover):
            crossOverAlgo = kPoint(selectionList)
            selectionList.append(crossOverAlgo)
        print("############################################     K-POINT OUTPUT     #######################################################")
        printList(selectionList)
    return selectionList
#randomly select two chromosomes from the current generation and whichever one has a higher fitness score will be copied
#into the next generation. You do not need to prevent chromosomes from being selected more than once.
def tournamentSort(populationUsingSelection, scoredChromosomeList):
    tournamentList = []
    for x in range(populationUsingSelection):
        chrom1 = random.randint(0, len(scoredChromosomeList) - 1)
        chrom2 = random.randint(0, len(scoredChromosomeList) - 1)
        
        if scoredChromosomeList[chrom1][1] > scoredChromosomeList[chrom2][1]:
            tournamentList.append(scoredChromosomeList[chrom1])
        elif scoredChromosomeList[chrom1][1] < scoredChromosomeList[chrom2][1]:
            tournamentList.append(scoredChromosomeList[chrom2])
        else:
            tournamentList.append(scoredChromosomeList[chrom1])
    return tournamentList

#select x highest fit chromosomes
def selectionSort(populationUsingSelection, scoredChromosomeList = []):
    elitistList = []
    minValue = scoredChromosomeList[0][1]
    minIndex = 0
    lengthScoreChromoList = len(scoredChromosomeList)
    #prefill elite list
    for x in range(populationUsingSelection):
        elitistList.append(scoredChromosomeList[x])
        #find smallest value in new list
        if elitistList[x][1] < minValue:
            minValue = elitistList[x][1]
            minIndex = x
    for y in range(populationUsingSelection, lengthScoreChromoList):
        if scoredChromosomeList[y][1] > elitistList[minIndex][1]:
            #swap the new smallest value
            elitistList[minIndex] = scoredChromosomeList[y]
            if y < lengthScoreChromoList:
                #fin new smallest value
                minIndex = findMinOrMax(populationUsingSelection, 0 , elitistList)
    return elitistList

###################          CROSSOVER                #############################
#Iterate over each of the 5 genes and randomly select whether to use the value from the first parent chromosome or the second parent chromosome. 
def uniform(selectionList):
    childChromosome = collections.namedtuple('scoredChromosome', 'chromosome score')
    childList = []
    chance = -1
    score = 0.0
    parent1 = random.randint(0, len(selectionList) - 1)
    parent2 = random.randint(0, len(selectionList) - 1)

    for i in range(5):
        chance = percentChance(50)
        #fill child list based on 50/50 chance of 2 randomly chosen parents
        if chance == 0:
            childList.append(selectionList[parent1][0][i])
        elif chance == 1:
            childList.append(selectionList[parent2][0][i])
    #organize list    
    for j in range(2):
        if childList[j * 2] > childList[(j * 2) + 1]:
            childList[j * 2] = childList[j * 2] + childList[(j*2) + 1]
            childList[(j * 2) + 1] = childList[j * 2] - childList[(j * 2) + 1]
            childList[j * 2] = childList[j * 2] - childList[(j * 2) + 1]
        childList[j * 2] =   round(childList[j * 2], 2)
        childList[(j * 2) + 1] = round(childList[(j * 2) + 1], 2)

    return childChromosome(childList, score)
#Take the first 2 genes from the first parent chromosome and the last 3 genes from the second parent chromosome to form a child chromosome. 
def kPoint(selectionList):
    childList = []
    score = 0.0
    parent1 = random.randint(0, len(selectionList) - 1)
    parent2 = random.randint(0, len(selectionList) - 1)
    childChromosome = collections.namedtuple('scoredChromosome', 'chromosome score')
    for i in range(5):
        if i < 2:
            childList.append(selectionList[parent1][0][i])
        elif i <= 4:
            childList.append(selectionList[parent2][0][i])
    score = selectionList[parent1][1]
    return childChromosome(childList, score)

###################          MUTATION                #############################
#Once the new chromosomes have been created, you should iterate over each gene in each one of them and with a Z% probability, trigger a mutation
def mutation(mutationProbability, newGeneration):
    lengthNewGenList = len(newGeneration)
    for i in range(lengthNewGenList):
        for j in range(5):
            chance = percentChance(mutationProbability)
            if j < 4:
                if chance == 0:
                    continue
                else:
                    #mutation occured, create new rand gene
                    randNumber = randNumpyNumber()
                    newGeneration[i][0][j] = round(randNumber, 2)
            else:
                if chance == 0:
                    continue
                else:
                    newGeneration[i][0][4] = percentChance(50)
        #reorganize list
        for j in range(2):
            if newGeneration[i][0][j * 2] > newGeneration[i][0][(j * 2) + 1]:
                newGeneration[i][0][j * 2] = newGeneration[i][0][j * 2] + newGeneration[i][0][(j*2) + 1]
                newGeneration[i][0][(j * 2) + 1] = newGeneration[i][0][j * 2] - newGeneration[i][0][(j * 2) + 1]
                newGeneration[i][0][j * 2] = newGeneration[i][0][j * 2] - newGeneration[i][0][(j * 2) + 1]
            newGeneration[i][0][j * 2] = round(newGeneration[i][0][j * 2] , 2)
            newGeneration[i][0][(j * 2) + 1] = round(newGeneration[i][0][(j * 2) + 1] , 2)
    print("############################################     MUTATION OUTPUT     #######################################################")
    printList(newGeneration)
    return newGeneration
###################          INITIALIZATION                #############################
def userInterface():    
    print("Hello! Welcome to the chromosome fitness testing lab!\n")
    while True:
        try:
            print("Select file: ")
            file = input()
            f = file
            f = open(file)
            f.close()
            break
        except FileNotFoundError:
            print('File does not exist')
    
    while True:
        print("\nNumber of generations: ")
        numGerations = input()
        if (numGerations.isdigit()):
            numGerations = int(numGerations)
            if numGerations < 1:
                print("Must be at least 1 gen.\n")
            else:
                break
        else:
            print("Not an integer! Try again \n")    

    while True:
        print("\nNumber of chromosome per generation: ")
        populationSize = input()
        if (populationSize.isdigit()):
            populationSize = int(populationSize)
            if(populationSize < 4):
                print("Must have at least 4 chromosomes per generation.\n")
            else:
                break
        else:
            print("Not an integer! Try again \n")

    while True:
        print("\nPercent of population to use selection on as integer (ex: 40% = 40), remainder will be created using crossover: ")
        percentSelection = input()
        if (percentSelection.isdigit()):
            percentSelection = int(percentSelection)
            if percentSelection > 100 or percentSelection < 0:
                print("Percent chose cannot be greater than 100% or less than 0%. \n")
            else:
                populationUsingSelection, populationUsingCrossover = generatePopulations(populationSize, percentSelection)
                break
        else:
            print("Not an integer! Try again \n")

    while True:
        print("\nElitist: 0 \nTournament: 1")
        selectionAlgo = input()
        if (selectionAlgo.isdigit()):
            selectionAlgo = int(selectionAlgo)
            if selectionAlgo != 0 and selectionAlgo != 1:
                print("Select 0 or 1. Try again \n")
            else:
                break
        else:
            print("Not an integer! Try again \n")
    
    while True:
        print("\nUniform: 0 \nK-Point: 1")
        crossOverAlgo = input()
        if (crossOverAlgo.isdigit()):
            crossOverAlgo = int(crossOverAlgo)
            if crossOverAlgo != 0 and crossOverAlgo != 1:
                print("Select 0 or 1. Try again \n")
            else:
                break
        else:
            print("Not an integer! Try again \n")

    while True:
        print("\nProbability percent to cause mutation as integer (ex: 40% = 40): \n")
        mutationProbability = input()
        if (mutationProbability.isdigit()):
            mutationProbability = int(mutationProbability)
            if mutationProbability > 100 or mutationProbability < 0:
                print("Percent chose cannot be greater than 100% or less than 0%. \n")
            else:
                break
        else:
            print("Not an integer! Try again \n")

    while True:
        print("\nPercent of mutation rate change(ex: 40% mutation rate and -10% rate change = 30% for next gen): \n")
        mutationRateChange = input()
        try:
            mutationRateChange = int(mutationRateChange)
            if mutationRateChange > 100:
                print("Percent chose cannot be greater than 100%.\n")
            else:
                break
        except:
            print("Not an integer, try again.")

    newGeneration = []
    totalPopulation = []
    start = time.time()
    for i in range(numGerations):
        newGeneration = fitnesScore(file, populationSize, populationUsingSelection, populationUsingCrossover, selectionAlgo, crossOverAlgo)
        newGeneration = mutation(mutationProbability, newGeneration)
        if (mutationProbability + mutationRateChange) <= 0:
            pass
        else:
            mutationProbability += mutationRateChange
        print("############################################     EVERY GENERATION OUTPUT     #######################################################")
        print("Generation: ", i, " COMPLETE \nMutation Rate: ", mutationProbability)
        totalPopulation.extend(newGeneration)
        checkEvery10Gens = (i+1) / 10
        if checkEvery10Gens % 1 == 0:
            #uncomment to see every chromosome in the current gen after all the steps
            #for j in totalPopulation:
             #   print(j.chromosome , j.score)
            min, max, average = findMinOrMax(len(totalPopulation), 2, totalPopulation)
            print("####################      10 ITERATIONS CHECK      ##############################")
            print("Group: ", (i+1) / 10) #group per 10 iterations ie: 20th iteration is group 2
            print("Min Value: ", totalPopulation[min][1])
            print("Max Value: ", totalPopulation[max][1])
            print("Average Fitness Score: ", average)
            print("############################################################################")
    end = time.time()
    print("Completion Time In Seconds: ", round(end-start, 3))
    max = findMinOrMax(len(newGeneration), 1, newGeneration)
    print("Fittest Chromosome from last population: ", newGeneration[max])
#creates chromsome gen 0
def initializeChromosome():
    #left values must be smaller than right on their respective day: [currentDay1, currentDay2, nextDay, nextDay2, stockReccomendation]
    chromosome=[]
    recommendationValue = -1 #1 = BUY, 0 = SHORT

    for i in range(3):         
        randNumber = randNumpyNumber()
        randNumber = round(randNumber,2)
        
        randNumber2 = randNumpyNumber()
        randNumber2 = round(randNumber2,2)

        if i < 1:
            if randNumber < randNumber2:
                chromosome.append(randNumber)
                chromosome.append(randNumber2)
            else:
                chromosome.append(randNumber2)
                chromosome.append(randNumber)
        elif i < 2:
            if randNumber <= randNumber2:
                chromosome.append(randNumber)
                chromosome.append(randNumber2)
            else:
                chromosome.append(randNumber2)
                chromosome.append(randNumber)    
        else:
            recommendationValue = percentChance(50)
            chromosome.append(recommendationValue)

    return chromosome
#check chromosome to see if its valid
def validateStockData(noMatch, score, stockList = [], chromosome = []):
    counter = 0
    flag = False
    stockIndex = 0
    
    #iterate through chromosome, except last value
    for chromoIndex in range(2):
        #all values of the list except for the last one, need to satisfy the range
        if chromosome[chromoIndex*2] <= stockList[stockIndex] <= chromosome[((chromoIndex*2) + 1)]:
            #if counter= 1 then the first value of the stock data satisfy chromo curr day
            if counter == 1:
                #data is within range so we check if buy or short
                if chromosome[-1] == 1:
                    score += stockList[-1]
                    break
                else:
                    #if you sell stock, then you lost money if the last value was positive in 
                    #the stockData list since you sold at a lower cost
                    #if you profit when you buy, you lose when you sell
                    score += (stockList[-1] * -1)
                    break
            else:
                stockIndex = 1
                counter += 1
                continue
        #if any value is not within that range skip this list
        else:
            noMatch +=1
            flag = True
            return noMatch, score, flag
    return noMatch, score, flag
#compute fitness score
def fitnesScore(file, populationSize, populationUsingSelection, populationUsingCrossover, selectionAlgo, crossOverAlgo):
    scoredChromosome = collections.namedtuple('scoredChromosome', 'chromosome score')
    scoredChromosomeList = []
    #this loop creates n number of chromosomes based on number of chromsomes per generation
    for chromosomeNumber in range(populationSize):
        tempScore = 0.0
        score = 0.0
        tempNoMatch = 0
        noMatch = 0
        counter = 0  

        #create chromosome
        chromosome =  initializeChromosome()   

        #open file
        with open(file, "r") as f:
            for line in f:
                # Now you have one line of text in the variable "line" and can
                # Convert strings to floats   
                stockList = [ float(x) for x in line.split() ] 
                #iterate through single list
                tempNoMatch, tempScore, flag = validateStockData(tempNoMatch, tempScore, stockList, chromosome)
                #make sure we dont add values that did not match conditions
                if flag != True:
                    score += tempScore
                tempScore = 0.0
                noMatch += tempNoMatch
                tempNoMatch = 0
                counter += 1
            
        if noMatch == counter:
            #no stocks in our data matched the total # of stocks we had, set default
            score = -5000 
        score = round(score, 3)
        #print("       ####     FITNESS SCORE    ####\n                  ", score)
        #package chromosomes into list of tuples
        scoredChromosomeList.append(scoredChromosome(chromosome, score))
    #this output shows the chromsome before selection, cross over and mutation which lets you verify that that fitness function works based on your data
    print("############################################     FITNESS SCORES COMPUTED      #######################################################")
    for i in scoredChromosomeList:
        print("CHROMSOME BEFORE ANY CHANGES: ", i)
    #pass current generation and percent to be chosen
    scoredChromosomeList = selection(populationUsingSelection, populationUsingCrossover, populationSize, scoredChromosomeList, selectionAlgo, crossOverAlgo)
    return scoredChromosomeList

###################          HELPER FUNCTIONS                #############################
#determine what number of chromosomes for selection and crossover
def generatePopulations(populationSize, percentSelection):
    # we need at LEAST 2 chromosomes for selection and 1 for crossover
    percentSelection = percentSelection/100
    populationUsingSelection = math.ceil(populationSize * percentSelection)
    populationUsingCrossover = populationSize - populationUsingSelection
    return populationUsingSelection, populationUsingCrossover
#probability funct based on value out of 100
def percentChance(probabilityValue):
    chance = random.randint(0, 100)

    if chance <= probabilityValue:
        return 0
    elif chance >= probabilityValue + 1:
        return 1
#generates chromosome stock gene
def randNumpyNumber():
    mean = 0
    standardDeviation = 1.15
    np.random.seed

    randNumber = np.random.normal(mean, standardDeviation)
    return randNumber
#finds max, min and avg values in given list
def findMinOrMax(stopValue, minOrMax=0, listBeingChecked=[]):
    smallValueToCompare = listBeingChecked[0][1]
    largeValueToCompare = listBeingChecked[0][1]
    minIndex = 0
    maxIndex = 0
    average = listBeingChecked[0][1]

    for x in range(1, stopValue):
        #find smallest value in new list
        if listBeingChecked[x][1] < smallValueToCompare:
            smallValueToCompare = listBeingChecked[x][1]
            minIndex = x
        #find largest value in new list
        if listBeingChecked[x][1] > largeValueToCompare:
            largeValueToCompare = listBeingChecked[x][1]
            maxIndex = x    
        average += listBeingChecked[x][1]
    average = round(average / len(listBeingChecked), 2)
    if minOrMax == 0:
        return minIndex
    elif minOrMax == 1:
        return maxIndex
    elif minOrMax == 2:
        return minIndex, maxIndex, average
def printList(listToPrint):
    for i in listToPrint:
        print(i)
###################          MAIN                #############################
if __name__ == '__main__':
    userInterface()

    
    
