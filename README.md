TO RUN
1. File was run using Python 3.7.3 64 bit
2. Run using the cmd prompt: stockPredictor.py
3. Follow prompts

OUTPUT
1. After each 10 generations program displays the max, min and average fitness of the chromosomes in the population.
2. Fittest chromosome for last generation.

DEBUG
1. Debug file is GA_debug.txt
2. Outcome is based on BUY/SHORT or if the chromosome is not compatible
    a. Chromosome is compatible and says buy (1), output: 3
    b. Chromosome is compatible and says short (0), output: -3
    c. Chromosome is not compatible, output: -5000
