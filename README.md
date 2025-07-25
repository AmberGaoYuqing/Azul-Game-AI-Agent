# Azul Game AI Agent 

<p align="center"> 
    <img src="img/azul.jpg" alt="Picture of Azul board" width="400">
 </p>


# Azul Game AI Agent 🎯

This project implements an autonomous agent capable of playing the board game **Azul** competitively.
The agent was developed using a modular architecture, allowing integration of multiple AI planning and decision-making strategies.

> ⚠️ This version is published as an independent educational showcase.
> All course-specific content and confidential assessment information have been removed.

---

## 🎮 About the Game

**Azul** is a two-player strategy board game where players take turns selecting colored tiles and placing them on their board to maximize points. The game involves complex planning, pattern recognition, and tactical adaptation.

In this project, the Azul environment is simulated with a game engine and visual interface. The agent interacts with the engine using defined APIs and must make decisions under strict time constraints (1 second per move, with a 15-second initialization buffer).

More information on the board game rules can be found [here](https://www.ultraboardgames.com/azul/game-rules.php), or you can watch [this explanation video](https://youtu.be/y0sUnocTRrY)  .

---

##  Features & Techniques

The agent integrates multiple AI decision-making modules and supports plug-and-play architecture for experimenting with different strategies:

* ✅ **Heuristic Search Algorithms**

  * Using Azul-specific evaluation functions based on tile value, board layout, and completion potential.
* ✅ **Monte Carlo Tree Search (MCTS)**

  * With UCT (Upper Confidence Bound) action selection for stochastic simulations.
* ✅ **Rule-Based and Lookahead Agents**

  * Including depth-limited planning and utility functions.
*  Optional support for precomputed policy loading during the 15-second initialization period.
*  Modular structure allowing easy replacement of decision-making modules.

---

##  Project Structure

```
azul-agent/
├── agents/
│   └── sample_team/
│       ├── my_agent.py       # Main logic of the autonomous agent
│       ├── heuristics.py     # Heuristic evaluations
│       ├── mcts.py           # Monte Carlo Tree Search logic
│       └── utils.py          # Game state helpers and evaluation tools
├── core/
│   ├── azul_model.py         # Azul game logic and valid action generator
│   ├── player_interface.py   # Interface class for agent interaction
│   ├── general_game_runner.py # Game setup, runner, logging, and rendering
│   └── azul_utils.py         # Constants and helpers
├── tests/                    # Unit tests and agent comparisons
└── README.md
```

---

##  Getting Started

**Dependencies**:

* Python 3.8+
* `func-timeout`, `pytz`

Install dependencies:

```bash
python -m pip install func_timeout pytz
```

Run a match between two random agents:

```bash
python core/general_game_runner.py -g Azul -a [agents.generic.random,agents.generic.random]
```

Run your agent against a random opponent:

```bash
python core/general_game_runner.py -g Azul -a [agents.sample_team.my_agent,agents.generic.random]
```

View options:

```bash
python core/general_game_runner.py -h
```

Common options:

* `-t`: Text-only interface (for headless environments)
* `-p`: Print output to terminal
* `-s`: Save game replay
* `-l`: Save game log

---

##  Time Constraints

* Each agent has **1 second per move**.
* A move exceeding **3 seconds** results in forfeiture.
* A **15-second buffer** at game start is allowed for policy loading or other setup.

Agents using multithreading or computing during the opponent’s turn will be **disqualified**.

---

##  Example Output

The agent competes against various built-in strategies and logs decision details:

```
Turn 3: MCTS selected move [Factory 2 → Row 4] with expected value 3.27
Turn 4: HeuristicAgent chose action [Factory 1 → Row 1] maximizing adjacency bonus
```

---

##  Highlights

* Competitive Azul AI built with modular, extendable architecture
* Multiple strategies benchmarked in simulation
* Designed for reproducibility and experimentation
* Git-driven development and testing workflow

---

##  License

This version is released under the [MIT License](LICENSE), which means you are free to use, modify, and share the code for **educational and non-commercial purposes**, provided that the original license and authorship notices are retained.

---

##  About This Repository

This is a **personal adaptation** and public showcase of an AI game-playing agent for Azul.
It does **not** contain assessment content or confidential material from any university course.
All implementations are original or modified and refactored for open sharing.

---

##  Acknowledgements

* Game rules adapted from the board game **Azul**
* Code design inspired by AI planning, search, and MCTS strategies
* Visualization and game engine structure inspired by general academic competition platforms
