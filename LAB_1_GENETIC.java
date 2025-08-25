import java.util.*;

public class genetic{

    static int POPULATION_SIZE = 6;
    static int CHROMOSOME_LENGTH = 5; // For x in [0, 31]
    static int MAX_GENERATIONS = 4;
    static double CROSSOVER_RATE = 0.7;
    static double MUTATION_RATE = 0.01;

    // Generate a random integer and convert it to binary string
    static String randomChromosome() {
        Random rand = new Random();
        int randomInt = rand.nextInt(32); // Random integer in the range [0, 31]
        return String.format("%5s", Integer.toBinaryString(randomInt)).replace(' ', '0');
    }

    // Convert binary string to integer
    static int binaryToInt(String binary) {
        return Integer.parseInt(binary, 2);
    }

    // Fitness function: f(x) = x^2
    static int fitness(String chromosome) {
        int x = binaryToInt(chromosome);
        return x * x;
    }

    // Roulette Wheel Selection based on fitness
    static String selectParent(List<String> population) {
        Random rand = new Random();
        int totalFitness = 0;
        for (String individual : population) {
            totalFitness += fitness(individual);
        }

        // Compute the cumulative probability
        int randomValue = rand.nextInt(totalFitness);

        int cumulativeFitness = 0;
        for (String individual : population) {
            cumulativeFitness += fitness(individual);
            if (cumulativeFitness >= randomValue) {
                return individual;
            }
        }
        return population.get(0); // Default return (should not happen)
    }

    // Crossover: single point
    static String crossover(String parent1, String parent2) {
        Random rand = new Random();
        if (rand.nextDouble() > CROSSOVER_RATE) {
            return parent1; // No crossover
        }
        int point = rand.nextInt(CHROMOSOME_LENGTH);
        return parent1.substring(0, point) + parent2.substring(point);
    }

    // Mutation: flip a random bit
    static String mutate(String chromosome) {
        Random rand = new Random();
        StringBuilder sb = new StringBuilder(chromosome);
        for (int i = 0; i < CHROMOSOME_LENGTH; i++) {
            if (rand.nextDouble() < MUTATION_RATE) {
                sb.setCharAt(i, sb.charAt(i) == '0' ? '1' : '0');
            }
        }
        return sb.toString();
    }

    public static void main(String[] args) {
        List<String> population = new ArrayList<>();

        // Step 1: Initialize population
        for (int i = 0; i < POPULATION_SIZE; i++) {
            population.add(randomChromosome());
        }

        // Step 2-7: Run for 4 generations
        for (int gen = 0; gen < MAX_GENERATIONS; gen++) {
            List<String> newPopulation = new ArrayList<>();
            int bestFitness = Integer.MIN_VALUE;
            String best = "";

            System.out.println("Generation " + (gen + 1));

            // Evaluate and print the fitness of each individual and its probability of selection
            int totalFitness = 0;
            List<Double> expectedProbabilities = new ArrayList<>();
            for (String individual : population) {
                int fit = fitness(individual);
                totalFitness += fit;
                System.out.println("Chromosome: " + individual + " -> x = " + binaryToInt(individual) + ", f(x) = " + fit);
            }

            // Calculate expected probability (fitness / totalFitness)
            System.out.println("Expected fitness probabilities for selection:");
            for (String individual : population) {
                int fit = fitness(individual);
                double expectedProb = (double) fit / totalFitness;
                expectedProbabilities.add(expectedProb);
                System.out.println("Chromosome: " + individual + " -> Expected selection probability: " + expectedProb);
            }

            // Calculate sum, average, and maximum of expected probabilities
            double sum = expectedProbabilities.stream().mapToDouble(Double::doubleValue).sum();
            double avg = sum / expectedProbabilities.size();
            double max = Collections.max(expectedProbabilities);

            System.out.println("Sum of Expected Probabilities: " + sum);
            System.out.println("Average Expected Probability: " + avg);
            System.out.println("Maximum Expected Probability: " + max);

            // Print best solution this generation
            for (String individual : population) {
                int fit = fitness(individual);
                if (fit > bestFitness) {
                    bestFitness = fit;
                    best = individual;
                }
            }

            int bestX = binaryToInt(best);
            System.out.println("Best solution this generation: x = " + bestX + ", f(x) = " + bestFitness);
            System.out.println();

            // Create new population
            while (newPopulation.size() < POPULATION_SIZE) {
                String parent1 = selectParent(population);
                String parent2 = selectParent(population);

                String child = crossover(parent1, parent2);
                child = mutate(child);

                newPopulation.add(child);
            }

            population = newPopulation;
        }

        // Final best solution
        String bestSolution = population.get(0);
        int finalBestX = binaryToInt(bestSolution);
        System.out.println("Final best solution after " + MAX_GENERATIONS + " generations: x = " + finalBestX + ", f(x) = " + fitness(bestSolution));
    }
}
