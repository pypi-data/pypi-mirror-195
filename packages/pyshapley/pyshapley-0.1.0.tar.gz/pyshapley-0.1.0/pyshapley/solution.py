import itertools
import math
import random

from . import export
from .game import CoalitionalGame
from .util import RandomSubsetGenerator


def marginal_coalitions(player, order):
    """

    :param player:
    :type player: str
    :param order:
    :type order: list
    :return:
    :rtype (set, set)
    """
    pos_player = order.index(player)
    return set(order[:pos_player]), set(order[: pos_player + 1])


def marginal_contribution_order(game, player, order):
    """

    :param player:
    :type player: str
    :param order:
    :type order: list
    :return:
    """
    c1, c2 = marginal_coalitions(
        player, order
    )  # e.g. p='a', o=['c', 'b', 'a', 'd'] => c1 = ['c', 'b'] c2 = ['c', 'b', 'a']
    # TODO How to deal with negative payoff? How to deal with negative marginal contributions?
    # return max(0,self.payoff(c2)) - max(0,self.payoff(c1))
    # print('c1 = %s, c2 = %s' % (c1, c2))
    return marginal_contribution_set(game, player, c1)


def marginal_contribution_set(game, player, lower_set):
    """
    Takes a subset of players and a player, transforms them into a higher set c2 and lower set c1 and calculates
     their marginal contribution based on the implemented payoff function.

    :param player: An element of self.players
    :type player: str
    :param lower_set: A subset of self.players of which player should be no part.
    :type lower_set: set
    :return:
    """
    lower_set = set(lower_set)
    try:
        higher_set = lower_set | {player}
    except TypeError:
        raise ValueError("Given set could not be joined with player %s" % player)
    marginal_contribution = max(0, game.payoff(higher_set)) - max(0, game.payoff(lower_set))
    return marginal_contribution


@export
class Shapley(object):
    def __init__(self, game: CoalitionalGame):
        self._game = game

    def shapley(self, player):
        if player not in self._game.players:
            raise ValueError("No such player in game: %s" % player)
        marginals = 0.0
        for order in itertools.permutations(self._game.players):  # e.g. ['c', 'b', 'a']
            marginals += marginal_contribution_order(self._game, player, order)
        return marginals / self._game.number_player_permutations

    def approx_shapley(self, player, samples):
        return self.approx_shapley_with_subsets(player, samples)

    def approx_shapley_with_permutations(self, player, samples: int):
        """
        Original Shapley value approximation based on random sampling of permutations of players.

        :param player:
        :param samples:
        :return:
        """
        # For n < 5 we have only up to 4! = 24 permutations, so return full pyshapley
        # which is computational feasible and needs no approximation
        if len(self._game.players) < 5:
            return self.shapley(player)
        currentOrder = list(self._game.players)
        marginals = []
        for _ in range(samples):
            # Each sample is a random order from which we take marginal coalitions
            # Thus orders could be repeatedly used. This is avoided for large game sizes as the number of samples
            # will be proportional very low.
            random.shuffle(currentOrder)
            marginals.append(marginal_contribution_order(self._game, player, currentOrder))
        return sum(marginals) / samples

    def approx_shapley_with_subsets(self, player, samples):
        """
        Shapley approximation based on random sampling of subsets of players.

        :param player:
        :param samples:
        :return:
        """
        if len(self._game.players) < 5:
            return self.shapley(player)

        weights = []
        marginals = []
        for subset in RandomSubsetGenerator(samples=samples, full_set=self._game.players, except_set={player}):
            marginal_contribution = marginal_contribution_set(self._game, player, subset)
            weight = math.factorial(len(subset)) * math.factorial(len(self._game.players) - len(subset) - 1)
            weights.append(weight)
            marginals.append(marginal_contribution)
        return sum([w * m for (w, m) in zip(weights, marginals)]) / sum(weights)
