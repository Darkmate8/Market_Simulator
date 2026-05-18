from bot import Bot
import yaml
from simulation import run_simulation
from stats_tracker import StatsTracker


with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)
    

# ======================================================
# INITIAL POPULATION
# ======================================================

bots = [
    Bot(
        inventory= config["start_inventory"],
        money= config["start_money"],
        aggressiveness= b["aggressiveness"],
        reference_price= b["reference_price"]
    )
    for b in config["bots"]
]

# ======================================================
# EXECUTION
# ======================================================

if __name__ == "__main__":

    stats = StatsTracker()
    run_simulation(bots, config, stats)

    # ======================================================
    # SUMMARY STATS AFTER SIMULATION
    # ======================================================

    print()
    print("===================================================")
    print("SIMULATION COMPLETE - STATS SUMMARY")
    print("===================================================")
    print()
    print(f"Total Trades: {stats.total_trades()}")
    print(f"Average Price (All Steps): {stats.average_price():.2f}")
