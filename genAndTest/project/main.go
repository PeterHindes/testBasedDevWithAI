
package main

func reduceBrightness(color int, reduction float64) int {
	r := (color >> 16) & 0xFF
	g := (color >> 8) & 0xFF
	b := color & 0xFF
	r = int(float64(r) * (1 - reduction))
	g = int(float64(g) * (1 - reduction))
	b = int(float64(b) * (1 - reduction))
	return (r << 16) | (g << 8) | b
}

func changeHue(color int, shift float64) int {
	r := (color >> 16) & 0xFF
	g := (color >> 8) & 0xFF
	b := color & 0xFF
	h := hue(r, g, b)
	h = (h + 360*shift) % 360
	r, g, b = rgbFromHue(h, float64(r)/255, float64(g)/255, float64(b)/255)
	return (int(r*255) << 16) | (int(g*255) << 8) | int(b*255)
}

func hue(r, g, b int) float64 {
	max := maxInt(r, g, b)
	min := minInt(r, g, b)
	if max == min {
		return 0
	}
	var h float64
	switch max {
	case r:
		h = 60 * (float64(g-b) / (max - min))
	case g:
		h = 60 * (float64(b-r) / (max - min) + 2)
	case b:
		h = 60 * (float64(r-g) / (max - min) + 4)
	}
	if h < 0 {
		h += 360
	}
	return h
}

func rgbFromHue(h, r, g, b float64) (float64, float64, float64) {
	c := maxFloat(r, g, b) - minFloat(r, g, b)
	x := c * (1 - absFloat(h/60-1))
	m := maxFloat(r, g, b) - c
	switch int(h / 60) {
	case 0:
		return c + m, x + m, m
	case 1:
		return x + m, c + m, m
	case 2:
		return m, c + m, x + m
	case 3:
		return m, x + m, c + m
	case 4:
		return x + m, m, c + m
	case 5:
		return c + m, m, x + m
	default:
		return r, g, b
	}
}

func maxFloat(a, b, c float64) float64 {
	if a > b {
		if a > c {
			return a
		}
		return c
	}
	if b > c {
		return b
	}
	return c
}

func minFloat(a, b, c float64) float64 {
	if a < b {
		if a < c {
			return a
		}
		return c
	}
	if b < c {
		return b
	}
	return c
}

func absFloat(a float64) float64 {
	if a < 0 {
		return -a
	}
	return a
}

func maxInt(a, b, c int) int {
	if a > b {
		if a > c {
			return a
		}
		return c
	}
	if b > c {
		return b
	}
	return c
}

func minInt(a, b, c int) int {
	if a < b {
		if a < c {
			return a
		}
		return c
	}
	if b < c {
		return b
	}
	return c
}
