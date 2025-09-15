from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple, Iterable, Optional

from .tables import TABLE, AA2CODONS, PREFERRED_CODON


ALLOWED_DNA = set("ACGT")


@dataclass
class CodonChange:
    index: int
    raw_codon: str
    new_codon: str
    raw_aa: str
    target_aa: str
    aa_changed: bool
    distance: int
    diff_positions: List[int]
    decision: str


def difference(s1: str, s2: str) -> int:
    """Return Hamming distance between two equal-length strings."""
    if len(s1) != len(s2):
        raise ValueError("difference() requires equal-length strings")
    return sum(a != b for a, b in zip(s1, s2))


def _diff_positions(s1: str, s2: str) -> List[int]:
    return [i for i, (a, b) in enumerate(zip(s1, s2)) if a != b]


def _validate_inputs(mut_aa: str, dna: str) -> None:
    if len(dna) % 3 != 0:
        raise ValueError("DNA length must be a multiple of 3")
    if len(mut_aa) != len(dna) // 3:
        raise ValueError("mut_aa length must equal DNA codon count")
    up_dna = dna.upper()
    if any(base not in ALLOWED_DNA for base in up_dna):
        bad = {b for b in up_dna if b not in ALLOWED_DNA}
        raise ValueError(f"DNA contains invalid bases: {sorted(bad)}")
    if any((TABLE.get(up_dna[i:i+3]) is None) for i in range(0, len(up_dna), 3)):
        raise ValueError("DNA contains invalid codons for the standard genetic code")
    up_aa = mut_aa.upper()
    if any(aa not in AA2CODONS for aa in up_aa):
        bad = {aa for aa in up_aa if aa not in AA2CODONS}
        raise ValueError(f"mut_aa contains invalid symbols: {sorted(bad)}")


def dna2aa(dna: str) -> str:
    """Translate DNA (length % 3 == 0) into amino acids using the standard genetic code."""
    if len(dna) % 3 != 0:
        raise ValueError("DNA length must be a multiple of 3")
    dna = dna.upper()
    return "".join(TABLE[dna[i:i + 3]] for i in range(0, len(dna), 3))


def _choose_codon(
    target_aa: str,
    ref_codon: str,
    tie_break: str = "wobble",
) -> Tuple[str, str, int, List[int]]:
    """Choose a codon for target_aa minimizing distance to ref_codon.

    Returns (chosen_codon, decision, distance, diff_positions)
    decision in {"same", "min_distance", "tie_break_wobble", "tie_break_freq", "tie_break_lex"}
    """
    # If the ref codon already encodes the target aa, keep it.
    if TABLE[ref_codon] == target_aa:
        return ref_codon, "same", 0, []

    candidates = AA2CODONS[target_aa]
    distances = [difference(c, ref_codon) for c in candidates]
    min_d = min(distances)
    tied = [c for c, d in zip(candidates, distances) if d == min_d]

    if len(tied) == 1:
        c = tied[0]
        return c, "min_distance", min_d, _diff_positions(c, ref_codon)

    # Tie-break strategies
    if tie_break == "wobble":
        # Prefer changes only at the third position (index 2) if present
        wobble_only = [c for c in tied if _diff_positions(c, ref_codon) == [2]]
        if wobble_only:
            c = wobble_only[0]
            return c, "tie_break_wobble", 1, [2]
        # Fall through to frequency preference
        pref = PREFERRED_CODON.get(target_aa)
        if pref in tied:
            return pref, "tie_break_freq", min_d, _diff_positions(pref, ref_codon)
        # Deterministic fallback
        tied.sort()
        c = tied[0]
        return c, "tie_break_lex", min_d, _diff_positions(c, ref_codon)

    elif tie_break == "freq":
        pref = PREFERRED_CODON.get(target_aa)
        if pref in tied:
            return pref, "tie_break_freq", min_d, _diff_positions(pref, ref_codon)
        tied.sort()
        c = tied[0]
        return c, "tie_break_lex", min_d, _diff_positions(c, ref_codon)

    else:
        # Unknown tie_break: deterministic lexicographic
        tied.sort()
        c = tied[0]
        return c, "tie_break_lex", min_d, _diff_positions(c, ref_codon)


def recode_by_aa_min_changes(
    mut_aa: str,
    dna: str,
    *,
    tie_break: str = "wobble",
    forbid_internal_stop: bool = True,
) -> Tuple[str, List[CodonChange]]:
    """Recode DNA so its translation matches mut_aa with minimal nucleotide changes.

    Parameters
    - mut_aa: target amino-acid sequence ("_" for stop), length equals DNA codon count
    - dna: original DNA sequence (A/T/G/C), length multiple of 3
    - tie_break: strategy used when multiple codons have the same minimal distance
                 ("wobble" | "freq")
    - forbid_internal_stop: if True, raises when mut_aa has stop not at final position

    Returns
    - new_dna: recoded DNA string
    - report: list of per-codon CodonChange entries
    """
    # Normalize inputs
    dna = dna.upper()
    mut_aa = mut_aa.upper().replace("*", "_")
    _validate_inputs(mut_aa, dna)

    if forbid_internal_stop and "_" in mut_aa[:-1]:
        raise ValueError("Internal stop codon in mut_aa is forbidden")

    report: List[CodonChange] = []
    new_codons: List[str] = []

    for i in range(0, len(dna), 3):
        idx = i // 3
        ref_codon = dna[i:i + 3]
        raw_aa = TABLE[ref_codon]
        target_aa = mut_aa[idx]

        chosen, decision, dist, diffs = _choose_codon(target_aa, ref_codon, tie_break)

        new_codons.append(chosen)
        report.append(CodonChange(
            index=idx,
            raw_codon=ref_codon,
            new_codon=chosen,
            raw_aa=raw_aa,
            target_aa=target_aa,
            aa_changed=(raw_aa != target_aa),
            distance=dist,
            diff_positions=diffs,
            decision=decision,
        ))

    return "".join(new_codons), report


# Backward-compatible names
def run_translate(mut_seq: str, raw_dna: str) -> str:
    """Backward-compatible wrapper returning only the recoded DNA string."""
    new_dna, _ = recode_by_aa_min_changes(mut_seq, raw_dna)
    return new_dna
