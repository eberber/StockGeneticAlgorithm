import numpy as np
import random
###################          GLOBALVARIABLES                #############################


###################          FUNCTIONS                #############################
def fiftyPercentChance():
    chance = random.randint(1,100)

    if chance <= 50:
        return 0
    elif chance >= 51:
        return 1

def initializeChromosome():
    mean = 0
    standardDeviation = 1.15
    np.random.seed
    flag = False
    counter = 0
    #left values must be smaller than right on their respective day
    chromosome=[]
    firstDayLeftValue = 0
    firstDayRightValue = 0
    nextDayLeftValue = 0
    nextDayRightValue = 0
    recommendationValue = -1 #1 = BUY, 0 = SHORT

    while flag == False:         
        randNumber = np.random.normal(mean, standardDeviation)
        randNumber = round(randNumber,2)
        
        randNumber2 = np.random.normal(mean, standardDeviation)
        randNumber2 = round(randNumber2,2)

        if counter == 0:
            if randNumber < randNumber2:
                firstDayLeftValue = randNumber
                firstDayRightValue = randNumber2
            else:
                firstDayLeftValue = randNumber2
                firstDayRightValue = randNumber
        elif counter == 1:
            if randNumber <= randNumber2:
                nextDayLeftValue = randNumber
                nextDayRightValue = randNumber2
                flag = True
            else:
                nextDayLeftValue = randNumber2
                nextDayRightValue = randNumber        
                flag = True
        else:
            print("Error assigning chromosome values, exiting...")
            exit()
        counter+=1
    
    recommendationValue = fiftyPercentChance()

    print("####    CHROMOSOME     ####")
    chromosome.append(firstDayLeftValue)
    chromosome.append(firstDayRightValue)
    chromosome.append(nextDayLeftValue)
    chromosome.append(nextDayRightValue)
    chromosome.append(recommendationValue)
    print(chromosome)
    return chromosome

def validateStockData(noMatch, score, stockValue = [], chromosome = []):
    counter = 0
    flag = False
    stockIndex = 0
    
    #iterate through chromosome, except last value
    for chromoIndex in range(2):
        #all values of the list except for the last one, need to satisfy the range
        t = chromosome[((chromoIndex*2) + 1)]
        print("HERE: ", t)
        if chromosome[chromoIndex*2] <= stockValue[stockIndex] <= chromosome[((chromoIndex*2) + 1)]:
            #if counter= 1 then the first value of the stock data satisfy chromo curr day
            if counter == 1:
                #data is within range so we check if buy or short
                if chromosome[-1] == 1:
                    score += stockValue[-1]
                    break
                else:
                    #if you sell stock, then you lost money if the last value was positive in 
                    #the stockData list since you sold at a lower cost
                    #if you profit when you buy, you lose when you sell
                    score += (stockValue[-1] * -1)
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

def fitnesScore(fileList = [], chromosome=[]):
    tempScore = 0.0
    score = 0.0
    tempNoMatch = 0
    noMatch = 0

    #iterate through single list of lists
    for i in fileList:
        tempNoMatch, tempScore, flag = validateStockData(tempNoMatch, tempScore, i, chromosome)
        #make sure we dont add values that did not match conditions
        if flag != True:
            score += tempScore
        tempScore = 0.0
        noMatch += tempNoMatch
        tempNoMatch = 0
        
    if noMatch == len(fileList):
        #no stocks in our data matched our range for chromo, set default
        score = -5000 
    print("####     FITNESS SCORE    ####\n", score)
    return score

def userInterface():
    fileList = []
    stock = []

    print("Hello! Welcome to the chromosome fitness testing lab!\n")
    print("Select a file containing the training data: ")
    #TODO: Dont hard code
    file = "GA_debug.txt"
    print(file)
    #open file
    file = open(file)
    f1 = file
    for x in f1:
        tempList = x.split()
        stock = []
        for y in tempList:
            stock.append(int(y))
        fileList.append(stock)
    #created list of lists that contain our stock data per line
    chromosome =  initializeChromosome()         
    fitnesScore(fileList, chromosome)

if __name__ == '__main__':
    userInterface()
    
    