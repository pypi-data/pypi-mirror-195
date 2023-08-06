import math


class CoalitionalGame(object):
    """
    Basic interface and implementation for a pyshapley game. Inherit from this class and implement a specific payoff
    function, then use game.pyshapley() or game.approx_shapley() for your computation of a pyshapley value for a specific
    player.

    Interface usage:
    ```python
    game = XyzShapley(players=[1,2,3,4,5,6])
    s4 = game.approx_shapley(4) # approximate pyshapley value for player 4
    ```
    """

    _players = {}  # Access via Shapley#players and Shapley#set_players
    _permutations = None  # Access via Shapley#number_of_permutations
    _lower_bound = None  # Access via Shapley#lower_bound
    _deviation = None  # Access via Shapley#deviation

    def __init__(self, players):
        self.players = players

    @property
    def players(self):
        """

        :return:
        :rtype set
        """
        return self._players

    @players.setter
    def players(self, players):
        """

        :param players:
        :type players set
        :return:
        """
        self._permutations = None
        self._lower_bound = None
        self._deviation = None
        self._players = set(players)

    @property
    def lower_bound(self):
        if self._lower_bound is None:
            self._lower_bound = self.payoff_raw(set())
        return self._lower_bound

    @property
    def number_player_permutations(self):
        """

        :return:
        :rtype: float
        """
        if self._permutations is None:
            self._permutations = math.factorial(len(self._players))
        return self._permutations

    def payoff(self, coalition):
        """
        Returns the corrected payoff value (payoff reduced by lower bound) of the given coalition based on the
        payoff_raw()-implementation.

        :param coalition: Subset of players (coalition) of which the payoff shall be computed.
        :type coalition set
        :return: Contribution value / payoff value for the given coalition.
        :rtype: float
        """
        return self.payoff_raw(coalition) - self.lower_bound

    def payoff_raw(self, coalition):
        """

        :param coalition: Subset of players (coalition) of which the payoff shall be computed.
        :type coalition set
        :return:
        """
        raise NotImplementedError("You should implement this in your pyshapley-calculation class.")


class ManualDictGame(CoalitionalGame):
    def __init__(self, players, payoff_dict):
        super().__init__(players)
        self._payoff_dict = payoff_dict

    def payoff(self, coalition):
        key = "".join(sorted(coalition))
        if key not in self._payoff_dict:
            if len(key) < 1:
                raise ValueError('No payoff defined for empty set (key = "")')
            else:
                raise ValueError('No payoff defined for "%s"' % key)
        return self._payoff_dict[key]


class GeneralCouncilGame(CoalitionalGame):
    _phi_temp = None
    _phi_perm = None

    def __init__(self, players, numberPermanentMembers, affirmativeCount):
        super().__init__(players)
        if isinstance(players, set):
            players = list(players)
        assert numberPermanentMembers < len(players)
        assert affirmativeCount > 0 and affirmativeCount < len(players)
        self._permanents = players[0:numberPermanentMembers]
        self._affirmativeCount = affirmativeCount

    def payoff(self, coalition):
        if len(coalition) < self._affirmativeCount or not all(x in coalition for x in self._permanents):
            return 0
        return 1

    def shapley(self, player):
        if player in self._permanents:
            return self._shapley_permanent_member()
        else:
            return self._shapley_temporary_member()

    def _shapley_temporary_member(self):
        """

        :return:
        :rtype : float
        """
        if self._phi_temp is None:
            # s = self._affirmativeCount
            # n = len(self.players)
            # 5 = len(self._permanents)
            # [(s!)/((s-5-1)!(n-s)!)] * [((s-1)!(n-s)!)/(n!)]
            self._phi_temp = (
                math.factorial(self._affirmativeCount)
                / (
                    math.factorial(self._affirmativeCount - len(self._permanents) - 1)
                    * math.factorial(len(self.players) - self._affirmativeCount)
                )
                * (
                    (
                        math.factorial(self._affirmativeCount - 1)
                        * math.factorial(len(self.players) - self._affirmativeCount)
                    )
                    / math.factorial(len(self.players))
                )
            )
        return self._phi_temp

    def _shapley_permanent_member(self):
        """

        :return:
        :rtype : float
        """
        if self._phi_perm is None:
            self._phi_perm = (1 - 10 * self._shapley_temporary_member()) / len(self._permanents)
        return self._phi_perm
