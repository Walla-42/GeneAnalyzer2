
class Sequence:
    """
    An abstract base class for all sequence type data. All sequences should inherit from this class.
    """

    def __init__(self, sequence):
        self.seq = sequence


class DNA(Sequence):
    pass

class RNA(Sequence):
    pass

class Protein(Sequence):

    def addPeptide(self, peptide):
        self.seq += peptide

    