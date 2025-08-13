from geneanalyzertool.analysis.analysis import Analysis
from geneanalyzertool.core.sequences import *
from typing import Any, override

class BasicSequenceAnalysis(Analysis):
    """
    Class for basic analysis performed on dna, rna or protein sequences

    """

    @override
    def analyze(self, sequence: Sequence, method: str) -> Any:
        """
        executes simple analysis of protein, RNA or DNA sequences.
        """
        method_dispatch = {
            "gc_percent": self._gc_percent,
            "base_count": self._base_count,
            "translate": self._translate,
            "transcribe": self._transcribe,
            "reverse_complement": self._reverse_complement
        }

        if method not in method_dispatch:
            raise ValueError(f"Uknown mehtod {method}")
        
        return method_dispatch[method](sequence)


    def _gc_percent(self, sequence: DNA | RNA) -> float:
        """
        Calculates the percent Guanine and Cytosine that are present in a DNA or RNA Molecule.
        Sequence must be of type RNA or DNA. 
        """
        if not isinstance(sequence, (DNA, RNA)):
            raise TypeError("Error: Sequence must be of type DNA or RNA")
        
        gc_count = sequence.upper().count("G") + sequence.upper().count("C")
        return (gc_count/len(sequence))*100
        
    
    def _base_count(self, sequence) -> dict:
        """
        Counts the number of each base in a DNA sequence.
        Sequence provided must be of type DNA or RNA.
        """
        base_counts = {
            'A': sequence.upper().count('A'),
            'T': sequence.upper().count('T'),
            'G': sequence.upper().count('G'),
            'C': sequence.upper().count('C')
        }

        return base_counts
    
    def _translate(self, sequence) -> Protein:
        """
        Translates a given RNA sequence into a predicted protein sequence minus
        post tranlational modificaitons. Sequnce provided must be of type RNA. 
        """
        peptide_table = {
            "UUU": "F", "UUC": "F", "UUA": "L", "UUG": "L",
             "UCU": "S", "UCC": "S", "UCA": "S", "UCG": "S",
             "UAU": "Y", "UAC": "Y", "UAA": "STOP", "UAG": "STOP",
             "UGU": "C", "UGC": "C", "UGA": "STOP", "UGG": "W",
             "CUU": "L", "CUC": "L", "CUA": "L", "CUG": "L",
             "CCU": "P", "CCC": "P", "CCA": "P", "CCG": "P",
             "CAU": "H", "CAC": "H", "CAA": "Q", "CAG": "Q",
             "CGU": "R", "CGC": "R", "CGA": "R", "CGG": "R",
             "AUU": "I", "AUC": "I", "AUA": "I", "AUG": "M",
             "ACU": "T", "ACC": "T", "ACA": "T", "ACG": "T",
             "AAU": "N", "AAC": "N", "AAA": "K", "AAG": "K",
             "AGU": "S", "AGC": "S", "AGA": "R", "AGG": "R",
             "GUU": "V", "GUC": "V", "GUA": "V", "GUG": "V",
             "GCU": "A", "GCC": "A", "GCA": "A", "GCG": "A",
             "GAU": "D", "GAC": "D", "GAA": "E", "GAG": "E",
             "GGU": "G", "GGC": "G", "GGA": "G", "GGG": "G", 
             }
        
        if not isinstance(sequence, RNA):
            raise TypeError("Error: Sequence must be of type RNA.")
        
        
        protein_seq = ""
        
        for i in range(0, len(sequence), 3):
            codon = sequence[i:i+3]
            if peptide_table.get(codon) == "STOP":
                protein_seq += "*"
                break
            
            if (peptide := peptide_table.get(codon)) is None:
                protein_seq += "X"
            else:
                protein_seq += peptide

        return Protein(protein_seq)
    
    def _transcribe(self, sequence: DNA) -> RNA:
        """
        Transcribes a given DNA sequence into an RNA sequence.
        Sequence provided must be of type DNA.
        """
        if not isinstance(sequence, DNA):
            raise TypeError("Error: Sequence must be of type DNA")
        
        rna_sequence = sequence.replace("T", "U")
        return RNA(rna_sequence)
    
    def _reverse_complement(self, sequence: DNA | RNA) -> DNA | RNA:
        """
        Returns the reverse complement of a given DNA sequence.
        Sequence provided must be of type DNA.
        """
        if not isinstance(sequence, (DNA, RNA)):
            raise TypeError("Error: Sequence must be of type DNA or RNA")
        
        if isinstance(sequence, DNA):
            reverse_complement = sequence.translate(str.maketrans("ATGCatgc", "TACGtacg"))[::-1]
            return DNA(reverse_complement)
        
        if isinstance(sequence, RNA):
            reverse_complement = sequence.translate(str.maketrans("AUGCaugc", "UACGuacg"))[::-1]
            return RNA(reverse_complement)
