# Monopoly

**Monopoly** is a simplified, terminal-based reimplementation of the classic board game, written in Python using the [Textual](https://github.com/Textualize/textual) library. Roll dice, buy “computer components” instead of properties, pay rent, draw Chance/Risk cards, and aim to bankrupt your opponent or collect a full set of components.

---

## Table of Contents

1. [Project Overview](#project-overview)  
2. [Requirements](#requirements)  
3. [Installation](#installation)  
4. [Running the Game](#running-the-game)  
5. [How to Play](#how-to-play)  
6. [Game Rules](#game-rules)  
7. [Repository Structure](#repository-structure)  
8. [Contributing](#contributing)  
9. [License](#license)  

---

## Project Overview

- Built with [Textual](https://github.com/Textualize/textual) to run entirely in your terminal.  
- Two players take turns rolling dice and moving around a board of 22 fields.  
- Instead of classic properties you buy “computer components”: Network Card, RAM, GPU, HDD, CPU.  
- Special fields include:
  - **Start**: Collect \$200 each time you pass.  
  - **Chance**: Draw a random event card.  
  - **Risk**: Face a random gamble.  
  - **Neostrada**: Choose how many spaces (1–16) to move.  

---

## Requirements

- Python 3.8 or higher  
- Dependencies listed in `requirements.txt`:
  ```bash
  textual=3.4.0
  ```

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/karol157/monopoly.git
   cd monopoly
   ```

2. (Optional) Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\Scripts\activate      # Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

---

## Running the Game

Start the game with:

```bash
python main.py
```

A Textual interface will launch in your terminal, displaying the board, dice panel, and sidebar with player info.

---

## How to Play

1. **Rolling the Dice**

   * Press **Enter** (or select “Roll the dice”) in the bottom panel.
   * The dice result and your new position will appear.

2. **Purchasing or Passing**

   * Landing on a purchasable field shows **Buy** and **Pass** buttons in the sidebar.

     * **Buy**: Pay the field price and add it to your assets.
     * **Pass**: Skip buying; the next player may still purchase this field later.

3. **Special Fields**

   * **Start**: Receive \$200 each time you pass from position 16 back to 1.
   * **Chance** & **Risk**: Draw a random card that may move you, adjust your money, or skip turns.
   * **Neostrada**: Enter a number (1–16) to move manually.

4. **Paying Rent**

   * If you land on an opponent’s owned component, pay the displayed rent.
   * Owning multiple of the same type doubles the rent.

5. **Ending the Game**
   The game ends when either:

   * A player goes bankrupt (has zero or negative cash), or
   * A player collects one of each of the five component types:

     1. Network Card
     2. RAM
     3. GPU
     4. HDD
     5. CPU

---

## Repository Structure

```
monopoly/
├── game/  
│   ├── board.py           # Main Textual app and board logic  
│   ├── field.py           # Field (property) definitions  
│   ├── player/  
│   │   ├── model.py       # Player UI widget  
│   │   └── player.py      # Player class (state, cash, position)  
│   ├── dice.py            # Dice widget and turn queue  
│   ├── thing_info.py      # Field info panel + Buy/Pass + event handling  
│   ├── chance_and_risk.py # Chance and Risk card definitions  
│   ├── number_input.py    # Manual-move screen (Neostrada / cards)  
│   └── win.py             # Victory / endgame screen  
├── src/                   # Textual CSS style sheets  
├── main.py                # Entry point to launch the game  
└── requirements.txt       # Python dependencies  
```
