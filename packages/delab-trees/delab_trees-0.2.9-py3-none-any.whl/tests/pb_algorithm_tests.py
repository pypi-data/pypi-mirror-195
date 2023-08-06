import unittest

from delab_trees.delab_tree import DelabTree
from delab_trees.main import get_social_media_trees


class PBAlgorithmsTestCase(unittest.TestCase):

    def setUp(self):
        self.manager = get_social_media_trees(n=10, platform="reddit")

    def test_load_trees(self):
        assert len(self.manager.trees) == 10

    def test_pb_algorithm(self):
        tree: DelabTree = self.manager.trees.popitem()[1]
        pb_vision = self.manager.get_pb_vision(tree, prepare_data=False)
        assert pb_vision.popitem()[1] > 0
