TO RUN
1. File was run using Python 3.7.3 64 bit
2. Run using the cmd prompt: stockPredictor.py
3. Follow prompts, be wary of some fields:
    a. Number of generations must be at least 1
    b. Chromosome number must be 4 or higher
    c. Percent of population to use selection on as integer cannot be greater than 90% or less than 10%.
    d. Mutation probability cannot be greater than 100% or less than 0%. 
    e. Mutation rate cannot be greater than 100%.
    there are various error checks as well ex: cannot enter letter for integer inputs

OUTPUT
1. After each 10 generations program displays the max, min and average fitness of the chromosomes in the population, IF the number of generations to run is > 10.
2. Fittest chromosome for last generation.

DEBUG
**Can accurately compute the fitness of a single chromosome**
1. Debug file is GA_debug.txt
2. User Inputs:
    a. For number of generations choose 1.
    b. Choose 4 chromsomes per generation. 
    c. The rest of the inputs don't matter since we are only going to look at the chromosome BEFORE any changes to make sure the fitness score is right. But for default choose:
        66 percent of population to use selection on as integer 
        0 for Elitist and Uniform
        20 for Probability percent to cause mutation as integer
        0 for mutation change rate
2. Outcome is based on BUY/SHORT or if the chromosome is not compatible
    a. Chromosome is compatible FOR BOTH training data and chromosome says buy (1), score: 3
    b. Chromosome is compatible FOR BOTH training data and chromosome says short (0), score: -3
    c. Chromosome is not compatible, output: -5000
    d. Only the first line of data is compatible and chromosome says buy (1): -5
        same idea if only the second line is compatible: 8
    e. Only the second line of data is compatible and chromosome says short (0): 5
        same idea if only the second line is compatible: -8

**Has own debug file(s) that allow for verifying that selection works correctly, crossover works correctly, mutation works correctly and that system converges to an optimal answer. README file should explain how debug file verifies correctness.**
1. Debug file is GA_debug.txt
2. User Inputs:
    a. For number of generations choose 1.
    b. Choose 4 chromsomes per generation. 
    c. Default inputs choose:
        33 percent of population to use selection on as integer 
        0 for Elitist and Uniform
        20 for Probability percent to cause mutation as integer
        1 for mutation change rate
3. The program outputs all the chromosomes in the generation being run after each calculation: 
    FITNESS
    SELECTION: (EITHER ELITIST OR TOURNAMENT DEPENDING ON CHOICE)
    CROSSOVER: (EITHER UNIFORM OR K-POINT DEPENDING ON CHOICE)
    MUTATION
    When that generation finishes and current mutation rate for that generation
    10 GENERATION ITERATIONS (only if its every 10)
4. Based on the outputs for each of the above compare the changes in chromosomes after each calculation. The changes reflect that calculations output.
    EXAMPLE: After FITNESS computed, if you selected ELITIST selection you should notice that only the top 2 of our original 4 chromosomes are displayed.
    
