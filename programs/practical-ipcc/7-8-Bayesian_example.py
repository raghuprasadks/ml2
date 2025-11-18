#https://vtupulse.com/machine-learning/bayesian-network-in-python-using-pgmpy/
import numpy as np
import pandas as pd
import csv 
from pgmpy.estimators import MaximumLikelihoodEstimator
ModelClass = None
try:
	from pgmpy.models import DiscreteBayesianNetwork
	ModelClass = DiscreteBayesianNetwork
except Exception:
	try:
		from pgmpy.models import BayesianModel
		ModelClass = BayesianModel
	except Exception:
		try:
			from pgmpy.models import BayesianNetwork
			ModelClass = BayesianNetwork
		except Exception:
			raise ImportError(
				"pgmpy does not expose a recognized Bayesian network class. "
				"Please install a compatible pgmpy version.")
from pgmpy.inference import VariableElimination

heartDisease = pd.read_csv('7-dataset.csv')
heartDisease = heartDisease.replace('?',np.nan)

print('Sample instances from the dataset are given below')
print(heartDisease.head())

print('\n Attributes and datatypes')
print(heartDisease.dtypes)

model= ModelClass([('age','heartdisease'),('gender','heartdisease'),('exang','heartdisease'),('cp','heartdisease'),('heartdisease','restecg'),('heartdisease','chol')])
print('\nLearning CPD using Maximum likelihood estimators')
model.fit(heartDisease,estimator=MaximumLikelihoodEstimator)

print('\n Inferencing with Bayesian Network:')
HeartDiseasetest_infer = VariableElimination(model)

print('\n 1. Probability of HeartDisease given evidence= restecg')
q1=HeartDiseasetest_infer.query(variables=['heartdisease'],evidence={'restecg':1})
print(q1)

print('\n 2. Probability of HeartDisease given evidence= cp ')
q2=HeartDiseasetest_infer.query(variables=['heartdisease'],evidence={'cp':2})
print(q2)