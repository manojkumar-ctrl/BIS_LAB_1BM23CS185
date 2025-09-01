import java.util.*;

public class TSP_GA {
    static final int NUM_CITIES = 10;
    static final int POP_SIZE = 100;
    static final int GENERATIONS = 50;  // Change to 50 generations as requested
    static final double MUTATION_RATE = 0.015;

    static double[][] distanceMatrix = new double[NUM_CITIES][NUM_CITIES];

    static class Tour {
        List<Integer> cities = new ArrayList<>();
        double fitness = 0;

        Tour() {
            for (int i = 0; i < NUM_CITIES; i++) {
                cities.add(i);
            }
            Collections.shuffle(cities);
        }

        Tour(List<Integer> cities) {
            this.cities = new ArrayList<>(cities);
        }

        double getDistance() {
            double dist = 0;
            for (int i = 0; i < cities.size() - 1; i++) {
                dist += distanceMatrix[cities.get(i)][cities.get(i + 1)];
            }
            dist += distanceMatrix[cities.get(cities.size() - 1)][cities.get(0)];
            return dist;   // <-- fixed: return statement added
        }

        void calculateFitness() {
            fitness = 1 / getDistance();
        }

        @Override
        public String toString() {
            return cities.toString() + " Distance: " + String.format("%.2f", getDistance());
        }
    }

    public static void main(String[] args) {

        Random rand = new Random();

        // Generate random distances
        for (int i = 0; i < NUM_CITIES; i++) {
            for (int j = 0; j < NUM_CITIES; j++) {
                if (i == j) distanceMatrix[i][j] = 0;
                else distanceMatrix[i][j] = 10 + rand.nextInt(90);
            }
        }

        // Initial population
        List<Tour> population = new ArrayList<>();
        for (int i = 0; i < POP_SIZE; i++) {
            Tour t = new Tour();
            t.calculateFitness();
            population.add(t);
        }

        Tour bestTourEver = null;

        for (int gen = 0; gen < GENERATIONS; gen++) {
            population.sort(Comparator.comparingDouble(t -> -t.fitness));
            if (bestTourEver == null || population.get(0).fitness > bestTourEver.fitness) {
                bestTourEver = population.get(0);
            }

            System.out.println("Generation " + gen + " Best: " + population.get(0));

            List<Tour> newPopulation = new ArrayList<>(population.subList(0, POP_SIZE / 2)); // elitism

            while (newPopulation.size() < POP_SIZE) {
                Tour parent1 = select(population);
                Tour parent2 = select(population);
                Tour child = crossover(parent1, parent2);
                mutate(child);
                child.calculateFitness();
                newPopulation.add(child);
            }

            population = newPopulation;
        }

        System.out.println("\n=== Best Tour Found ===");
        System.out.println(bestTourEver);
    }

    static Tour select(List<Tour> population) {
        Random rand = new Random();
        return population.get(rand.nextInt(POP_SIZE / 2));
    }

    static Tour crossover(Tour parent1, Tour parent2) {
        Random rand = new Random();
        int start = rand.nextInt(NUM_CITIES);
        int end = rand.nextInt(NUM_CITIES - start) + start;

        List<Integer> childCities = new ArrayList<>(Collections.nCopies(NUM_CITIES, -1));
        for (int i = start; i < end; i++) {
            childCities.set(i, parent1.cities.get(i));
        }

        int idx = 0;
        for (int i = 0; i < NUM_CITIES; i++) {
            int city = parent2.cities.get(i);
            if (!childCities.contains(city)) {
                while (childCities.get(idx) != -1) idx++;
                childCities.set(idx, city);
            }
        }
        return new Tour(childCities);
    }

    static void mutate(Tour t) {
        Random rand = new Random();
        for (int i = 0; i < NUM_CITIES; i++) {
            if (rand.nextDouble() < MUTATION_RATE) {
                int j = rand.nextInt(NUM_CITIES);
                Collections.swap(t.cities, i, j);
            }
        }
    }
}
