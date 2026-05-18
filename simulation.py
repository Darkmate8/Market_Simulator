import random
from bot import Bot
from stats_tracker import StatsTracker


def run_simulation(bots, config, stats=None):

    if stats is None:
        stats = StatsTracker()

    market_regime = "high liquidity"
    
    for generation in range(config["num_generations"]):

        print()
        print("===================================================")
        print(f"GENERATION {generation}")
        print("===================================================")

        price = config["starting_price"]

        price_history = []

        # ==================================================
        # SIMULATION LOOP
        # ==================================================

        for step in range(config["steps_per_generation"]):

            # --------------------------------------------------
            # Market regime switch
            # --------------------------------------------------
            regime_switch_interval = config["regime_switch_interval"]
            if step % regime_switch_interval == 0:

                if random.randint(1, 2) == 1:
                    market_regime = "high liquidity"

                else:
                    market_regime = "low liquidity"

            # --------------------------------------------------
            # Liquidity impact
            # --------------------------------------------------

            if market_regime == "high liquidity":
                impact = random.randint(config["high_liquidity_impact_min"], config["high_liquidity_impact_max"])

            else:
                impact = random.randint(config["low_liquidity_impact_min"], config["low_liquidity_impact_max"])

            buyers = []
            sellers = []

            # ==================================================
            # BOT DECISIONS
            # ==================================================

            for bot in bots:

                action = bot.decide(price)

                if action == "buy":
                    buyers.append(bot)

                elif action == "sell":
                    sellers.append(bot)

            # ==================================================
            # MATCH TRADES
            # ==================================================

            total_trades = min(len(buyers), len(sellers))

            buys_this_step = total_trades
            sells_this_step = total_trades

            for i in range(total_trades):

                buyer = buyers.pop(0)
                seller = sellers.pop(0)

                buyer.execute_trade("buy", price)
                seller.execute_trade("sell", price)

            # ==================================================
            # PRICE MOVEMENT
            # ==================================================

            net_demand = len(buyers) - len(sellers)

            price += net_demand * impact

            price_history.append(price)

            # ==================================================
            # SANITY CHECKS
            # ==================================================

            for bot in bots:

                if bot.inventory < 0:
                    raise Exception("Negative inventory")

                if bot.money < 0:
                    raise Exception("Negative money")

            # ==================================================
            # RECORD STEP DATA
            # ==================================================

            stats.record_step(price, buys_this_step, sells_this_step)

            # ==================================================
            # OCCASIONAL MARKET PRINT
            # ==================================================

            if step % config["print_interval"] == 0:

                print()
                print(f"STEP {step}")
                print(f"Price: {price}")
                print(f"Market Regime: {market_regime}")

                for i, bot in enumerate(bots):

                    print(
                        f"Bot {i} | "
                        f"Inv: {bot.inventory} | "
                        f"Money: {bot.money} | "
                        f"Agg: {bot.aggressiveness} | "
                        f"Ref: {bot.reference_price} | "
                        f"NW: {bot.net_worth(price)}"
                    )

                

        # ======================================================
        # RANKING
        # ======================================================

        ranking = sorted(
            bots,
            key=lambda bot: bot.net_worth(price),
            reverse=True
        )

        top_three = ranking[:3]

        print()
        print("TOP 3 BOTS")

        for i, bot in enumerate(top_three):

            print(
                f"Rank {i + 1} | "
                f"NW: {bot.net_worth(price)} | "
                f"Agg: {bot.aggressiveness} | "
                f"Ref: {bot.reference_price}"
            )

        # ======================================================
        # AVERAGE STATS
        # ======================================================

        avg_ref_price = sum(
            bot.reference_price for bot in bots
        ) / len(bots)

        avg_aggressiveness = sum(
            bot.aggressiveness for bot in bots
        ) / len(bots)

        avg_price = sum(price_history) / len(price_history)

        print()
        print(f"Average Reference Price: {avg_ref_price}")
        print(f"Average Aggressiveness: {avg_aggressiveness}")
        print(f"Average Market Price: {avg_price}")

        # ======================================================
        # RECORD GENERATION DATA
        # ======================================================

        stats.record_generation(bots, generation, price)

        # ======================================================
        # REPRODUCTION
        # ======================================================

        new_generation = []

        # --------------------------------------------------
        # Survivors
        # --------------------------------------------------

        for survivor in top_three:

            copied_bot = Bot(
                inventory= config["start_inventory"],
                money= config["start_money"],
                aggressiveness=survivor.aggressiveness,
                reference_price=survivor.reference_price
            )

            new_generation.append(copied_bot)

        # --------------------------------------------------
        # Mutated offspring
        # --------------------------------------------------

        for parent in top_three:

            # Reference price mutation
            mutated_reference = parent.reference_price

            if random.randint(1, 2) == 1:

                mutated_reference += random.randint(-2, 2)

                mutated_reference = max(
                    config["mutation_ref_min"],
                    min(config["mutation_ref_max"], mutated_reference)
                )

            # Aggressiveness mutation
            mutated_aggressiveness = parent.aggressiveness

            if random.randint(1, 2) == 1:

                mutated_aggressiveness += random.randint(-1, 1)

                mutated_aggressiveness = max(
                    config["agg_clamp_min"],
                    min(config["agg_clamp_max"], mutated_aggressiveness)
                )

            child = Bot(
                inventory=config["start_inventory"],
                money=config["start_money"],
                aggressiveness=mutated_aggressiveness,
                reference_price=mutated_reference
            )

            new_generation.append(child)

        # ======================================================
        # REPLACE OLD GENERATION
        # ======================================================

        bots = new_generation

        print()
        print("NEW GENERATION CREATED")

        for i, bot in enumerate(bots):

            print(
                f"Bot {i} | "
                f"Agg: {bot.aggressiveness} | "
                f"Ref: {bot.reference_price}"
            )

    print()
    print("===================================================")
    print("FINAL POPULATION")
    print("===================================================")

    for i, bot in enumerate(bots):

        print(
            f"Bot {i} | "
            f"Agg: {bot.aggressiveness} | "
            f"Ref: {bot.reference_price}"
        )   