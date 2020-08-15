cdef extern from "math.h":
	double sin(double)

cdef double f(double x) except *:
	return sin(x**2)

def integrate(double a, double b, int N):
	cdef int i
	cdef double dx, s = 0
	dx = (b-a)/N
	for i in range(N):
		s += f(a+i*dx)
	return s*dx
