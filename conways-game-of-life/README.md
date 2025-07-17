# Conway's Game of Life

A Go implementation of Conway's Game of Life cellular automaton, built using Test-Driven Development (TDD).

## About

Conway's Game of Life is a cellular automaton devised by mathematician John Horton Conway. It consists of a grid of cells that evolve through generations based on simple rules:

1. Any live cell with 2 or 3 live neighbors survives
2. Any dead cell with exactly 3 live neighbors becomes alive
3. All other live cells die, and all other dead cells stay dead

## Running the Program

```bash
# Build and run with board size and number of generations
go build
./conways-game-of-life <board_size> <generations>

# Or run directly
go run game.go <board_size> <generations>

# Example: 8x8 board for 5 generations
go run game.go 8 5
```

The program creates a square board of the specified size with randomly populated cells (30% probability of a cell being alive) and runs for the specified number of generations. The simulation will exit early if the board stabilizes (oscillates between two states).

## Running Tests

```bash
go test
```

## Implementation

The implementation includes:
- `cellNextState()` - Determines a cell's next state based on current state and neighbor count
- `countNeighbors()` - Counts live neighbors for a given cell position
- `nextGeneration()` - Computes the next generation of the entire grid
- `printGrid()` - Displays the grid using block characters
- `gridsEqual()` - Compares two grids for equality to detect stabilization
- `createGrid()` - Creates a square grid with a blinker pattern
- `createRandomGrid()` - Creates a square grid with randomly populated cells

The program automatically detects when the board has stabilized (oscillating between two states) and exits early to avoid boring repetitive output.

The code was developed using TDD principles, with tests written first to define the expected behavior.