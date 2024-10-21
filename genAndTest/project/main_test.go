package main

import "testing"

// equal checks if two boolean slices are equal
func equal(a, b []bool) bool {
	if len(a) != len(b) {
		return false
	}
	for i := range a {
		if a[i] != b[i] {
			return false
		}
	}
	return true
}

func TestReduceBrightness(t *testing.T) {
	// Test case 1
	input := 0x3af06b; // int
	reduction := 0.5 // float64
	expected := 0x1d7835 // int
	output := reduceBrightness(input, reduction)
	if output != expected {
		t.Errorf("Expected %v but got %v", expected, output)
	}
}

func TestChangeHue(t *testing.T) {
	// Test case 1
	input := 0x771d1d; // int
	shift := 0.5 // float64 // percent of full hue shift
	expected := 0x1d7878 // int
	output := changeHue(input, shift)
	if output != expected {
		t.Errorf("Expected %v but got %v", expected, output)
	}
}