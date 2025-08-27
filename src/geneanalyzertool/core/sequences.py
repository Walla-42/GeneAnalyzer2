
class Sequence(str):
    """
    An abstract base class for all sequence type data. All sequences should inherit from this class.
    
    This class extends Python's built-in str class to provide a foundation for
    biological sequence types (DNA, RNA, Protein).
    
    Args:
        sequence (str): The sequence string data
        
    Returns:
        Sequence: A new sequence instance
    """
    def __new__(cls, sequence):
        return super().__new__(cls, sequence)


class DNA(Sequence):
    """
    DNA sequence class for representing deoxyribonucleic acid sequences.
    
    Inherits from Sequence base class and is used specifically for DNA sequence data.
    Expected to contain nucleotides A, T, G, C.
    """
    pass


class RNA(Sequence):
    """
    RNA sequence class for representing ribonucleic acid sequences.
    
    Inherits from Sequence base class and is used specifically for RNA sequence data.
    Expected to contain nucleotides A, U, G, C.
    """
    pass


class Protein(Sequence):
    """
    Protein sequence class for representing amino acid sequences.
    
    Inherits from Sequence base class and is used specifically for protein sequence data.
    Expected to contain standard amino acid letters.
    """
    pass
