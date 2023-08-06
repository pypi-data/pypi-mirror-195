import logging
import os
import pickle
from random import choice

import pandas as pd

from delab_trees.constants import TREE_IDENTIFIER
from delab_trees.delab_tree import DelabTree
from delab_trees.preperation_alg_pb import prepare_pb_data
from delab_trees.preperation_alg_rb import prepare_rb_data
from delab_trees.training_alg_pb import train_pb
from delab_trees.training_alg_rb import train_rb

logger = logging.getLogger(__name__)


class TreeManager:

    def __init__(self, df, n=None):
        self.trees = {}
        self.df = df
        self.__initialize_trees(n)

    def __initialize_trees(self, n=None):
        """
        internal method to extract the portion of the pandas dataframe that belongs to one tree and initialize the
        networkx graph for that reply tree
        :param n:
        :return:
        """
        grouped_by_tree_ids = {k: v for k, v in self.df.groupby(TREE_IDENTIFIER)}
        counter = 0
        tree_ids_picked=[]
        for tree_id, df in grouped_by_tree_ids.items():
            counter += 1
            if n is not None and counter > n:
                break
            tree = DelabTree(df)
            self.trees[tree_id] = tree
            tree_ids_picked.append(tree_id)
        self.df = self.df[self.df["tree_id"].isin(tree_ids_picked)]
        return self

    def single(self) -> DelabTree:
        """
        if the manager holds only one tree the latter is returned
        :return:
        """
        assert len(self.trees.keys()) == 1, "There needs to be exactly one tree in the manager!"
        return self.trees[self.trees.keys()[0]]

    def random(self) -> DelabTree:
        """
        if the manager holds any tree, a random tree is returned
        :return:
        """
        assert len(self.trees.keys()) >= 1
        return self.trees[choice(list(self.trees.keys()))]

    def __prepare_rb_model(self, prepared_data_filepath, prepare_data=True):
        """
        convert the trees to a matrix with all the node pairs (node -> ancestor) in order run the RB
        algorithm that wagers a prediction whether a post has been seen by a subsequent post's author

        """
        if prepare_data:
            rb_prepared_data = prepare_rb_data(self)
            rb_prepared_data.to_pickle(prepared_data_filepath)
        else:
            with open("pb_prepared_data.pkl", 'rb') as f:
                rb_prepared_data = pickle.load(f)
        return rb_prepared_data

    def __train_apply_rb_model(self, prepared_data_filepath="rb_prepared_data.pkl", prepare_data=True) \
            -> dict['tree_id', dict['author_id', 'rb_vision']]:
        """
        internal method to prepare the training data for the rb algorithm
        :param prepared_data_filepath:
        :param prepare_data:
        :return:
        """
        if prepare_data:
            data = self.__prepare_rb_model(prepared_data_filepath)
        else:
            with open("rb_prepared_data.pkl", 'rb') as f:
                data = pickle.load(f)
        assert data.empty is False, "There was a mistake during the preparation of the data for the rb algorithm"
        applied_model, trained_model, features = train_rb(data)
        result = applied_model.pivot(columns='conversation_id', index='author', values="predictions").to_dict()
        return result

    def get_rb_vision(self, tree: DelabTree = None, prepare_data=True):
        """
        :param prepare_data: if False the previously rb_prepared_data.pkl is used
        :param tree: DelabTree
        :return: -> dict['tree_id', dict['author_id', 'rb_vision'] - a measure for how likely it is that a given author
                                                                     has seen a random tweet in a conversation.
                                                                     If a tree is given only the inner dict is returned!
        """
        applied_rb_model = self.__train_apply_rb_model(prepare_data=prepare_data)
        if tree is None:
            return applied_rb_model
        else:
            return applied_rb_model[tree.conversation_id]

    def __prepare_pb_model(self, prepared_data_filepath):
        """
        internal method to prepare the data for training for the rb_vision algorithm
        :param prepared_data_filepath:
        :return:
        """
        rb_prepared_data = prepare_pb_data(self)
        rb_prepared_data.to_pickle(prepared_data_filepath)
        return rb_prepared_data

    def __train_apply_pb_model(self, prepared_data_filepath="pb_prepared_data.pkl", prepare_data=True) \
            -> dict['tree_id', dict['author_id', 'pb_vision']]:
        """
        internal method to prepare the data for training the pb_vision algorithm
        :param prepared_data_filepath:
        :param prepare_data:
        :return:
        """
        if prepare_data:
            data = self.__prepare_pb_model(prepared_data_filepath)
        else:
            with open("pb_prepared_data.pkl", 'rb') as f:
                data = pickle.load(f)
        assert data.empty is False, "There was a mistake during the preparation of the data for the pb algorithm"
        applied_model = train_pb(data)

        result = applied_model.pivot(columns='conversation_id', index='author', values="predictions").to_dict()
        return result

    def get_pb_vision(self, tree: DelabTree = None, prepare_data=True):
        """
        :param prepare_data:
        :param tree: DelabTree
        :return: r:float - multilabel classification computing the likelihood of a given author would answer
                           given a random tweet.
        """
        applied_pb_model = self.__train_apply_pb_model(prepare_data=prepare_data)
        if tree is None:
            return applied_pb_model
        else:
            return applied_pb_model[tree.conversation_id]


