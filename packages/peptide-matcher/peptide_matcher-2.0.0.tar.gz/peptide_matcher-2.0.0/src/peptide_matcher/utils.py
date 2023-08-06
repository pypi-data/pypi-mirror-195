import re

cigar_re = re.compile('(\d+)(.)')

def parse_hexscores(encoded):
    """Parse strings of concatenated 2-digit hexadecimal ints into a list of integers
    """
    return [ int(encoded[i:i+2], 16) for i in range(0, len(encoded), 2) ]

def parse_cigar(encoded):
    """Uncompress strings in CIGAR-like compression: <int><char><int><char>... where the integers
    show the number of times the characters appear consecutively.
    Returns an uncompress string <char><char><char><char><char>...
    """
    s = ''
    for num, char in cigar_re.findall(encoded):
        s += char * int(num)
    return s

def wrap_logos(logos):
    """Wrap logos <int><char><int><char>...|<int><char><int><char>...|... where the integers
    show the number of times the chars (amino acids) appear at every position
    """
    logo_strs = []
    for logo in logos:
        counts = [ str(count) + aa for aa, count in logo.items() ]
        logo_strs.append(''.join(counts))
    return '|'.join(logo_strs)

def wrap_scores(scores):
    """Wrap a list of of integer scores as a comma-separated string
    """
    return ','.join(map(str, scores))

