import numpy as np

# Power System Data 
generators = [
    {"a": 0.007,  "b": 7.0,  "c": 240, "Pmin": 100, "Pmax": 500},
    {"a": 0.0095, "b": 10.0, "c": 200, "Pmin": 50,  "Pmax": 200},
    {"a": 0.009,  "b": 8.5,  "c": 220, "Pmin": 80,  "Pmax": 300},
    {"a": 0.008,  "b": 11.0, "c": 200, "Pmin": 50,  "Pmax": 150},
]

# Power demand (MW)
Power_Demand = 700  

def generation_cost(P):
  
    total_cost = 0
    total_power = np.sum(P)
    penalty_factor = 1000  
    
    for i, gen in enumerate(generators):
        total_cost += gen["a"] * P[i]**2 + gen["b"] * P[i] + gen["c"]

 
    penalty = penalty_factor * abs(total_power - Power_Demand)
    
    return total_cost + penalty

#  GWO Algorithm 
def grey_wolf_optimization(num_agents=30, max_iterations=100):
  
    num_generators = len(generators)
    
    Pmin = np.array([g["Pmin"] for g in generators])
    Pmax = np.array([g["Pmax"] for g in generators])

    population = np.random.uniform(Pmin, Pmax, (num_agents, num_generators))

    best_power, second_best_power, third_best_power = np.zeros(num_generators), np.zeros(num_generators), np.zeros(num_generators)
    best_cost, second_best_cost, third_best_cost = np.inf, np.inf, np.inf

    #   Main Optimization Loop 
    for iteration in range(max_iterations):
        for i in range(num_agents):
            cost = generation_cost(population[i])

         
            if cost < best_cost:
                third_best_cost, second_best_cost, best_cost = second_best_cost, best_cost, cost
                third_best_power, second_best_power, best_power = second_best_power.copy(), best_power.copy(), population[i].copy()
            elif cost < second_best_cost:
                third_best_cost, second_best_cost = second_best_cost, cost
                third_best_power, second_best_power = second_best_power.copy(), population[i].copy()
            elif cost < third_best_cost:
                third_best_cost = cost
                third_best_power = population[i].copy()


        a = 2 - 2 * (iteration / max_iterations)  

        for i in range(num_agents):
            for j in range(num_generators):
                r1, r2 = np.random.rand(), np.random.rand()
                A1, C1 = 2 * a * r1 - a, 2 * r2
                D1 = abs(C1 * best_power[j] - population[i][j])
                X1 = best_power[j] - A1 * D1

                r1, r2 = np.random.rand(), np.random.rand()
                A2, C2 = 2 * a * r1 - a, 2 * r2
                D2 = abs(C2 * second_best_power[j] - population[i][j])
                X2 = second_best_power[j] - A2 * D2

                r1, r2 = np.random.rand(), np.random.rand()
                A3, C3 = 2 * a * r1 - a, 2 * r2
                D3 = abs(C3 * third_best_power[j] - population[i][j])
                X3 = third_best_power[j] - A3 * D3

                population[i][j] = (X1 + X2 + X3) / 3

            population[i] = np.clip(population[i], Pmin, Pmax)

        print(f"Iteration {iteration+1:3d}: Best Total Generation Cost = {best_cost:.4f}")

    return best_power, best_cost


optimal_generation, minimum_cost = grey_wolf_optimization(num_agents=40, max_iterations=200)

# results
print("\n")
for i, P in enumerate(optimal_generation, start=1):
    print(f"Generator {i}: {P:.3f} MW")
print(f"Total Power Generated = {np.sum(optimal_generation):.3f} MW")
print(f"Total Generation Cost = ${minimum_cost:.3f}")
print("")






//Output 

