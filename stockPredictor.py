import numpy as np
import random
###################          GLOBALVARIABLES                #############################
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

    print("####    CHROMOSOME     ####\n",firstDayLeftValue)
    print(firstDayRightValue)
    print(nextDayLeftValue)
    print(nextDayRightValue)
    print(recommendationValue)

#def checkChromosome(chromosome[]):

#def fitnesScore(chromosome[]):
if __name__ == '__main__':
    initializeChromosome() 
        
    
    