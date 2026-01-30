# Learn2Slither
A cutting-edge Q-learning project focused on autonomous decision-making in a dynamic environment

# 🐍 Learn2Slither — Reinforcement Learning Snake

Learn2Slither is a reinforcement learning project where an intelligent agent learns to control a snake through trial and error.  
Using **Q-learning**, the agent interacts with a grid-based environment, receives rewards or penalties, and progressively improves its behavior over many training sessions.

The ultimate goal: **reach a snake length of at least 10 and survive as long as possible.**

---

## ✨ Features

- 10×10 board-based Snake environment
- Reinforcement Learning agent powered by **Q-learning**
- Green apples (reward) and red apples (penalty)
- Multiple training sessions with exploration vs exploitation
- Exportable / importable trained models
- Graphical visualization (with adjustable speed)
- Step-by-step mode for debugging and demonstrations
- Head-only “vision” state representation (4 directions)
- Non-learning (evaluation) mode to benchmark trained models

---

## 🧠 Project Overview

The project is split into two main parts:

### Environment (Board)

- Fixed size: **10×10**
- Items:
  - 🟢 Two green apples (increase snake length by 1)
  - 🔴 One red apple (decrease snake length by 1)
  - 🔵 Snake (starts with length 3, placed randomly and contiguously)

Game over conditions:

- Snake hits a wall
- Snake collides with itself
- Snake length drops to 0

Each run is called a **training session**. A single session is not enough — the agent must be trained over many sessions (often hundreds or thousands).

A graphical window displays the board, and each agent action updates the environment in real time.

---

### Agent (Reinforcement Learning)

#### State (Snake Vision)

The agent only sees what is accessible from the snake’s head in the **four cardinal directions** (UP, DOWN, LEFT, RIGHT).

Each direction is encoded as:

- `W` — Wall  
- `H` — Snake head  
- `S` — Snake body  
- `G` — Green apple  
- `R` — Red apple  
- `0` — Empty cell  

⚠️ The agent must **only** use this limited vision as input.

#### Actions

The agent can choose exactly one of:

- `UP`
- `LEFT`
- `DOWN`
- `RIGHT`

No other information about the board is allowed.

#### Rewards (suggested approach)

You are free to design your reward function. A typical setup:

- ✅ Eat green apple → positive reward  
- ❌ Eat red apple → negative reward  
- ➖ Move without eating → small negative reward  
- 💀 Game over → large negative reward  

These rewards drive the Q-learning updates.

---

## 📈 Learning Method

The agent use **Q-learning**:

Core concepts implemented:

- Iterative learning over many sessions
- Exploration vs exploitation (e.g., ε-greedy)
- Q-function updates after every action
- Ability to:
  - **Save** models (Q-values / network weights)
  - **Load** models
  - Run in **evaluation mode** (`dontlearn`) where learning is disabled

During heavy training, graphics and terminal output can be disabled for speed.

---

## ⚙️ Command-Line Arguments

The program accepts several command-line options to control training, visualization, model persistence, and board size.

### Available Arguments

| Argument      | Type | Default | Description |
|--------------|------|---------|-------------|
| `-sessions`  | int  | `100`   | Number of training sessions (episodes) to run. |
| `-save`      | str  | `None`  | Path where the trained Q-table / model will be saved after training. |
| `-visual`    | flag | `False` | Enable graphical visualization during execution. |
| `-dontlearn` | flag | `False` | Disable learning. The agent will act using the loaded model without updating Q-values (evaluation mode). |
| `-load`      | str  | `None`  | Path to a previously trained model to load. |
| `-size`      | int  | `10`    | Size of the square game board (default: 10 creates a 10×10 board). |

Flags (`-visual`, `-dontlearn`) do not take values — their presence alone enables the option.

---

## 🚀 Usage

### Train a new model

```bash
./snake -sessions 10 -save models/10sess.txt

Game over, max length = 4, max duration = 17
Save learning state in models/10sess.txt
```

### Run with a trained model (no learning)
./snake -visual -load models/100sess.txt -sessions 10 -dontlearn

### Pure evaluation
./snake -visual -load models/1000sess.txt