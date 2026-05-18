import random


# ======================================================
# BOT CLASS
# ======================================================

class Bot:

    def __init__(self, inventory, money, aggressiveness, reference_price):

        self.inventory = inventory
        self.money = money
        self.aggressiveness = aggressiveness
        self.reference_price = reference_price

    # --------------------------------------------------
    # Decide whether to buy/sell/hold
    # --------------------------------------------------

    def decide(self, price):

        effective_aggressiveness = self.aggressiveness

        # Intended action
        if price > self.reference_price:
            chosen_action = "sell"

        elif price < self.reference_price:
            chosen_action = "buy"

        else:
            chosen_action = "hold"

        # Inventory pressure
        if chosen_action == "sell":

            if self.inventory < 4:
                effective_aggressiveness -= 3

            elif self.inventory >= 7:
                effective_aggressiveness += 3

        elif chosen_action == "buy":

            if self.inventory > 7:
                effective_aggressiveness -= 3

            elif self.inventory <= 4:
                effective_aggressiveness += 3

        # Clamp between 1 and 10
        effective_aggressiveness = max(
            1,
            min(10, effective_aggressiveness)
        )

        # Random hesitation / confidence roll
        comparison_number = random.randint(1, 10)

        if comparison_number <= effective_aggressiveness:
            return chosen_action

        return "hold"

    # --------------------------------------------------
    # Execute actual trade
    # --------------------------------------------------

    def execute_trade(self, action, price):

        if action == "buy":

            if self.money >= price:
                self.inventory += 1
                self.money -= price

        elif action == "sell":

            if self.inventory > 0:
                self.inventory -= 1
                self.money += price

    # --------------------------------------------------
    # Net worth
    # --------------------------------------------------

    def net_worth(self, price):

        return self.money + (self.inventory * price)



