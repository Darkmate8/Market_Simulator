# Market Simulator — Phase Plan (v2 through v4)

This document is the roadmap for the next 3 phases of the market simulator.
It replaces vague goals like "learn OOP" with specific behavioral milestones,
the way the v1 goals were structured.

**Rule:** Do not start a phase until the previous one is fully done.
**Rule:** Do not add features that aren't listed here without writing them
down first. Scope creep killed v1's readability.

---

## How to use this document

- Each phase has **mini-goals**. Each mini-goal is small enough to finish in
  one focused sitting (45–90 min).
- Each mini-goal has:
  - **What to build** — the specific behavior or change
  - **Concept to learn** — the Python idea this teaches
  - **Acceptance test** — how you know it's done
- Work strictly in order. Don't skip ahead.
- Before writing code for any mini-goal: explain the concept back to Claude
  in your own words. If you can't, you don't know it yet.
- After each mini-goal: commit to Git with a clear message.

---

# PHASE 1 — OOP Refactor (v1 → v2)

**Phase goal:** The simulator behaves identically to v1, but is now organized
into classes and multiple files. No new mechanics. No new features. Same
inputs, same outputs, cleaner skeleton.

**Why this phase exists:** v1 uses parallel lists (`inventory[i]`, `money[i]`,
`aggressiveness[i]` all referring to "bot i"). This breaks the moment you add
a new bot attribute, a new bot type, or any feature that doesn't fit the
existing parallel-list shape. Phase 1 fixes the foundation so Phases 2–7
become possible.

**Phase done when:** Running `python main.py` produces a generational
simulation with the same kind of output as v1, but the code lives in 3–4
files, uses a `Bot` class, and has the matching bug fixed.

---

## Mini-goal 1.1 — Set up the project folder

**What to build:**
- Create a folder `market-sim/` (or whatever you want to call it)
- Move your existing `main.py` into it as `main_v1.py` (keep it as reference)
- Create an empty `main.py` for the new version
- Create a `.gitignore` file that ignores `__pycache__/`, `.venv/`, `*.pyc`
- `git init`, first commit: "Initial v2 project structure"

**Concept to learn:** Project structure. Why code lives in folders, not just
loose files. What `.gitignore` does and why you need it from day one.

**Acceptance test:**
- `ls` shows the folder structure
- `git log` shows your first commit
- `main.py` exists and is empty (or has just `print("hello")`)

---

## Mini-goal 1.2 — Understand what a class is, before writing one

**What to build:** Nothing. This is a learning checkpoint.

**Concept to learn:**
- What problem does a class solve?
- The difference between a class and an object/instance
- What `self` means
- What `__init__` does

**Acceptance test:** You can answer these to Claude in plain English:
1. Why are parallel lists (`inventory[i]`, `money[i]`) a bad pattern in v1?
2. If you make a `Bot` class, what attributes does each bot need?
3. What's the difference between `Bot` (the class) and `bot1 = Bot(...)`
   (an instance)?
4. Why does every method have `self` as the first parameter?

You do not need to write code for this mini-goal. You need to be able to
explain it. If you can't, do not move to 1.3.

---

## Mini-goal 1.3 — Build the Bot class (state only)

**What to build:** A `Bot` class that holds the four attributes a bot needs
in v1: `inventory`, `money`, `reference_price`, `aggressiveness`. No methods
yet except `__init__`.

Then in `main.py`: create 6 bot instances with the same starting values v1
used. Print each bot's attributes to confirm it works.

**Concept to learn:** `class`, `__init__`, `self`, attributes. How to
instantiate an object. How to access object attributes with `bot.inventory`
instead of `inventory[i]`.

**Acceptance test:**
- `main.py` creates 6 bots in a list
- Looping over the list and printing `bot.reference_price` for each gives
  you the same values as v1's `reference_price` list
- No methods on Bot yet besides `__init__`
- Code runs without errors

---

## Mini-goal 1.4 — Move the decision logic into `bot.decide(price)`

**What to build:** A method on `Bot` called `decide(price)` that takes the
current market price as input and returns one of three strings: `"buy"`,
`"sell"`, or `"hold"`.

Inside this method, replicate v1's decision logic exactly:
- Compare price to `self.reference_price` → intended action
- Apply inventory pressure to `effective_aggressiveness`
- Clamp aggressiveness to [1, 10]
- Roll random 1–10, compare to effective aggressiveness
- Return "buy", "sell", or "hold"

**Concept to learn:** Methods. How a method uses `self` to access the
object's own attributes. Why moving logic *onto the object* is cleaner than
having the logic live outside the object and read its data through indices.

