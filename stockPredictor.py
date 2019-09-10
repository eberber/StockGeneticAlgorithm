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
    for i in chromosome:
        print(i)
    return chromosome

def fitnesScore(fileList = [], chromosome=[]):
    score = 0.0
    length = len(chromosome)
    noMatch = 0
    flag = False
    scoreFlag = False

    print("chromosome: ", chromosome)
    #iterate through single list of lists
    for i in fileList:
         #iterate through that single lists values
        flag= False
        scoreFlag = False
        counter = 0
        for x in i:
            #iterate through chromosome
            for y in range(length):
                #we only want to check two values of chromo against the stock value at a time
                if counter == 2:
                    break
                else:
                    #make sure to stay in bounds
                    if (y*2) + 1 <= length -1:
                        #all values of the list except for the last one, need to satisfy the range
                        if chromosome[y*2] <= x <= chromosome[((y*2) + 1)]:
                            if counter == 1:
                                #data is within range so we check if buy or short
                                if chromosome[-1] == 1:
                                    score += i[-1]
                                    scoreFlag = True
                                    break
                                else:
                                    #if you sell stock, then you lost money if the last value was positive in 
                                    #the stockData list since you sold at a lower cost
                                    #if you profit when you buy, you lose when you sell
                                    score += (i[-1] * -1)
                                    scoreFlag = True
                                    break
                            else:
                                break
                        #if any value is not within that range skip this list
                        else:
                            noMatch +=1
                            flag = True
                            break
                    else:
                        break
            counter += 1
            #TODO: fix logic for below if
            if flag != True or scoreFlag != True:
                continue
            else:
                break
        if scoreFlag != True:
            continue
        else:
            break
    if noMatch == len(fileList):
        #no stocks in our data matched our range for chromo, set default
        score = -5000 
    print("score: ", score)
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
    
    