
class Sequence(str):
    """
    An abstract base class for all sequence type data. All sequences should inherit from this class.
    """
    def __new__(cls, sequence):
        return super().__new__(cls, sequence)


class DNA(Sequence):
    pass


class RNA(Sequence):
    pass


class Protein(Sequence):
    pass
