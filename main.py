import random

# --- 0. INITIAL STATE ---
price = 100

bots = [10, 10, 10, 10, 10, 10]
reference_price = [97, 100, 103, 95, 101, 99]
agressivness = [3, 7, 9, 9, 5, 4]
money = [1000, 1000, 1000, 1000, 1000, 1000]
net_worth = []

price_history = []
bot_action_log = []

market_regime = "high liquidity"


# --- 1. SIMULATION LOOP ---
for step in range(50):

    # 1.1 Regime switch (every 10 steps)
    if step % 10 == 0:
        if random.randint(1, 2) == 2:
            market_regime = "low liquidity"
        else:
            market_regime = "high liquidity"

    # 1.2 Random draw for decision
    comparision_number = random.randint(1, 10)

    # 1.3 Impact by liquidity
    if market_regime == "high liquidity":
        impact = random.randint(1, 3)
    else:
        impact = random.randint(4, 7)

    # 1.4 Choose bot
    index_bot = random.choice(range(len(bots)))
    effective_aggressiveness = agressivness[index_bot]

    # 1.5 Decide intended action
    if price > reference_price[index_bot]:
        chosen_action = "sell"
    elif price < reference_price[index_bot]:
        chosen_action = "buy"
    else:
        chosen_action = "nothing"

    # 1.6 Inventory pressure (Goal 6B)
    if chosen_action == "sell":
        if bots[index_bot] < 4:
            effective_aggressiveness -= 3
        elif bots[index_bot] >= 7:
            effective_aggressiveness += 3

    elif chosen_action == "buy":
        if bots[index_bot] > 7:
            effective_aggressiveness -= 3
        elif bots[index_bot] <= 4:
            effective_aggressiveness += 3

    # Clamp
    effective_aggressiveness = max(1, min(10, effective_aggressiveness))

    # 1.7 Act or hesitate
    if comparision_number <= effective_aggressiveness:
        decision = "yes"
    else:
        decision = "do not"

    # 1.8 Apply action
    if decision == "yes":
        if chosen_action == "sell" and bots[index_bot] > 0:
            bots[index_bot] -= 1
            money[index_bot] += price
            price -= impact
        elif chosen_action == "buy" and money[index_bot] >= price:
            bots[index_bot] += 1
            money[index_bot] -= price
            price += impact

    # 1.9 Record
    price_history.append(price)
    bot_action_log.append(f"bot {index_bot} {chosen_action}")
    

    # 1.10 Sanity checks
    if len(price_history) >= 2:
        price_change = price_history[-1] - price_history[-2]

        if decision == "yes":
            if chosen_action == "buy" and price_change != impact:
                raise Exception("Bad BUY impact")
            if chosen_action == "sell" and price_change != -impact:
                raise Exception("Bad SELL impact")
            if chosen_action == "nothing" and price_change != 0:
                raise Exception("NOTHING moved price")
            if chosen_action == "buy" and money[index_bot] < price:
                raise Exception("Not enough Money")
        else:
            if price_change != 0:
                raise Exception("Price moved without action")

    for inv in bots:
        if inv < 0:
            raise Exception("Negative inventory")
        


for num in range(len(bots)):
    net = money[num] + (bots[num]*price)
    net_worth.append(net)




# --- 2. OUTPUT ---
print(bots)
print(price_history[-6:-1])
print(money)
print(net_worth)
