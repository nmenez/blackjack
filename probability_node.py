class Node:
    def __init__(self, children=None,
                 probability=0,
                 value=0):

        self.children = children if children is not None else []
        self.probability = probability
        self.value = value

    def add_child(self, child):
        self.children.append(child)

    def get_expected_value(self):
        if len(self.children) == 0:
            return self.probability * self.value
        else:
            return sum(child.get_expected_value() for child in self.children)

    def get_probability(self):
        if len(self.children) == 0:
            return self.probability

        else:
            return sum(child.probability for child in self.children)


