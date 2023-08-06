from Bio import SeqIO
import re
from collections import Counter, defaultdict
from ahocorasick import Automaton
from peptide_matcher.utils import parse_cigar, parse_hexscores

class PeptideMatcher:
    """The main class for peptide matching.
    Initilize as: PeptideMatcher(peptides, fasta, sst_included, flanks) where
    peptides is an iterable containing peptide sequences as individual items,
    fasta is a file name or file handle with the protein database,
    sst_included is a boolean indicating whether the database contains structural
    information and flanks is the flank length for the matches.
    
    The method PeptideMatcher.run() yields dict output for every input peptide.
    """
    def __init__(self, peptides, fasta, sst_included, flanks = 4):
        self.fasta = fasta
        self.sst_included = sst_included
        self.peptides = peptides
        self.flanks = flanks
        self.flanks_range = list(range(flanks))
        self.flanks_revrange = list(reversed(range(flanks)))
        self.sst_re   = re.compile('secstruct:([^\s]+)')
        self.acc_re   = re.compile('accessibility:([^\s]+)')
        self.conf_re  = re.compile('confidence:([^\s]+)')
        self.tm_re    = re.compile('transmembrane:([^\s]+)')

    def parse_peptides(self):
        self.automaton = Automaton()
        self.peptide_seqs = []
        for line in self.peptides:
           peptide = line.rstrip().upper()
           assert re.match('[ACDEFGHIKLMNPQRSTVWY]+$', peptide), "Malformed peptide string '%s'" % peptide
           self.automaton.add_word(peptide, peptide)
           self.peptide_seqs.append(peptide)
        assert len(self.automaton) > 0, "The peptide list seems empty"
        self.automaton.make_automaton()

    def run(self):
        self.parse_peptides()
        data = defaultdict(list)
        for record in SeqIO.parse(self.fasta, 'fasta'):
            record_seq = str(record.seq)
            seq_len = len(record_seq)
            if self.sst_included:
                match_sst  = self.sst_re.search(record.description)
                match_tm   = self.tm_re.search(record.description)
                match_acc  = self.acc_re.search(record.description)
                match_conf = self.conf_re.search(record.description)
                sst  = parse_cigar(match_sst.group(1))     if match_sst  else ''
                tm   = parse_cigar(match_tm.group(1))      if match_tm   else ''
                acc  = parse_hexscores(match_acc.group(1))  if match_acc  else []
                conf = parse_hexscores(match_conf.group(1)) if match_conf else []
            else:
                sst = tm = acc = conf = None
            for end_index, peptide in self.automaton.iter(record_seq):
                start_index = end_index - len(peptide) + 1
                start = start_index + 1
                end = end_index + 1
                to_c_term = seq_len - end
                if start_index > self.flanks:
                    n_term = record_seq[start_index - self.flanks:start_index]
                else:
                    n_term = '[' + record_seq[0:start_index]
                if to_c_term > self.flanks:
                    c_term = record_seq[end:end + self.flanks]
                else:
                    c_term = record_seq[end:] + ']'

                if sst:
                    sst_pept = sst[start_index:end]
                    if start_index > self.flanks:
                        sst_n_term = sst[start_index - self.flanks:start_index]
                    else:
                        sst_n_term = '[' + sst[0:start_index]
                    if to_c_term > self.flanks:
                        sst_c_term = sst[end:end + self.flanks]
                    else:
                        sst_c_term = sst[end:] + ']'
                else:
                    sst_pept = sst_n_term = sst_c_term = ''

                if tm:
                    tm_pept = tm[start_index:end]
                    if start_index > self.flanks:
                        tm_n_term = tm[start_index - self.flanks:start_index]
                    else:
                        tm_n_term = '[' + tm[0:start_index]
                    if to_c_term > self.flanks:
                        tm_c_term = tm[end:end + self.flanks]
                    else:
                        tm_c_term = tm[end:] + ']'
                else:
                    tm_pept = tm_n_term = tm_c_term = ''

                if acc:
                    acc_pept = acc[start_index:end]
                    if start_index > self.flanks:
                        acc_n_term = acc[start_index - self.flanks:start_index]
                    else:
                        acc_n_term = [ '[' ] + acc[0:start_index]
                    if to_c_term > self.flanks:
                        acc_c_term = acc[end:end + self.flanks]
                    else:
                        acc_c_term = acc[end:] + [ ']' ]
                else:
                    acc_pept = acc_n_term = acc_c_term = []
                if conf:
                    conf_pept = conf[start_index:end]
                    if start_index > self.flanks:
                        conf_n_term = conf[start_index - self.flanks:start_index]
                    else:
                        conf_n_term = [ '[' ] + conf[0:start_index]
                    if to_c_term > self.flanks:
                        conf_c_term = conf[end:end + self.flanks]
                    else:
                        conf_c_term = conf[end:] + [ ']' ]
                else:
                    conf_pept = conf_n_term = conf_c_term = []
                data[peptide].append((record.id, start, end, n_term, c_term, to_c_term, sst_n_term, sst_pept, sst_c_term, tm_n_term, tm_pept, tm_c_term, conf_n_term, conf_pept, conf_c_term, acc_n_term, acc_pept, acc_c_term))
        for peptide in self.peptide_seqs:
            peplen = len(peptide)
            matches = []
            n_logos = []
            c_logos = []
            if peptide in data:
                all_n_terms = []
                all_c_terms = []
                for i in range(self.flanks):
                    all_n_terms.append([])
                    all_c_terms.append([])
                data_peptide = data[peptide]
                for record_id, start, end, n_term, c_term, to_c_term, *struct_info in data_peptide:

                    offset = self.flanks - len(n_term)

                    for i in self.flanks_revrange:
                        let = n_term[i - offset]
                        all_n_terms[i].append(let)
                        if let == '[': break
                    for i in self.flanks_range:
                        let = c_term[i]
                        all_c_terms[i].append(let)
                        if let == ']': break
                    match = {
                        'record_id': record_id,
                        'start': start,
                        'end': end,
                        'c_term': to_c_term + 1,
                        'n_flank': str(n_term),
                        'c_flank': str(c_term)
                    }
                    if self.sst_included:
                        match['sst_n_term'], match['sst_pept'], match['sst_c_term'], match['tm_n_term'], match['tm_pept'], \
                        match['tm_c_term'], match['conf_n_term'], match['conf_pept'], match['conf_c_term'], match['acc_n_term'], match['acc_pept'], match['acc_c_term'] \
                            = struct_info
                    matches.append(match)

                for pos in all_n_terms:
                    logo = dict(Counter(pos))
                    n_logos.append(logo)

                for pos in all_c_terms:
                    logo = dict(Counter(pos))
                    c_logos.append(logo)

            yield { 'peptide': peptide, 'matches': matches, 'n_logos': n_logos, 'c_logos': c_logos }
