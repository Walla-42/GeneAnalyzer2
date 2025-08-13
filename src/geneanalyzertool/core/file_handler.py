from Bio import SeqIO

class FileHandler():
    """A class that handles file operations for the GeneAnalyzer2 tool."""

    def __init__(self):
        pass

    def file_support_check(self, file):
        while True:
            if file[-4:] == '.fna' or file[-6:] == '.fasta':
                print('\033[1;33m' + 'Opening and parsing file...' + '\033[0m')
                break

            else:
                print('\033[1;31m' + "file type not supported. Please select a .fna or .fasta file to read." + '\033[0m')

        for record in SeqIO.parse(file, 'fasta'):
            print(f"Description: {record.description}")

    def read_in_sequence(self, fasta_file):    

        """User guided sequence that parses a .fna or .fasta file according to how the user would like it analyzed. """

        self.file_support_check(fasta_file)

        while True:
            select = input('Which sequence would you like to analyze? if all type "all". ' + "\n" + ">>> ")
            match_found = False
            sequence_dictionary = {}
            sequence_keys = []

            if select.strip().lower() == "all":
                for record in SeqIO.parse(fasta_file, 'fasta'):
                    sequence_dictionary[record.id] = record.seq
                    sequence_keys.append(record.id)
                break

            else:
                for record in SeqIO.parse(fasta_file, 'fasta'):
                    if select in record.description:
                        sequence_dictionary[record.id] = record.seq
                        sequence_keys.append(record.id)
                        match_found =True

                        print(f"ID: {record.id}")
                        print(f"Name: {record.name}")
                        print(f"Description: {record.description}")
                        print(f"Length: {len(record.seq)}")
                        break

            if match_found:
                break

            else:
                print('\033[1;31m' + "No matching records found. Please select a valid record." + '\033[0m')
                
        return sequence_dictionary, sequence_keys

    