**Acceptance test:**
- Loop through your bots, call `bot.decide(100)` on each, print results
- Output looks like: `Bot 0 decided: buy`, `Bot 1 decided: hold`, etc.
- Same decision logic as v1 (you can verify by running v1 with the same
  random seed and comparing — see optional note below)

**Optional but recommended:** Use `random.seed(42)` at the top of both v1
and v2 during testing. This makes the random rolls identical so you can
verify v2 produces the same decisions as v1. Remove the seed later.

---

## Mini-goal 1.5 — Move the execution logic into `bot.execute_trade(action, price)`

**What to build:** A method on `Bot` called `execute_trade(action, price)`.
Given an action ("buy" or "sell") and a price, it updates the bot's own
`inventory` and `money`.

For "buy": `self.inventory += 1`, `self.money -= price`
For "sell": `self.inventory -= 1`, `self.money += price`

**Concept to learn:** Methods that mutate `self`. The bot now owns both
the decision *and* the consequence — it doesn't need an outside function
reaching into its data.

**Acceptance test:**
- Create a bot, print its starting inventory and money
- Call `bot.execute_trade("buy", 100)`, print again — inventory up by 1,
  money down by 100
- Call `bot.execute_trade("sell", 105)`, print again — inventory back to
  start, money up by 5

---

## Mini-goal 1.6 — Add `bot.net_worth(price)` method

**What to build:** A small method that returns `self.money + self.inventory * price`.

**Concept to learn:** That methods aren't only for big logic. Small helper
methods that compute a property are normal and good.

**Acceptance test:** Loop through bots, print `bot.net_worth(100)` for each.
Matches v1's net worth calculation.

---

## Mini-goal 1.7 — Rewrite the inner simulation loop using Bot objects

**What to build:** Replace v1's inner step loop with a version that:
- Loops over `bots` (list of Bot objects), not `range(len(inventory))`
- Calls `bot.decide(price)` to collect intentions
- Sorts bots into `buyers` and `sellers` lists
- Matches them pairwise (fixing the bug from v1 along the way)
- Calls `bot.execute_trade(...)` on the matched bots
- Updates the price using net demand

**Critical: fix the matching bug.** In v1, the matching loop has bugs:
- `seller_bot` and `buyer_bot` are reset to 0 inside the loop, then `+=`
  used incorrectly
- `execute` flag is never reset to False when one list empties
- `sellers.pop(0)` and `buyers.pop(0)` happen even when there's no match

The clean version is:

```python
while sellers and buyers:
    seller = sellers.pop(0)
    buyer = buyers.pop(0)
    seller.execute_trade("sell", price)
    buyer.execute_trade("buy", price)
    total_sells += 1
    total_buys += 1
```

That's it. Five lines replace ~20 lines of v1's buggy version.

**Concept to learn:** How OOP makes the main loop dramatically shorter. The
loop is now about *coordinating* bots, not *managing their internal state*.

**Acceptance test:**
- One full step runs without errors
- Inventory and money totals are conserved across trades (every buy has a
  matched sell — total money across all bots stays constant after trades,
  total inventory across all bots stays constant)
- Add a sanity-check line that asserts this and runs every step

---

## Mini-goal 1.8 — Rewrite the outer generation loop

**What to build:** Wrap the step loop in a generation loop. After 200 steps:
- Rank bots by `net_worth(price)`
- Top 3 survive (their `reference_price` and `aggressiveness` carry forward)
- Bottom 3 are replaced by mutated copies of the top 3 (same mutation rules
  as v1)
- Reset all bots' `inventory` to 10 and `money` to 1000
- Run the next generation

**Concept to learn:** Lists of objects. Sorting objects by a method's
return value. Creating new objects from old ones.

**Acceptance test:**
- 10 generations run end to end
- Prints per generation: top 3 reference prices, top 3 aggressiveness,
  average price during that generation
- Across generations, the average reference price drifts toward whatever
  pricing emerged (same emergent behavior as v1)

---

## Mini-goal 1.9 — Split into multiple files

**What to build:** Move `Bot` into `bot.py`. Move the simulation loop into
`simulation.py` (with a function like `run_simulation(bots, num_steps, num_generations)`).
`main.py` becomes a thin entry point: import, create bots, call
`run_simulation`, print results.

Folder ends up like:
```
market-sim/
├── main.py
├── bot.py
├── simulation.py
├── main_v1.py          (kept as reference)
└── .gitignore
```

**Concept to learn:** Modules and imports. `from bot import Bot`. Why splitting
files makes a project navigable. The role of `main.py` as the entry point.

