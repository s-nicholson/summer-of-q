package main

import (
	"reflect"
	"testing"
)

func TestCellNextState(t *testing.T) {
	tests := []struct {
		name      string
		alive     bool
		neighbors int
		expected  bool
	}{
		{"dead cell with 3 neighbors becomes alive", false, 3, true},
		{"live cell with 2 neighbors stays alive", true, 2, true},
		{"live cell with 3 neighbors stays alive", true, 3, true},
		{"live cell with 1 neighbor dies", true, 1, false},
		{"live cell with 4 neighbors dies", true, 4, false},
		{"dead cell with 2 neighbors stays dead", false, 2, false},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := cellNextState(tt.alive, tt.neighbors)
			if result != tt.expected {
				t.Errorf("cellNextState(%v, %d) = %v, want %v", tt.alive, tt.neighbors, result, tt.expected)
			}
		})
	}
}

func TestCountNeighbors(t *testing.T) {
	grid := [][]bool{
		{true, false, true},
		{false, true, false},
		{true, false, true},
	}

	tests := []struct {
		name     string
		x, y     int
		expected int
	}{
		{"center cell has 4 neighbors", 1, 1, 4},
		{"corner cell has 1 neighbor", 0, 0, 1},
		{"edge cell has 3 neighbors", 1, 0, 3},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := countNeighbors(grid, tt.x, tt.y)
			if result != tt.expected {
				t.Errorf("countNeighbors(grid, %d, %d) = %d, want %d", tt.x, tt.y, result, tt.expected)
			}
		})
	}
}

func TestNextGeneration(t *testing.T) {
	current := [][]bool{
		{false, true, false},
		{false, true, false},
		{false, true, false},
	}

	expected := [][]bool{
		{false, false, false},
		{true, true, true},
		{false, false, false},
	}

	result := nextGeneration(current)
	if !reflect.DeepEqual(result, expected) {
		t.Errorf("nextGeneration() = %v, want %v", result, expected)
	}
}

func TestCreateGrid(t *testing.T) {
	grid := createGrid(3)
	if len(grid) != 3 {
		t.Errorf("createGrid(3) height = %d, want 3", len(grid))
	}
	if len(grid[0]) != 3 {
		t.Errorf("createGrid(3) width = %d, want 3", len(grid[0]))
	}
	// Check center cell is alive (blinker pattern)
	if !grid[1][1] {
		t.Error("createGrid(3) center cell should be alive")
	}
}