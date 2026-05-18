import csv
import os

# ======================================================
# STATS TRACKER CLASS
# ======================================================

class StatsTracker:

    def __init__(self):

        # --------------------------------------------------
        # Step-level tracking
        # --------------------------------------------------

        self.step_data = []
        self.generation_data = []


    def record_step(self, price, buys, sells):

        self.step_data.append({
            "step": len(self.step_data),
            "price": price,
            "buys": buys,
            "sells": sells
        })
        
        self.save_to_csv("price_history.csv", self.step_data)


    def record_generation(self, bots, generation_num, current_price):

        for i, bot in enumerate(bots):

            self.generation_data.append({
                "generation": generation_num,
                "bot_id": i,
                "reference_price": bot.reference_price,
                "aggressiveness": bot.aggressiveness,
                "net_worth": bot.net_worth(current_price)
            })
        
        self.save_to_csv("bot_evolution.csv", self.generation_data)

    def save_to_csv(self, filename, data):
        if not data:
            return
        
        with open(filename, "w", newline="") as f1:
            writer = csv.DictWriter(
                f1,
                fieldnames= data[0].keys()
            )
            
            writer.writeheader()  
            writer.writerows(data)
            
            

    def total_trades(self):

        return sum(s["buys"] + s["sells"] for s in self.step_data)

    def average_price(self):

        if not self.step_data:
            return 0

        return sum(s["price"] for s in self.step_data) / len(self.step_data)

    def average_price_per_generation(self, generation_num, steps_per_generation):

        gen_start = generation_num * steps_per_generation
        gen_end = gen_start + steps_per_generation

        gen_prices = [
            s["price"] for s in self.step_data
            if gen_start <= s["step"] < gen_end
        ]

        if gen_prices:
            return sum(gen_prices) / len(gen_prices)
        return 0
