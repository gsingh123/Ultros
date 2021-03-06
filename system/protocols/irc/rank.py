__author__ = 'Sean'

from system.translations import Translations
_ = Translations().get()


class Rank(object):
    """
    A user rank in a channel.
    We're all consenting adults here: don't change the properties after
    creation please, or tentacles will go the wrong way.

    Note: A higher order means a lower rank, and vice-versa. This class
    overrides certain operators, and does so in terms of rank, not order.
    i.e. Rank("o","@","2") > Rank("v","+","5") == True
    """
    def __init__(self, mode, symbol, order):
        self.mode = mode
        self.symbol = symbol
        self.order = order

    def __str__(self):
        return "%s%s%s" % (self.mode, self.symbol, self.order)

    def __lt__(self, other):
        if isinstance(other, Rank):
            other = other.order
        return self.order > other

    def __gt__(self, other):
        if isinstance(other, Rank):
            other = other.order
        return self.order < other

    def __le__(self, other):
        if isinstance(other, Rank):
            other = other.order
        return self.order >= other

    def __ge__(self, other):
        if isinstance(other, Rank):
            other = other.order
        return self.order <= other

    def __eq__(self, other):
        if isinstance(other, Rank):
            other = other.order
        return self.order == other

    def __ne__(self, other):
        if isinstance(other, Rank):
            other = other.order
        return self.order != other


class Ranks(object):
    def __init__(self):
        self._ranks_by_mode = {}
        self._ranks_by_symbol = {}
        self._ranks_by_order = {}

    def add_rank(self, rank_or_mode, symbol=None, order=None):
        if not isinstance(rank_or_mode, Rank):
            if symbol is None or order is None:
                raise ValueError(_("First argument must be of type Rank or "
                                   "all arguments must be given"))
            else:
                rank_or_mode = Rank(rank_or_mode, symbol, order)
        self._ranks_by_mode[rank_or_mode.mode] = rank_or_mode
        self._ranks_by_symbol[rank_or_mode.symbol] = rank_or_mode
        self._ranks_by_order[rank_or_mode.order] = rank_or_mode

    @property
    def modes(self):
        return self._ranks_by_mode.keys()

    @property
    def symbols(self):
        return self._ranks_by_symbol.keys()

    @property
    def orders(self):
        return self._ranks_by_order.keys()

    def by_mode(self, mode):
        if mode in self._ranks_by_mode:
            return self._ranks_by_mode[mode]
        return None

    def by_symbol(self, symbol):
        if symbol in self._ranks_by_symbol:
            return self._ranks_by_symbol[symbol]
        return None

    def by_order(self, order):
        if order in self._ranks_by_order:
            return self._ranks_by_order[order]
        return None

    def is_op(self, rank, or_above=True):
        op = self.by_mode("o")
        if or_above:
            return rank >= op
        else:
            return rank == op

    def is_hop(self, rank, or_above=True):
        hop = self.by_mode("h")
        if hop is None:
            # Half-op isn't necessarily on every IRCd, but op is in the RFC
            self.by_mode("o")
        if or_above:
            return rank >= hop
        else:
            return rank == hop

    def is_voice(self, rank, or_above=True):
        voice = self.by_mode("v")
        if or_above:
            return rank >= voice
        else:
            return rank == voice
