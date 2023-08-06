import unittest

from delab_trees.delab_tree import DelabTree
from delab_trees.main import get_social_media_trees


class RBAlgorithmsTestCase(unittest.TestCase):

    def setUp(self):
        self.manager = get_social_media_trees(n=10)

    def test_load_trees(self):
        assert len(self.manager.trees) == 10

    def test_rb_algorithm(self):
        tree: DelabTree = self.manager.random()
        rb_vision = self.manager.get_rb_vision(tree)
        assert rb_vision.popitem()[1] > 0

