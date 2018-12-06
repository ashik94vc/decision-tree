import argparse
import pandas
import numpy as np
import time
from pandas import DataFrame
from pptree import print_tree

from core import DecisionTree

parser = argparse.ArgumentParser(description="Decision Tree Classifier")
parser.add_argument('dataset')
parser.add_argument('label')
parser.add_argument('--criterion',default="gini")
args = parser.parse_args()

dataset = args.dataset

dataframe = pandas.read_csv(dataset, header=None)
label = int(args.label)
criterion = args.criterion
dataframe = dataframe.sample(frac=1)
mask = np.arange(len(dataframe)) < 0.8*len(dataframe)

train_data = dataframe[mask]
test_data = dataframe[~mask]

train_outputs = train_data[label]
train_data = train_data.drop(label, axis=1)
train_inputs = train_data
test_outputs = test_data[label]
test_data = test_data.drop(label, axis=1)
test_inputs = test_data
print("Using {0} criterion".format(criterion))
start = time.time()
decision_tree = DecisionTree(criterion=criterion)
decision_tree.train(train_inputs, train_outputs)
score = decision_tree.score(test_inputs, test_outputs)
end = time.time()
print(end - start)
print(score*100)
data = [[12, 20, 30]]
print(decision_tree.predict(data))
# decision_tree.train()
