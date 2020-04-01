import os

# tensorflow CPU 관련 경고 메시지 무시
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split

class shallow_NN():
	def __init__(self):
		self.data_A = pd.read_csv("data_A.csv", names=["data_A_x", "data_A_y"])
		self.data_B = pd.read_csv("data_B.csv", names=["data_B_x", "data_B_y", "speed"])
	
	
	def print_message(self, msg):
		print("=" * 65)
		print(msg)
		print("=" * 65)

	def train_test_split(self):
		idx = np.random.choice(len(self.data_A), 200)
		train_idx = self.data_A.index.isin(idx.tolist())

		self.X_train = self.data_B[train_idx]
		self.y_train = self.data_A[train_idx]

		self.X_test  = self.data_B[~train_idx]
		self.y_test  = self.data_A[~train_idx]

	def nn_model(self, lr=0.001, decay=1e-5):
		print("Make shallow NN")
		nn_model = Sequential()
		nn_model.add(Dense(100, input_dim=3, kernel_initializer='normal', activation='relu'))
		nn_model.add(Dense(200, activation='relu'))
		nn_model.add(Dense(50, activation='relu'))
		nn_model.add(Dense(25, activation='relu'))
		nn_model.add(Dense(2, activation='linear'))

		print(nn_model.summary())

		# MAPE
		nn_model.compile(loss="mean_absolute_percentage_error", optimizer=Adam(lr, decay))
		# nn_model.compile(loss="mse", optimizer=Adam(lr, decay))

		return nn_model

	def run(self):
		self.train_test_split()
		model = self.nn_model()

		self.print_message("Model Training ... ")

		result = model.fit(
			self.X_train, self.y_train,
			epochs=5000,
			batch_size=300,
			verbose=0
		)

		preds = model.predict(self.X_test)
		MAPE = tf.keras.losses.MAPE(self.y_test.to_numpy(), preds)

		# showing results
		
		print("Prediction")
		print("="*65)

		print("True data_A coord")
		print(self.y_test.to_numpy()[:5])

		print("Predicted data_A coord")
		print(preds[:5])

		print(f"MAPE: {np.mean(MAPE)}")

if __name__ == "__main__":
	my_NN = shallow_NN()
	my_NN.run()