import random

# ======================================================
# 0. INITIAL STATE
# ======================================================





inventory = [10, 10, 10, 10, 10, 10]
reference_price = [97, 100, 103, 95, 101, 99]
aggressiveness = [3, 7, 9, 9, 5, 4]
money = [1000, 1000, 1000, 1000, 1000, 1000]


market_regime = "high liquidity"



for generation in range(10):
    
    price = 100
    net_worth = []
    price_history = []
    bot_action_log = []
    
    
    if len(inventory) != 6:
        raise Exception("inventory issue")
    
    if len(reference_price) != 6:
        raise Exception("reference list issue")
    
    if len(aggressiveness) != 6:
        raise Exception("aggressiveness list issue")
    
    if len(money) != 6:
        raise Exception("money list issue")
   
   
    # ======================================================
    # 1. SIMULATION LOOP
    # ======================================================

    for step in range(200):
        
        
        # --------------------------------------------------
        # 1.1 Regime switch (every 10 steps)
        # --------------------------------------------------
        if step % 5 == 0:
            if random.randint(1, 2) == 2:
                market_regime = "low liquidity"
            else:
                market_regime = "high liquidity"

        # --------------------------------------------------
        # 1.2 Decision roll
        # --------------------------------------------------
        comparision_number = random.randint(1, 10)

        # --------------------------------------------------
        # 1.3 Liquidity impact
        # --------------------------------------------------
        if market_regime == "high liquidity":
            impact = random.randint(1, 3)
        else:
            impact = random.randint(4, 7)

        
        
        total_buys = 0
        total_sells = 0
        
        # --------------------------------------------------
        # 1.4 Iterate through bots bot
        # --------------------------------------------------
        
        for index_bot in range(len(inventory)):
            
            
            effective_aggressiveness = aggressiveness[index_bot]

            
            comparision_number = random.randint(1, 10)
            
            # --------------------------------------------------
            # 1.4.2 Intended action
            # --------------------------------------------------
            if price > reference_price[index_bot]:
                chosen_action = "sell"
            elif price < reference_price[index_bot]:
                chosen_action = "buy"
            else:
                chosen_action = "nothing"

            # --------------------------------------------------
            # 1.4.3 Inventory pressure (Goal 6B)
            # --------------------------------------------------
            if chosen_action == "sell":
                if inventory[index_bot] < 4:
                    effective_aggressiveness -= 3
                elif inventory[index_bot] >= 7:
                    effective_aggressiveness += 3

            elif chosen_action == "buy":
                if inventory[index_bot] > 7:
                    effective_aggressiveness -= 3
                elif inventory[index_bot] <= 4:
                    effective_aggressiveness += 3

            # Clamp aggressiveness
            effective_aggressiveness = max(1, min(10, effective_aggressiveness))

            # --------------------------------------------------
            # 1.4.4 Act or hesitate
            # --------------------------------------------------
            if comparision_number <= effective_aggressiveness:
                decision = "yes"
            else:
                decision = "do not"

            # --------------------------------------------------
            # 1.4.5 Apply action
            # --------------------------------------------------
            
            execute = False
            
            if decision == "yes":
                if chosen_action == "sell" and inventory[index_bot] > 0:
                    execute = True
                elif chosen_action == "buy" and money[index_bot] >= price: 
                    execute = True
            else:
                execute = False
             
            
            if execute == True:
                if chosen_action == "sell":
                    inventory[index_bot] -= 1
                    money[index_bot] += price
                    total_sells += 1

                elif chosen_action == "buy":
                    inventory[index_bot] += 1
                    money[index_bot] -= price
                    total_buys += 1

        # --------------------------------------------------
        # 1.5 Price changes + Record
        # --------------------------------------------------
        
        net_demand = total_buys - total_sells
        price += net_demand * impact
        price_history.append(price)
        
        

        # --------------------------------------------------
        # 1.6 Sanity checks
        # --------------------------------------------------
        if len(price_history) >= 2:
            price_change = price_history[-1] - price_history[-2]

            
            if net_demand > 0 and price_change != net_demand * impact:
                raise Exception("Bad BUY impact")

            if net_demand < 0 and price_change != net_demand * impact:
                raise Exception("Bad SELL impact")

            

        for inv in inventory:
            if inv < 0:
                raise Exception("Negative inventory")
            
        for cash in money:
            if cash < 0:
                raise Exception("Negative money")
            
        if step % 10 == 0:
            if price_history[-1] > 115 or price_history[-1] < 85:
                print(f"Price is currently: {price_history[-1]}")
                print(f"Market liquidity: {market_regime}")
                print()


    # ======================================================
    # 2. NET WORTH & RANKING
    # ======================================================

    for i in range(len(inventory)):
        net = money[i] + (inventory[i] * price)
        net_worth.append(net)

    ranking = sorted(
        [(i, net_worth[i]) for i in range(len(net_worth))],
        key=lambda x: x[1],
        reverse=True
    )

    top_three_indices = [i for i, _ in ranking[:3]]
    top_three = ranking[:3]



    #FINDING AVG REF PRI AND AVG AGGRESSIVENESS
    total_ref_price = 0
    for ref_pri in range(len(reference_price)):
        temp_ref_pri = reference_price[ref_pri]
        total_ref_price += temp_ref_pri
        
    avg_ref_pri = total_ref_price / len(reference_price)
    
    print()
    print(f"Avg reference price: {avg_ref_pri}")
    print()
    
    total_agg = 0
    for agg in range(len(aggressiveness)):
        temp_agg = aggressiveness[agg]
        total_agg += temp_agg
    
    avg_agg = total_agg / len(aggressiveness)
    
    print()
    print(f"Avg aggressivness: {avg_agg}")
    print()
    
    
    total_pp = 0
    for pp in range(len(price_history)):
        temp_pp = price_history[pp]
        total_pp += temp_pp
    
    avg_pp = total_pp / len(price_history)
    
    print()
    print(f"Avg price: {avg_pp}")
    print()

    # ======================================================
    # 3. REPRODUCTION (GOAL 7)
    # ======================================================

    new_inventory = [10, 10, 10, 10, 10, 10]
    new_money = [1000, 1000, 1000, 1000, 1000, 1000]
    new_reference_price = []
    new_aggressiveness = []

    # --- Copy survivors ---
    for idx in top_three_indices:
        new_reference_price.append(reference_price[idx])
        new_aggressiveness.append(aggressiveness[idx])

    # --- Mutated offspring ---
    for idx in top_three_indices:

        # Reference price mutation
        coin_flip = random.randint(1, 2)
        if coin_flip == 1:
            reference_add = random.randint(-2, 2)
            temp_reference = reference_price[idx] + reference_add
            temp_reference = max(85, min(115, temp_reference))
            new_reference_price.append(temp_reference)
        else:
            new_reference_price.append(reference_price[idx])

        # Aggressiveness mutation
        coin_flip_2 = random.randint(1, 2)
        if coin_flip_2 == 1:
            aggressive_add = random.randint(-1, 1)
            temp_aggressiveness = aggressiveness[idx] + aggressive_add
            temp_aggressiveness = max(1, min(10, temp_aggressiveness))
            new_aggressiveness.append(temp_aggressiveness)
        else:
            new_aggressiveness.append(aggressiveness[idx])


    # ======================================================
    # 4. GENERATION REPLACEMENT
    # ======================================================

    inventory = new_inventory
    money = new_money
    reference_price = new_reference_price
    aggressiveness = new_aggressiveness
    
    print("Generation:", generation)
    print("Reference Prices:", reference_price)
    print("Aggressiveness:", aggressiveness)
    print("----------------------------")



print(f"New reference price is: {reference_price}")
print(f"New agressiveness is: {aggressiveness}")
