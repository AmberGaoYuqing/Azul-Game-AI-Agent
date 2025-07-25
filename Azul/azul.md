# Azul: A Competitive Game 🎲

This repository contains the full implementation of the **Azul board game simulator and visualizer**, used for building and testing intelligent agents in a competitive environment. It provides a modular codebase including core game logic, rule enforcement, rendering, and agent integration.

---

##  Key Files

###  Main Logic:

* `core/azul_model.py` – Implements Azul game mechanics and state transitions. Includes methods like `getLegalActions()` and game simulation support.
* `core/azul_utils.py` – Contains constants and utility functions related to Azul tiles, board structure, and rules.
* `core/general_game_runner.py` – Command-line runner that manages matches, replays, logging, and display.
* `core/player_interface.py` – Interface definition for AI agents to interact with the game engine.

###  Agent Examples:

* `agents/generic/single_lookahead.py` – A basic lookahead agent skeleton showing how to structure agent logic.
* `agents/generic/random.py` – A baseline agent making random moves, useful for testing.
* `agents/sample_team/my_agent.py` – The agent you are meant to build and submit.

>  Only the folder `agents/t_XXX/` will be used in evaluation. You may add additional modules within it.

---

##  Game Interface

When launched, the game provides two windows:

* **Game window** – Displays the Azul board and current score.
* **Activity log** – Shows the action history. Clickable to replay each step.

A text-only mode is also available for headless environments.

---

## Running the Game

Install requirements:

```bash
python -m pip install func_timeout pytz
```

Run a sample game between random agents:

```bash
python core/general_game_runner.py -g Azul -a [agents.generic.random,agents.generic.random]
```

Run your agent:

```bash
python core/general_game_runner.py -g Azul -a [agents.sample_team.my_agent,agents.generic.random]
```

Check all options:

```bash
python core/general_game_runner.py -h
```

Common flags:

* `-t`: text mode
* `-s`: save replay
* `-l`: save logs
* `--half-scale`: GUI scaling for small screens

---

##  Time & Fair Play Constraints

* Each agent is given **1 second per move**.
* Moves >3 seconds or excessive warnings lead to forfeiture.
* A 15-second warm-up period at the start is allowed (e.g., for loading policies).

Agents **may not use multi-threading** or compute during the opponent’s turn.

---

##  Competition & Ranking

* Agents are ranked using the [ELO system](https://en.wikipedia.org/wiki/Elo_rating_system)  .
* Win: 3 pts, Tie: 1 pt, Loss: 0 pts
* Staff teams with strong agents will participate in the tournament (prefix: `staff-`).

---

##  Warnings

* All `stdout`/`stderr` from your agent will be visible in tournament logs. Avoid leaking confidential info.
* Crashes will be shown with stack traces in public logs.

---

##  Learn More

* Official rules: [ultraboardgames.com/azul](https://www.ultraboardgames.com/azul/game-rules.php) &#x20;
* Tutorial video by Becca Scott: [YouTube Link](https://youtu.be/y0sUnocTRrY) &#x20;

---

##  Summary

This environment provides a rich platform for developing AI agents that play Azul competitively. With a robust and clean codebase, developers can focus on decision-making logic, experiment with strategies, and participate in tournament-style evaluation.
