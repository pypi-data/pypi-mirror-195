import random

from . import export


@export
class SubsetGenerator(object):
    _full_set = ()

    @property
    def full_set(self):
        return self._full_set

    @full_set.setter
    def full_set(self, full_set):
        if full_set is None:
            raise ValueError("Given set might not be None.")
        self._full_set = full_set

    def __iter__(self):
        return self

    def __next__(self):
        # Python 3 compatibility
        return self.next()

    def next(self):
        raise StopIteration("Not implemented.")


@export
class RandomSubsetGenerator(SubsetGenerator):
    def __init__(self, samples, full_set=None, except_set=None):
        self.samples = samples
        self._current_sample = 0
        self._except_set = {}

        if full_set is not None:
            self.full_set = full_set
        if except_set is not None:
            self.except_set = except_set

    @property
    def full_set(self):
        return set(self._element_list)

    @full_set.setter
    def full_set(self, full_set):
        if full_set is None:
            raise ValueError("Given set might not be None.")
        # Force set to be a list, so we can access it in fixed order as long as it is not changed
        self._element_list = list(full_set)
        self._index_except_set()

    @property
    def samples(self):
        return self._samples

    @property
    def except_set(self):
        return self._except_set

    @except_set.setter
    def except_set(self, except_set):
        self._except_set = except_set
        self._index_except_set()

    def _index_except_set(self):
        if self._except_set is not None and self._element_list is not None:
            self._except_set_indices = set(
                self._element_list.index(el) for el in self._except_set if el in self._element_list
            )
        else:
            self._except_set_indices = set()

    @samples.setter
    def samples(self, samples):
        self._samples = int(samples)

    def next(self):
        """

        :return:
        :rtype set
        """
        if self._element_list is None:
            raise StopIteration()

        if self._current_sample < self._samples:
            set_size = len(self._element_list)
            random_subset_code = random.randint(0, (2**set_size) - 1)
            self._current_sample += 1
            return set(
                self._element_list[i]
                for i in range(set_size)
                if random_subset_code & (2**i) > 0 and i not in self._except_set_indices
            )
        else:
            self._current_sample = 0  # reset counter, so we can reuse the object
            raise StopIteration()  # make sure we don't get an infinite loop
