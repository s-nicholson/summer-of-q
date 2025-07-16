# Conway's Game of Life

A Go implementation of Conway's Game of Life cellular automaton, built using Test-Driven Development (TDD).

## About

Conway's Game of Life is a cellular automaton devised by mathematician John Horton Conway. It consists of a grid of cells that evolve through generations based on simple rules:

1. Any live cell with 2 or 3 live neighbors survives
2. Any dead cell with exactly 3 live neighbors becomes alive
3. All other live cells die, and all other dead cells stay dead

## Running the Program

```bash
# Build and run
go build
./conways-game-of-life

# Or run directly
go run game.go
```

The program displays 10 generations of a simple oscillator pattern (blinker).

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

The code was developed using TDD principles, with tests written first to define the expected behavior.