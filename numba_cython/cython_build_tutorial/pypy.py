import math

def f(x):
	return math.sin(x**2)

def integrate(a, b, N):
	s = 0.0
	dx = (b-a)/N
	for i in range(N):
		s += f(a+i*dx)
	return s*dx