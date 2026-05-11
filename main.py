from bot import Bot
import random
from simulation import run_simulation

# ======================================================
# INITIAL POPULATION
# ======================================================

bots = [
    Bot(10, 1000, 3, 97),
    Bot(10, 1000, 7, 100),
    Bot(10, 1000, 9, 103),
    Bot(10, 1000, 9, 95),
    Bot(10, 1000, 5, 101),
    Bot(10, 1000, 4, 99),
]

# ======================================================
# EXECUTION (The missing part!)
# ======================================================

if __name__ == "__main__":
    # Define how long and how many times the simulation runs
    STEPS_PER_GEN = 100
    TOTAL_GENERATIONS = 5
    
    # Run the simulation logic from simulation.py
    run_simulation(bots, STEPS_PER_GEN, TOTAL_GENERATIONS)