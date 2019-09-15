import numpy as np
import random
import time
import collections
import math
###################          GLOBALVARIABLES                #############################


###################          FUNCTIONS                #############################
###################          SELECTION                #############################

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

def findMin(populationUsingSelection, elitistList = []):
    minValue = elitistList[0][1]
    minIndex = 0
    for x in range(1, populationUsingSelection):
        #find smallest value in new list
        if elitistList[x][1] < minValue:
            minValue = elitistList[x][1]
            minIndex = x
    return minIndex, minValue

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
        if scoredChromosomeList[y][1] > minValue:
            #swap the new smallest value
            elitistList[minIndex] = scoredChromosomeList[y]
            if y < lengthScoreChromoList:
                minIndex, minValue = findMin(populationUsingSelection, elitistList)
    return elitistList

###################          CROSSOVER                #############################
def selection(populationUsingSelection, populationUsingCrossover, populationSize, scoredChromosomeList, selectionAlgo, crossOverAlgo):
    selectionList = []
    chromosome = collections.namedtuple('scoredChromosome', 'chromosome score')

    if selectionAlgo == 0:
        print("Starting Elitist \n")
        selectionList = selectionSort(populationUsingSelection, scoredChromosomeList)
    elif selectionAlgo == 1:
        print("Starting Tournament \n")
        selectionList = tournamentSort(populationUsingSelection, scoredChromosomeList)

    if crossOverAlgo == 0:
        print("Starting Uniform \n")
        for x in range(populationUsingCrossover):
            chromosome = uniform(selectionList)
            selectionList.append(chromosome)
    elif crossOverAlgo == 1:
        print("Starting K-Point \n")
        for x in range(populationUsingCrossover):
            crossOverAlgo = kPoint(selectionList)
            selectionList.append(crossOverAlgo)
    return selectionList

#Iterate over each of the 5 genes and randomly select whether to use the value from the first parent chromosome or the second parent chromosome. 
def uniform(selectionList):
    childChromosome = collections.namedtuple('scoredChromosome', 'chromosome score')
    childList = []
    chance = -1
    score = 0.0
    parent1 = random.randint(0, len(selectionList) - 1)
    parent2 = random.randint(0, len(selectionList) - 1)

    for i in range(5):
        chance = fiftyPercentChance()
        if i != 4:
            if chance == 0:
                childList.append(selectionList[parent1][0][i])
            elif chance == 1:
                childList.append(selectionList[parent2][0][i])
        else:
            if chance == 0:
                score = round(selectionList[parent1][1], 2)
            elif chance == 1:
                score = round(selectionList[parent2][1], 2)
    #organize list    
    for j in range(2):
        if childList[j * 2] > childList[(j * 2) + 1]:
            childList[j * 2] = childList[j * 2] + childList[(j*2) + 1]
            childList[(j * 2) + 1] = childList[j * 2] - childList[(j * 2) + 1]
            childList[j * 2] = childList[j * 2] - childList[(j * 2) + 1]

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
        elif i < 4:
            childList.append(selectionList[parent2][0][i])
        else:
            score = childList.append(selectionList[parent2][1])
    return childChromosome(childList, score)

###################          MUTATION                #############################
#def mutation():

###################          INITIALIZATION                #############################
def userInterface():    
    print("Hello! Welcome to the chromosome fitness testing lab!\n")
    ''' try:
        print("Select a file containing the training data: ")
        file = input()
    except:
        print("Error opening,", file ,",try again \n") '''
    
    while True:
        print("Number of chromosome per generation: ")
        populationSize = input()
        if (populationSize.isdigit()):
            populationSize = int(populationSize)
            break
        else:
            print("Not an integer! Try again \n")

    while True:
        print("Percent of population to use selection on as integer (ex: 40% = 40), remainder will be created using crossover: \n")
        percentSelection = input()
        if (percentSelection.isdigit()):
            percentSelection = int(percentSelection)
            if percentSelection > 100:
                print("Percent chose cannot be greater than 100%. \n")
            else:
                populationUsingSelection, populationUsingCrossover = generatePopulations(populationSize, percentSelection)
                break
        else:
            print("Not an integer! Try again \n")

    while True:
        print("Elitist: 0 \nTournament: 1")
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
        print("Uniform: 0 \n K-Point: 1")
        crossOverAlgo = input()
        if (crossOverAlgo.isdigit()):
            crossOverAlgo = int(crossOverAlgo)
            if crossOverAlgo != 0 and crossOverAlgo != 1:
                print("Select 0 or 1. Try again \n")
            else:
                break
        else:
            print("Not an integer! Try again \n")
    #TODO: Dont hard code
    file = "genAlgData1.txt"
    #file = "GA_debug.txt"
    #print(file)
    start = time.time()
    fitnesScore(file, populationSize, populationUsingSelection, populationUsingCrossover, selectionAlgo, crossOverAlgo)
    end = time.time()
    print("Completion Time In Seconds: ", round(end-start, 3))

def generatePopulations(populationSize, percentSelection):
    percentSelection = percentSelection/100
    populationUsingSelection = math.floor(populationSize * percentSelection)
    populationUsingCrossover = populationSize - populationUsingSelection
    return populationUsingSelection, populationUsingCrossover

def fiftyPercentChance():
    chance = random.randint(1, 100)

    if chance <= 50:
        return 0
    elif chance >= 51:
        return 1

def randNumpyNumber():
    mean = 0
    standardDeviation = 1.15
    np.random.seed

    randNumber = np.random.normal(mean, standardDeviation)
    return randNumber

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
            recommendationValue = fiftyPercentChance()
            chromosome.append(recommendationValue)

    return chromosome

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

def fitnesScore(file, populationSize, populationUsingSelection, populationUsingCrossover, selectionAlgo, crossOverAlgo):
    scoredChromosome = collections.namedtuple('scoredChromosome', 'chromosome score')
    scoredChromosomeList = []

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
                #iterate through single list of lists
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
    #pass current generation and percent to be chosen
    scoredChromosomeList = selection(populationUsingSelection, populationUsingCrossover, populationSize, scoredChromosomeList, selectionAlgo, crossOverAlgo)

###################          MAIN                #############################
if __name__ == '__main__':
    userInterface()

    
    