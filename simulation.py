import random
from bot import Bot

def run_simulation(bots, num_steps, num_generations):
    

    market_regime = "high liquidity"
    
    for generation in range(num_generations):

        print()
        print("===================================================")
        print(f"GENERATION {generation}")
        print("===================================================")

        price = 100

        price_history = []

        # ==================================================
        # SIMULATION LOOP
        # ==================================================

        for step in range(num_steps):

            # --------------------------------------------------
            # Market regime switch
            # --------------------------------------------------

            if step % 5 == 0:

                if random.randint(1, 2) == 1:
                    market_regime = "high liquidity"

                else:
                    market_regime = "low liquidity"

            # --------------------------------------------------
            # Liquidity impact
            # --------------------------------------------------

            if market_regime == "high liquidity":
                impact = random.randint(1, 3)

            else:
                impact = random.randint(4, 7)

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
            # OCCASIONAL MARKET PRINT
            # ==================================================

            if step % 20 == 0:

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
        # REPRODUCTION
        # ======================================================

        new_generation = []

        # --------------------------------------------------
        # Survivors
        # --------------------------------------------------

        for survivor in top_three:

            copied_bot = Bot(
                inventory=10,
                money=1000,
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
                    85,
                    min(115, mutated_reference)
                )

            # Aggressiveness mutation
            mutated_aggressiveness = parent.aggressiveness

            if random.randint(1, 2) == 1:

                mutated_aggressiveness += random.randint(-1, 1)

                mutated_aggressiveness = max(
                    1,
                    min(10, mutated_aggressiveness)
                )

            child = Bot(
                inventory=10,
                money=1000,
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