def get_test_tree() -> DelabTree:
    """
    :return: r:DelabTree - a self written example tree
    """

    d = {'tree_id': [1] * 4,
         'post_id': [1, 2, 3, 4],
         'parent_id': [None, 1, 2, 1],
         'author_id': ["james", "mark", "steven", "john"],
         'text': ["I am James", "I am Mark", " I am Steven", "I am John"],
         "created_at": [pd.Timestamp('2017-01-01T01'),
                        pd.Timestamp('2017-01-01T02'),
                        pd.Timestamp('2017-01-01T03'),
                        pd.Timestamp('2017-01-01T04')]}
    df = pd.DataFrame(data=d)
    manager = TreeManager(df)
    # creates one tree
    test_tree = manager.random()
    return test_tree


def get_test_manager() -> TreeManager:
    d = {'tree_id': [1] * 4,
         'post_id': [1, 2, 3, 4],
         'parent_id': [None, 1, 2, 1],
         'author_id': ["james", "mark", "steven", "john"],
         'text': ["I am James", "I am Mark", " I am Steven", "I am John"],
         "created_at": [pd.Timestamp('2017-01-01T01'),
                        pd.Timestamp('2017-01-01T02'),
                        pd.Timestamp('2017-01-01T03'),
                        pd.Timestamp('2017-01-01T04')]}
    d2 = d.copy()
    d2["tree_id"] = [2] * 4
    d2['parent_id'] = [None, 1, 2, 3]
    d3 = d.copy()
    d3["tree_id"] = [3] * 4
    d3['parent_id'] = [None, 1, 1, 1]
    # a case where an author answers himself
    d4 = d.copy()
    d4["tree_id"] = [4] * 4
    d4["author_id"] = ["james", "james", "james", "john"]

    d5 = d.copy()
    d5["tree_id"] = [5] * 4
    d5['parent_id'] = [None, 1, 2, 3]
    d5["author_id"] = ["james", "james", "james", "john"]

    df1 = pd.DataFrame(data=d)
    df2 = pd.DataFrame(data=d2)
    df3 = pd.DataFrame(data=d3)
    df4 = pd.DataFrame(data=d4)
    df5 = pd.DataFrame(data=d5)
    df_list = [df1, df2, df3, df4, df5]
    df = pd.concat(df_list, ignore_index=True)
    manager = TreeManager(df)
    return manager


def get_social_media_trees(platform="twitter", n=None, context="production"):
    assert platform == "twitter" or platform == "reddit", "platform needs to be reddit or twitter!"
    if context == "test":
        file = "../delab_trees/data/dataset_twitter_no_text.pkl"
        # file = "/home/dehne/PycharmProjects/delab/scriptspy/dataset_twitter_no_text.pkl"
    else:
        this_dir, this_filename = os.path.split(__file__)
        file = os.path.join(this_dir, 'data/dataset_twitter_no_text.pkl')
    file = file.replace("reddit", platform)
    df = pd.read_pickle(file)
    manager = TreeManager(df, n)
    return manager
