import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def calc_coord(radius, theta):
	theta = theta * math.pi / 180.0
	x = radius * math.cos(theta)
	y = radius * math.sin(theta)
	coord = [x, y]

	return coord

def make_coord_df(result):
	df = pd.DataFrame(result, columns=['x', 'y'])
	
	return df
 
def plot_coord(r, df):
	plt.figure(figsize=(5, 5))
	plt.xlim(-r*2, r*2)
	plt.ylim(-r*2, r*2)
	plt.plot(df['x'], df['y'], marker='*', linewidth=0)
	plt.show()

if __name__ == "__main__":
	r = 1
	n = 4
	n_angle = int(360 / n)

	result = []

	for this in range(0, 360, n_angle):
		coord = calc_coord(r, this)
		result.append(coord)

	df = make_coord_df(result)
	print(df)
	plot_coord(r, df)





