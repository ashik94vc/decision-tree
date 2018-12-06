from pandas import DataFrame
from ds import Tree

class DecisionTree(object):

    def __init__(self, dataframe, label_column):
        self.dataset = dataframe
        self.label_index = label_column
        self.decision_tree = None
        self.label_column = self.dataset[label_column]

    def __get__(self, instance, group):
        return self.decision_tree

    def get_labels(self):
        labels = dict()
        for row in self.label_column:
            if not row in labels:
                labels[row] = 0
        return labels.values()

    def create_groups(self, attribute_index, value):
        groups = {0: DataFrame(), 1: DataFrame()}
        for _,row in self.dataset.iterrows():
            if row[attribute_index] < value:
                groups[0] = groups[0].append(row)
            else:
                groups[1] = groups[1].append(row)
        return groups.values()

    def gini_index(self, attribute_index, value=None):
        groups = self.create_groups(attribute_index, value)
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

        return gini_index,groups

    def get_best_attribute(self, attributes):
        best_score = 1000
        best_attribute = -1
        best_split = None
        for attribute in attributes:
            for value in self.dataset[attribute].values:
                gini,groups = self.gini_index(attribute,value)
                if gini < best_score:
                    best_score = gini
                    best_attribute = attribute
                    best_split = groups
        return best_attribute,groups

    def build_tree(self, tree, attributes):
        attribute, groups = self.get_best_attribute(attributes)
        attribute_categories = list(self.dataset[attribute].unique())
        for cat in attribute_categories:
            tree.addChild(Tree(attribute=attribute, value=cat))
        attributes = attributes.remove(attribute)
        for child in tree.getChildren():
            child_gini = self.gini_index(child.attribute)
            if self.gini_index(child.attribute) > 0:
                self.build_tree(child, attributes)
        return True

    def train(self):
        attributes = list(self.dataset.columns.values)
        attributes.remove(self.label_index)
        tree = Tree()
        self.build_tree(tree, attributes)
        self.decision_tree = tree

    def eval_row(self, row, tree):
        if tree.isLeafNode():
            return tree.value
        for child in tree.getChildren():
            if child.value == row[child.attribute]:
                tree = child
                return self.eval_row(row, tree)
        return False

    def predict(self, row):
        tree = self.decision_tree
        output = self.eval_row(row)
        if not output:
            raise ValueError("Input not correct")
        return output
    
    def test(self, test_data):
        test_data = test_data.rename(columns={self.label_index: 'target'})
        target_frame = test_data['target']
        test_data.drop('target', inplace=True)
        for _,row in test_data.iterrows():
            tree = self.decision_tree
            output = self.eval_row(row, tree)
            if not output:
                raise ValueError("Input not correct")
            target_frame.loc[len(target_frame), 'output'] = output
        total = len(target_frame)
        correct = 0
        for _,row in target_frame.iterrows():
            if row.target == row.output:
                correct += 1
        accuracy = 100.*(correct/total)
        return accuracy