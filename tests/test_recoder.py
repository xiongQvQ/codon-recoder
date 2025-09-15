import pytest

from codon_recode import recode_by_aa_min_changes, dna2aa, run_translate


def test_identity_no_change():
    dna = "ATGAAAACG"  # M K T
    aa = "MKT"
    new_dna, report = recode_by_aa_min_changes(aa, dna)
    assert new_dna == dna
    assert dna2aa(new_dna) == aa
    assert sum(r.distance for r in report) == 0


def test_single_change_min_distance():
    dna = "ATGAAAACG"  # M K T
    # Change K -> N at second codon (AAA -> AAC minimal change by 1 nt at 3rd pos)
    aa = "MNT"
    new_dna, report = recode_by_aa_min_changes(aa, dna)
    assert new_dna[:3] == "ATG"
    assert new_dna[3:6] in {"AAC", "AAT"}
    assert dna2aa(new_dna) == aa
    # Ensure we made exactly one nucleotide change at the middle codon
    assert sum(r.distance for r in report) == 1


def test_back_compat_run_translate():
    dna = "ATGAAAACG"  # M K T
    aa = "MNT"
    out = run_translate(aa, dna)
    assert isinstance(out, str)
    assert dna2aa(out) == aa


def test_validation_errors():
    with pytest.raises(ValueError):
        recode_by_aa_min_changes("MK", "ATGAAAA")  # not multiple of 3
    with pytest.raises(ValueError):
        recode_by_aa_min_changes("M", "ATGAAA")  # length mismatch
    with pytest.raises(ValueError):
        recode_by_aa_min_changes("Z", "ATG")  # invalid AA

