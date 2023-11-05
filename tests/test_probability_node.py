from probability_node import Node
from unittest import TestCase


class TestNode(TestCase):
    def test_end_node_null(self):
        node = Node()
        res = node.get_expected_value()
        self.assertEqual(0., res)

    def test_end_node_not_null(self):
        node = Node(probability=0.25, value=2)
        res = node.get_expected_value()
        self.assertEqual(.5, res)

    def test_node_two_levels(self):
        root = Node()
        root.add_child(Node(probability=.75, value=1))
        root.add_child(Node(probability=.25, value=-1))

        actual = root.get_expected_value()
        expected = 0.75 * 1 + -1*.25
        self.assertEqual(actual, expected)

    def test_node_three_levels(self):
        root = Node()
        root.add_child(Node())
        root.children[0].add_child(Node(probability=.25, value=1))
        root.children[0].add_child(Node(probability=.25, value=2))
        root.add_child(Node(probability=.5, value=3))

        actual = root.get_expected_value()
        expected = 0.25 * 1 + .25*2 + .5*3
        self.assertEqual(actual, expected)

    def test_node_end_node_probability(self):
        node = Node(probability=.33, value=1)
        self.assertEqual(node.probability, .33)

    def test_node_probability_two_levels(self):
        root = Node()
        root.add_child(Node(probability=.75, value=1))
        root.add_child(Node(probability=.25, value=-1))

        actual = root.get_probability()
        expected = 1
        self.assertEqual(actual, expected)