**Acceptance test:**
- `python main.py` runs the full simulation
- No file is over ~120 lines
- Each file does one thing: `bot.py` defines the bot, `simulation.py` runs
  the loop, `main.py` orchestrates

---

## Mini-goal 1.10 — Phase 1 commit + reflection

**What to build:** Nothing new. Cleanup:
- Remove any leftover debug `print`s you don't need
- Add brief comments at the top of each file saying what it does
- Final commit: "Phase 1 complete — v2 OOP refactor"

**Then write yourself a short note** (in a `NOTES.md` or whatever) answering:
1. What was the hardest part?
2. What concept finally clicked?
3. What's one thing you want to do differently in Phase 2?

This isn't busywork. It locks in the learning and tells you where to
focus next.

**Phase 1 done.** You now have v2.

---

# PHASE 2 — Config + Stats (v2 → v3)

**Phase goal:** All tuning parameters live outside the code. The simulator
records meaningful data during runtime and saves it to a file you can
analyze later.

**Why this phase exists:** Right now, changing "200 steps" to "500 steps"
means editing code. Changing starting money from 1000 to 5000 means editing
code. This is fine for one developer playing with one simulator. It is not
fine when you want to run 20 experiments with different parameters. Configs
fix that. Stats tracking is the prerequisite for ever analyzing what the
simulator is actually doing — without it, you're just watching numbers
scroll past.

**Phase done when:** You can change simulation parameters by editing a
`config.yaml` file (no code touched), and at the end of a run you get a
CSV with price history, trade volume, and per-bot net worth over time.

---

## Mini-goal 2.1 — Externalize parameters to `config.yaml`

**What to build:** A `config.yaml` file that holds:
- Number of bots
- Starting inventory, starting money
- Number of steps per generation
- Number of generations
- Regime switch probability, impact ranges
- Mutation parameters (range of reference price drift, aggressiveness drift)
- Aggressiveness clamp range

Then load the config in `main.py` using the `pyyaml` library.

**Concept to learn:** External configuration. The `pyyaml` library. Why
YAML is preferred over hardcoded values. Installing a package with `pip`.

**Acceptance test:**
- Changing a number in `config.yaml` (e.g., steps from 200 to 500) changes
  the simulation behavior without editing any `.py` file
- The simulation still runs identically when the config matches v2 defaults

---

## Mini-goal 2.2 — Pass config through the code cleanly

**What to build:** A `Config` class or a config dict that gets passed into
`run_simulation()` and into the `Bot` constructor where needed. No function
should read from a global. All parameters are passed explicitly.

**Concept to learn:** Dependency injection (the simple version — passing
data in instead of reading globals). Why globals are bad in larger
projects.

**Acceptance test:** Search your code for the string `200`, `1000`, `10`,
`6` (typical hardcoded numbers from v1). None of them should appear as
"magic numbers" anymore — they all come from config.

---

## Mini-goal 2.3 — Build a `StatsTracker` class

**What to build:** A class that gets passed into the simulation and records:
- Price at each step
- Number of buys and sells per step
- Each bot's net worth at the end of each generation
- Each bot's reference price and aggressiveness at the end of each generation

Methods like `stats.record_step(price, buys, sells)` and
`stats.record_generation(bots)`.

**Concept to learn:** Composition (the simulation *has-a* stats tracker).
Lists of dicts (or dicts of lists) for time-series data. Why you separate
"the thing happening" from "the thing recording what's happening."

**Acceptance test:**
- A simulation run produces an in-memory record of everything
- You can print summary stats at the end: average price, total trades,
  most-improved bot

---

## Mini-goal 2.4 — Save stats to CSV

**What to build:** `stats.save_to_csv(filename)` that writes the recorded
data to one or more CSV files. At minimum:
- `price_history.csv` — step, price, buys, sells
- `bot_evolution.csv` — generation, bot_id, reference_price,
  aggressiveness, net_worth

**Concept to learn:** File I/O. The `csv` library. Why CSV is a useful
default output format (Excel opens it, Python reads it back, anyone can
inspect it).

**Acceptance test:**
- After a run, two CSV files exist
- Open them in any spreadsheet program and the data makes sense
- The price history matches what was printed to console

---

## Mini-goal 2.5 — Phase 2 commit + reflection

Same drill as 1.10. Commit, note what you learned.

**Phase 2 done.** You now have v3.

---

# PHASE 3 — Real Order Book (v3 → v4)

**Phase goal:** Bots submit *orders* (price + quantity), and a matching
engine pairs them based on price priority. This produces an emergent
bid-ask spread instead of a single artificial price.

