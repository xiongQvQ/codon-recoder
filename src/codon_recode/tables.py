from typing import Dict, List

# Standard genetic code: DNA codon -> amino acid ("_" for stop)
TABLE: Dict[str, str] = {
    'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M',
    'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
    'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K',
    'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',
    'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L',
    'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
    'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q',
    'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
    'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V',
    'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
    'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E',
    'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
    'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S',
    'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
    'TAC':'Y', 'TAT':'Y', 'TAA':'_', 'TAG':'_',
    'TGC':'C', 'TGT':'C', 'TGA':'_', 'TGG':'W',
}

# Amino acid -> list of synonymous codons
AA2CODONS: Dict[str, List[str]] = {
    'I': ['ATA', 'ATC', 'ATT'],
    'M': ['ATG'],
    'T': ['ACA', 'ACC', 'ACG', 'ACT'],
    'N': ['AAC', 'AAT'],
    'K': ['AAA', 'AAG'],
    'S': ['AGC', 'AGT', 'TCA', 'TCC', 'TCG', 'TCT'],
    'R': ['AGA', 'AGG', 'CGA', 'CGC', 'CGG', 'CGT'],
    'L': ['CTA', 'CTC', 'CTG', 'CTT', 'TTA', 'TTG'],
    'P': ['CCA', 'CCC', 'CCG', 'CCT'],
    'H': ['CAC', 'CAT'],
    'Q': ['CAA', 'CAG'],
    'V': ['GTA', 'GTC', 'GTG', 'GTT'],
    'A': ['GCA', 'GCC', 'GCG', 'GCT'],
    'D': ['GAC', 'GAT'],
    'E': ['GAA', 'GAG'],
    'G': ['GGA', 'GGC', 'GGG', 'GGT'],
    'F': ['TTC', 'TTT'],
    'Y': ['TAC', 'TAT'],
    '_': ['TAA', 'TAG', 'TGA'],
    'C': ['TGC', 'TGT'],
    'W': ['TGG'],
}

# Preferred codon per amino acid, used as a deterministic tie-break fallback
PREFERRED_CODON: Dict[str, str] = {
    '_': 'TAA', 'A': 'GCG', 'C': 'TGC', 'D': 'GAT', 'E': 'GAA', 'F': 'TTT',
    'G': 'GGC', 'H': 'CAT', 'I': 'ATT', 'K': 'AAA', 'L': 'CTG', 'M': 'ATG',
    'N': 'AAC', 'P': 'CCG', 'Q': 'CAG', 'R': 'CGT', 'S': 'AGC', 'T': 'ACC',
    'V': 'GTG', 'W': 'TGG', 'Y': 'TAT'
}