PS C:\Users\STUDENT\Desktop\LAB CIE_BIS> python grey.py
Iteration   1: Best Total Generation Cost = $23797.4238
Iteration   2: Best Total Generation Cost = $10667.3250
Iteration   3: Best Total Generation Cost = $9792.2194
Iteration   4: Best Total Generation Cost = $9792.2194
Iteration   5: Best Total Generation Cost = $9522.1855
Iteration   6: Best Total Generation Cost = $9522.1855
Iteration   7: Best Total Generation Cost = $9522.1855
Iteration   8: Best Total Generation Cost = $9522.1855
Iteration   9: Best Total Generation Cost = $8821.9025
Iteration  10: Best Total Generation Cost = $8821.9025
Iteration  11: Best Total Generation Cost = $8821.9025
Iteration  12: Best Total Generation Cost = $8675.3575
Iteration  13: Best Total Generation Cost = $8538.1408
Iteration  14: Best Total Generation Cost = $8538.1408
Iteration  15: Best Total Generation Cost = $8538.1408
Iteration  16: Best Total Generation Cost = $8155.8688
Iteration  17: Best Total Generation Cost = $8155.8688
Iteration  18: Best Total Generation Cost = $8155.8688
Iteration  19: Best Total Generation Cost = $8155.8688
Iteration  20: Best Total Generation Cost = $8155.8688
Iteration  21: Best Total Generation Cost = $8155.8688
Iteration  22: Best Total Generation Cost = $8155.8688
Iteration  23: Best Total Generation Cost = $8155.8688
Iteration  24: Best Total Generation Cost = $8155.8688
Iteration  25: Best Total Generation Cost = $8155.8688
Iteration  26: Best Total Generation Cost = $8155.8688
Iteration  27: Best Total Generation Cost = $8155.8688
Iteration  28: Best Total Generation Cost = $8155.8688
Iteration  29: Best Total Generation Cost = $8155.8688
Iteration  30: Best Total Generation Cost = $8155.8688
Iteration  31: Best Total Generation Cost = $8155.8688
Iteration  32: Best Total Generation Cost = $8155.8688
Iteration  33: Best Total Generation Cost = $8155.8688
Iteration  34: Best Total Generation Cost = $8155.8688
Iteration  35: Best Total Generation Cost = $8155.8688
Iteration  36: Best Total Generation Cost = $8155.8688
Iteration  37: Best Total Generation Cost = $8155.8688
Iteration  38: Best Total Generation Cost = $7991.8054
Iteration  39: Best Total Generation Cost = $7991.8054
Iteration  40: Best Total Generation Cost = $7991.8054
Iteration  41: Best Total Generation Cost = $7991.8054
Iteration  42: Best Total Generation Cost = $7991.8054
Iteration  43: Best Total Generation Cost = $7991.8054
Iteration  44: Best Total Generation Cost = $7991.8054
Iteration  45: Best Total Generation Cost = $7991.8054
Iteration  46: Best Total Generation Cost = $7991.8054
Iteration  47: Best Total Generation Cost = $7991.8054
Iteration  48: Best Total Generation Cost = $7991.8054
Iteration  49: Best Total Generation Cost = $7991.8054
Iteration  50: Best Total Generation Cost = $7991.8054
Iteration  51: Best Total Generation Cost = $7991.8054
Iteration  52: Best Total Generation Cost = $7991.8054
Iteration  53: Best Total Generation Cost = $7991.8054
Iteration  54: Best Total Generation Cost = $7991.8054
Iteration  55: Best Total Generation Cost = $7991.8054
Iteration  56: Best Total Generation Cost = $7991.8054
Iteration  57: Best Total Generation Cost = $7991.8054
Iteration  58: Best Total Generation Cost = $7991.8054
Iteration  59: Best Total Generation Cost = $7991.8054
Iteration  60: Best Total Generation Cost = $7991.8054
Iteration  61: Best Total Generation Cost = $7991.8054
Iteration  62: Best Total Generation Cost = $7991.8054
Iteration  63: Best Total Generation Cost = $7991.8054
Iteration  64: Best Total Generation Cost = $7991.8054
Iteration  65: Best Total Generation Cost = $7991.8054
Iteration  66: Best Total Generation Cost = $7991.8054
Iteration  67: Best Total Generation Cost = $7991.8054
Iteration  68: Best Total Generation Cost = $7991.8054
Iteration  69: Best Total Generation Cost = $7991.8054
Iteration  70: Best Total Generation Cost = $7991.8054
Iteration  71: Best Total Generation Cost = $7991.8054
Iteration  72: Best Total Generation Cost = $7991.8054
Iteration  73: Best Total Generation Cost = $7991.8054
Iteration  74: Best Total Generation Cost = $7991.8054
Iteration  75: Best Total Generation Cost = $7991.8054
Iteration  76: Best Total Generation Cost = $7991.8054
Iteration  77: Best Total Generation Cost = $7991.8054
Iteration  78: Best Total Generation Cost = $7991.8054
Iteration  79: Best Total Generation Cost = $7991.8054
Iteration  80: Best Total Generation Cost = $7991.8054
Iteration  81: Best Total Generation Cost = $7991.8054
Iteration  82: Best Total Generation Cost = $7991.8054
Iteration  83: Best Total Generation Cost = $7991.8054
Iteration  84: Best Total Generation Cost = $7991.8054
Iteration  85: Best Total Generation Cost = $7991.8054
Iteration  86: Best Total Generation Cost = $7991.8054
Iteration  87: Best Total Generation Cost = $7991.8054
Iteration  88: Best Total Generation Cost = $7991.8054
Iteration  89: Best Total Generation Cost = $7991.8054
Iteration  90: Best Total Generation Cost = $7991.8054
Iteration  91: Best Total Generation Cost = $7991.8054
Iteration  92: Best Total Generation Cost = $7991.8054
Iteration  93: Best Total Generation Cost = $7991.8054
Iteration  94: Best Total Generation Cost = $7991.8054
Iteration  95: Best Total Generation Cost = $7991.8054
Iteration  96: Best Total Generation Cost = $7991.8054
Iteration  97: Best Total Generation Cost = $7991.8054
Iteration  98: Best Total Generation Cost = $7991.8054
Iteration  99: Best Total Generation Cost = $7991.8054
Iteration 100: Best Total Generation Cost = $7991.8054
Iteration 101: Best Total Generation Cost = $7991.8054
Iteration 102: Best Total Generation Cost = $7991.8054
Iteration 103: Best Total Generation Cost = $7988.2682
Iteration 104: Best Total Generation Cost = $7988.2682
Iteration 105: Best Total Generation Cost = $7946.0113
Iteration 106: Best Total Generation Cost = $7946.0113
Iteration 107: Best Total Generation Cost = $7946.0113
Iteration 108: Best Total Generation Cost = $7946.0113
Iteration 109: Best Total Generation Cost = $7946.0113
Iteration 110: Best Total Generation Cost = $7946.0113
Iteration 111: Best Total Generation Cost = $7946.0113
Iteration 112: Best Total Generation Cost = $7946.0113
Iteration 113: Best Total Generation Cost = $7946.0113
Iteration 114: Best Total Generation Cost = $7946.0113
Iteration 115: Best Total Generation Cost = $7946.0113
Iteration 116: Best Total Generation Cost = $7946.0113
Iteration 117: Best Total Generation Cost = $7946.0113
Iteration 118: Best Total Generation Cost = $7946.0113
Iteration 119: Best Total Generation Cost = $7946.0113
Iteration 120: Best Total Generation Cost = $7946.0113
Iteration 121: Best Total Generation Cost = $7946.0113
Iteration 122: Best Total Generation Cost = $7946.0113
Iteration 123: Best Total Generation Cost = $7946.0113
Iteration 124: Best Total Generation Cost = $7946.0113
Iteration 125: Best Total Generation Cost = $7946.0113
Iteration 126: Best Total Generation Cost = $7946.0113
Iteration 127: Best Total Generation Cost = $7946.0113
Iteration 128: Best Total Generation Cost = $7946.0113
Iteration 129: Best Total Generation Cost = $7946.0113
Iteration 130: Best Total Generation Cost = $7946.0113
Iteration 131: Best Total Generation Cost = $7946.0113
Iteration 132: Best Total Generation Cost = $7946.0113
Iteration 133: Best Total Generation Cost = $7946.0113
Iteration 134: Best Total Generation Cost = $7946.0113
Iteration 135: Best Total Generation Cost = $7946.0113
Iteration 136: Best Total Generation Cost = $7946.0113
Iteration 137: Best Total Generation Cost = $7946.0113
Iteration 138: Best Total Generation Cost = $7946.0113
Iteration 139: Best Total Generation Cost = $7946.0113
Iteration 140: Best Total Generation Cost = $7946.0113
Iteration 141: Best Total Generation Cost = $7946.0113
Iteration 142: Best Total Generation Cost = $7946.0113
Iteration 143: Best Total Generation Cost = $7946.0113
Iteration 144: Best Total Generation Cost = $7946.0113
Iteration 145: Best Total Generation Cost = $7946.0113
Iteration 146: Best Total Generation Cost = $7946.0113
Iteration 147: Best Total Generation Cost = $7946.0113
Iteration 148: Best Total Generation Cost = $7946.0113
Iteration 149: Best Total Generation Cost = $7946.0113
Iteration 150: Best Total Generation Cost = $7946.0113
Iteration 151: Best Total Generation Cost = $7946.0113
Iteration 152: Best Total Generation Cost = $7946.0113
Iteration 153: Best Total Generation Cost = $7946.0113
Iteration 154: Best Total Generation Cost = $7946.0113
Iteration 155: Best Total Generation Cost = $7946.0113
Iteration 156: Best Total Generation Cost = $7946.0113
Iteration 157: Best Total Generation Cost = $7946.0113
Iteration 158: Best Total Generation Cost = $7946.0113
Iteration 159: Best Total Generation Cost = $7946.0113
Iteration 160: Best Total Generation Cost = $7946.0113
Iteration 161: Best Total Generation Cost = $7946.0113
Iteration 162: Best Total Generation Cost = $7946.0113
Iteration 163: Best Total Generation Cost = $7946.0113
Iteration 164: Best Total Generation Cost = $7946.0113
Iteration 165: Best Total Generation Cost = $7946.0113
Iteration 166: Best Total Generation Cost = $7946.0113
Iteration 167: Best Total Generation Cost = $7946.0113
Iteration 168: Best Total Generation Cost = $7946.0113
Iteration 169: Best Total Generation Cost = $7946.0113
Iteration 170: Best Total Generation Cost = $7946.0113
Iteration 171: Best Total Generation Cost = $7946.0113
Iteration 172: Best Total Generation Cost = $7946.0113
Iteration 173: Best Total Generation Cost = $7946.0113
Iteration 174: Best Total Generation Cost = $7946.0113
Iteration 175: Best Total Generation Cost = $7946.0113
Iteration 176: Best Total Generation Cost = $7946.0113
Iteration 177: Best Total Generation Cost = $7946.0113
Iteration 178: Best Total Generation Cost = $7946.0113
Iteration 179: Best Total Generation Cost = $7946.0113
Iteration 180: Best Total Generation Cost = $7946.0113
Iteration 181: Best Total Generation Cost = $7946.0113
Iteration 182: Best Total Generation Cost = $7946.0113
Iteration 183: Best Total Generation Cost = $7946.0113
Iteration 184: Best Total Generation Cost = $7946.0113
Iteration 185: Best Total Generation Cost = $7946.0113
Iteration 186: Best Total Generation Cost = $7946.0113
Iteration 187: Best Total Generation Cost = $7946.0113
Iteration 188: Best Total Generation Cost = $7946.0113
Iteration 189: Best Total Generation Cost = $7946.0113
Iteration 190: Best Total Generation Cost = $7946.0113
Iteration 191: Best Total Generation Cost = $7946.0113
Iteration 192: Best Total Generation Cost = $7946.0113
Iteration 193: Best Total Generation Cost = $7946.0113
Iteration 194: Best Total Generation Cost = $7946.0113
Iteration 195: Best Total Generation Cost = $7920.5462
Iteration 196: Best Total Generation Cost = $7920.5462
Iteration 197: Best Total Generation Cost = $7920.5462
Iteration 198: Best Total Generation Cost = $7920.5462
Iteration 199: Best Total Generation Cost = $7920.5462
Iteration 200: Best Total Generation Cost = $7920.5462


Generator 1: 315.778 MW
Generator 2: 145.431 MW
Generator 3: 187.602 MW
Generator 4: 51.191 MW
Total Power Generated = 700.001 MW
Total Generation Cost = $7920.546
