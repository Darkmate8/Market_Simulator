import random


# ---------- INITIAL STATE ----------
price = 100
bots = [10, 10, 10, 10, 10, 10]
reference_price = [97, 100, 103, 95, 101, 99]

price_history = []
bot_action_log = []


market_regime = "high liquidity"

actions = ["buy", "sell", "nothing"]



# ---------- SIMULATION LOOP ----------
for step in range(50):
    
    # Step finder
    if step % 10 == 0:
        num = random.randint(1,2)
        if num > 1:
            market_regime = "low liquidity"
        else:
            market_regime = "high liquidity"
    
    # 1. Impact finder
    if market_regime == "high liquidity":
        impact = random.randint(1,3)
    elif market_regime == "low liquidity":
        impact = random.randint(4,7)
        
    # 2. Choose actor and action
    index_bot = random.choice(range(len(bots)))

    
    if price > reference_price[index_bot]:
        chosen_action = "sell"
    elif price < reference_price[index_bot]:
        chosen_action = "buy"
    elif price == reference_price[index_bot]:
        chosen_action = "nothing"

    # 3. Apply action
    if chosen_action == "sell":
        if bots[index_bot] > 0:
            bots[index_bot] -= 1
            price -= impact

    elif chosen_action == "buy":
        bots[index_bot] += 1
        price += impact

    elif chosen_action == "nothing":
        pass

    # 4. Record state
    price_history.append(price)
    bot_action_log.append(f"bot {index_bot} {chosen_action}")

    # 5. Sanity checks
    if len(price_history) >= 2:
        price_change = price_history[-1] - price_history[-2]

        if chosen_action == "buy" or chosen_action == "sell":
            abs(price_change) == impact
        elif chosen_action == "nothing":
            abs(price_change) == 0
        else:
            raise Exception("Price changed by the wrong amount")
            
        if chosen_action == "nothing" and price_change != 0:
            raise Exception("Price changed even though nothing happened")

    for inv in bots:
        if inv < 0:
            raise Exception("Inventory went negative")

    # Optional debug print
    # print(bots)


# ---------- OUTPUT ----------
print(bots)
print(price_history)
