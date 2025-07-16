package main

import (
	"fmt"
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

func main() {
	grid := [][]bool{
		{false, false, false, false, false},
		{false, false, true, false, false},
		{false, false, true, false, false},
		{false, false, true, false, false},
		{false, false, false, false, false},
	}

	for i := 0; i < 10; i++ {
		fmt.Printf("Generation %d:\n", i)
		printGrid(grid)
		fmt.Println()
		grid = nextGeneration(grid)
		time.Sleep(500 * time.Millisecond)
	}
}