**Why this phase exists:** v1 and v2 use a fictional "single price" — every
trade happens at the same price the model produces. Real markets don't work
that way. Real markets have a bid-ask spread, a limit order book, and price
emerges from order matching. This phase is the leap from a toy model to
something that resembles actual market microstructure.

**Phase done when:** The simulator maintains an order book with bids
(buy orders) and asks (sell orders), bots submit limit orders, the matching
engine pairs them at the best available prices, and the price the
simulator reports is the most recent trade price — not an externally
imposed number.

---

## Mini-goal 3.1 — Define an `Order` class

**What to build:** A simple class with:
- `side` ("buy" or "sell")
- `price` (the limit price the bot is willing to accept)
- `quantity`
- `bot` (reference back to the bot that submitted it)

**Concept to learn:** Lightweight data classes. The relationship between a
Bot (the actor) and an Order (the action).

---

## Mini-goal 3.2 — Build the `OrderBook` class

**What to build:** A class that holds two lists: `bids` (sorted by price
descending — highest first) and `asks` (sorted by price ascending — lowest
first). Methods: `add_order(order)`, `match()`, `best_bid()`, `best_ask()`,
`spread()`.

**Concept to learn:** Sorted data structures. Why bids and asks have
opposite sort orders. The concept of a "book" as a state object the market
maintains.

---

## Mini-goal 3.3 — Update bots to submit limit orders

**What to build:** `bot.decide(order_book)` no longer returns a string. It
returns an `Order` (or `None`). The bot looks at `order_book.best_bid()`
and `order_book.best_ask()` and decides what price to offer.

**Concept to learn:** Bots reasoning about *the market*, not just the price.
This is where bot strategies start to matter — and where Phase 5 (multiple
bot types) becomes natural.

---

## Mini-goal 3.4 — Build the matching engine

**What to build:** Inside `OrderBook.match()`: while the best bid price >=
the best ask price, execute a trade at one of those prices (convention:
the price of the order that was there first), then remove or decrement
those orders.

**Concept to learn:** Matching algorithms. Price-time priority. The
fundamental rule of all real exchanges.

---

## Mini-goal 3.5 — Replace the artificial price with last-trade price

**What to build:** Remove the v1/v2 "price + net_demand * impact" logic.
Price is now defined as "the price of the most recent trade." If no trade
happened this step, the price is the midpoint of the spread (or unchanged).

**Concept to learn:** Emergent price. The single most important concept in
market microstructure — price isn't set, it's discovered.

---

## Mini-goal 3.6 — Update stats tracker for the new model

**What to build:** Track bid-ask spread, order book depth, number of
matched vs unmatched orders per step. Save to CSV.

---

## Mini-goal 3.7 — Phase 3 commit + reflection

**Phase 3 done.** You now have v4.

---

# What comes after Phase 3 (preview, not detailed yet)

Once you've finished Phase 3, the next obvious phases are:

- **Phase 4 — Multiple bot types.** `MeanReverter`, `Momentum`,
  `MarketMaker`, `Noise`. This is where inheritance becomes useful and
  where the simulation starts producing genuinely interesting dynamics.

- **Phase 5 — Better evolution.** Cross-bot mutation, fitness functions
  that reward more than just net worth, possibly a tournament structure.

- **Phase 6 — Analysis tooling.** Jupyter notebook (or scripts) that load
  the CSVs and produce charts. This is where NumPy and matplotlib enter.

- **Phase 7 — The "vibe-coding" transition.** By here you've built the
  judgment to evaluate AI-generated code. You start letting Claude Code
  draft larger pieces while you review.

We will write detailed plans for these only after Phase 3 is done. Trying
to plan them now is premature — Phase 3 will change what makes sense for
Phase 4.

---

# Operating principles for this project

These apply to every phase. Pin them.

1. **No new feature without writing it down here first.** If you have an
   idea mid-phase, add it to a "future ideas" list. Don't build it.

2. **No code you don't understand.** If Claude shows you a snippet you
   can't explain back, stop and learn it first.

3. **Commit after every mini-goal.** Small commits are recoverable. Giant
   commits are not.

4. **One mini-goal per sitting.** Splitting attention across mini-goals
   produces half-finished mini-goals. Pick one, finish it, then stop.

5. **When stuck for more than 30 minutes, ask Claude.** Don't burn an
   evening on something a 2-line explanation would unstick.

6. **The simulator's behavior is the truth.** If your refactored code
   produces different output than v1 (with the same random seed), the
   refactor is wrong. Fix it before moving on.
