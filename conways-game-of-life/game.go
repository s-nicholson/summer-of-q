package main

import (
	"fmt"
	"os"
	"strconv"
	"time"
)

func cellNextState(alive bool, neighbors int) bool {
	if neighbors == 3 {
		return true
	}
	if alive && neighbors == 2 {
		return true
	}
	return false
}

func countNeighbors(grid [][]bool, x, y int) int {
	count := 0
	height, width := len(grid), len(grid[0])

	for dx := -1; dx <= 1; dx++ {
		for dy := -1; dy <= 1; dy++ {
			if dx == 0 && dy == 0 {
				continue
			}
			nx, ny := x+dx, y+dy
			if nx >= 0 && nx < height && ny >= 0 && ny < width && grid[nx][ny] {
				count++
			}
		}
	}
	return count
}

func nextGeneration(grid [][]bool) [][]bool {
	height, width := len(grid), len(grid[0])
	next := make([][]bool, height)
	for i := range next {
		next[i] = make([]bool, width)
	}

	for x := 0; x < height; x++ {
		for y := 0; y < width; y++ {
			neighbors := countNeighbors(grid, x, y)
			next[x][y] = cellNextState(grid[x][y], neighbors)
		}
	}
	return next
}

func printGrid(grid [][]bool) {
	for _, row := range grid {
		for _, cell := range row {
			if cell {
				fmt.Print("█")
			} else {
				fmt.Print(" ")
			}
		}
		fmt.Println()
	}
}

func createGrid(size int) [][]bool {
	grid := make([][]bool, size)
	for i := range grid {
		grid[i] = make([]bool, size)
	}
	// Create blinker pattern in center
	center := size / 2
	if center > 0 && center < size-1 {
		grid[center-1][center] = true
		grid[center][center] = true
		grid[center+1][center] = true
	}
	return grid
}

func gridsEqual(a, b [][]bool) bool {
	if len(a) != len(b) {
		return false
	}
	for i := range a {
		if len(a[i]) != len(b[i]) {
			return false
		}
		for j := range a[i] {
			if a[i][j] != b[i][j] {
				return false
			}
		}
	}
	return true
}

func main() {
	if len(os.Args) != 3 {
		fmt.Println("Usage: go run game.go <board_size> <generations>")
		os.Exit(1)
	}

	size, err := strconv.Atoi(os.Args[1])
	if err != nil || size < 3 {
		fmt.Println("Board size must be a number >= 3")
		os.Exit(1)
	}

	gens, err := strconv.Atoi(os.Args[2])
	if err != nil || gens < 1 {
		fmt.Println("Generations must be a number >= 1")
		os.Exit(1)
	}

	grid := createGrid(size)
	var prev1, prev2 [][]bool

	for i := 0; i < gens; i++ {
		fmt.Printf("Generation %d:\n", i)
		printGrid(grid)
		fmt.Println()

		// Check for stabilization (oscillation between 2 states)
		if prev2 != nil && gridsEqual(grid, prev2) {
			fmt.Println("Board stabilized - exiting early")
			break
		}

		prev2 = prev1
		prev1 = grid
		grid = nextGeneration(grid)
		time.Sleep(500 * time.Millisecond)
	}
}