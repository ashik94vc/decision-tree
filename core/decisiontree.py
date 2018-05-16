from pandas import DataFrame
from ds.tree import Tree

class DecisionTree(object):

    def __init__(self, dataframe, label_column):
        self.dataset = dataframe
        self.label_index = label_column
        self.label_column = self.dataset[label_column]

    def get_labels(self):
        labels = dict()
        for row in self.label_column:
            if not row in labels:
                labels[row] = 0
        return labels.values()

    def create_groups(self, attribute_index, value=None, dtype="nominal"):
        if dtype == "nominal":
            values = dict()
            groups = dict()
            for row in self.dataset.iterrows():
                if not row[attribute_index] in values:
                    values[row[attribute_index]] = len(values)
                    groups[values[row[attribute_index]]] = DataFrame()
                groups[values[row[attribute_index]]] = groups[values[row[attribute_index]]].append(row)
            return groups.values()
        else:
            groups = {0: DataFrame(), 1: DataFrame()}
            for row in self.dataset.iterrows():
                if row[attribute_index] < value:
                    groups[0] = groups[0].append(row)
                else:
                    groups[1] = groups[1].append(row)
            return groups.values()

    def gini_index(self, attribute_index):
        groups = self.create_groups(attribute_index)
        total_enries = len(self.dataset)
        labels = self.get_labels()
        gini_index = 0
        for group in groups:
            group_gini = len(group)/len(self.dataset)
            group_gini_score = 1
            prob_df = group[self.label_index].value_counts()
            for label in labels:
                group_gini_score -= prob_df[label]**2
            group_gini = group_gini*group_gini_score
            gini_index += group_gini

        return gini_index

    def get_best_attribute(self, attributes):
        best_score = 1000
        best_attribute = -1
        for attribute in attributes:
            gini = self.gini_index(attribute)
            if gini < best_score:
                best_score = gini
                best_attribute = attribute
        return best_attribute

    def train():
        attributes = list(self.dataset.columns.values)
        attributes.remove(self.label_index)
        tree = Tree()
