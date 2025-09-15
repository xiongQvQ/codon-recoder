codon-recoder
================

Language: English | [中文](README.zh-CN.md)

Recode a DNA sequence to match a target amino‑acid sequence with the minimal number of nucleotide changes, preserving the reading frame. Includes a CLI and Python API.

Features
- Minimal-change recoding per codon using Hamming distance
- Tie-break strategies (wobble position, preferred codon)
- Detailed per-codon change report
- Strict input validation and clear errors

Install
- Local: `pip install -e .`

CLI Usage
- Basic: `codon-recoder --dna ATGGCCGCT --aa MAA`
- With report: `codon-recoder --dna dna.txt --aa aa.txt --report report.tsv`
- Options:
  - `--dna` or `--dna-file` for input DNA (A/T/G/C, length multiple of 3)
  - `--aa` or `--aa-file` for target AA (use `_` for stop)
  - `--tie-break {wobble,freq}` select tie-break strategy (default: wobble)
  - `--report` output path (TSV or JSON by extension)
  - `--quiet` suppress per-codon summary

Python API
```python
from codon_recode import recode_by_aa_min_changes, dna2aa

new_dna, report = recode_by_aa_min_changes(
    mut_aa="MKT_",
    dna="ATGAAAACGAAA",
    tie_break="wobble",
)
print(new_dna)
print(dna2aa(new_dna))
```

Notes
- Uses the standard genetic code. Stop is `_` (CLI also accepts `*`).
- Forbid internal stop by default. Enable explicit stop only if desired.
- Does not perform organism-specific codon optimization; uses a fixed preferred-codon map on ties.

Input formats
- Plain sequences or FASTA files are accepted for both DNA and AA inputs.
- Whitespace and line breaks are ignored. FASTA headers (`>` lines) are stripped.
- The AA length must equal the DNA codon count (`len(dna) / 3`).

Development
- Run tests: `pytest -q`
  - In restricted environments: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src pytest -q --capture=no -p no:cacheprovider`

Project
- License: MIT (see `LICENSE`)
- Contributing guide: see `CONTRIBUTING.md`

Examples
- Case 1 — Identity (no change required)
  - Command: `codon-recoder --dna ATGAAAACG --aa MKT`
  - Output:
    - new DNA: `ATGAAAACG`
    - AA(before): `MKT`
    - AA(after): `MKT`
    - Codons changed: `0 / 3`; Nucleotide changes: `0`

- Case 2 — Single amino-acid change with wobble tie (K→N)
  - Command: `codon-recoder --dna ATGAAAACG --aa MNT`
  - Output:
    - new DNA: `ATGAACACG`
    - AA(before): `MKT`
    - AA(after): `MNT`
    - Codons changed: `1 / 3`; Nucleotide changes: `1`

- Case 3 — Non‑wobble minimal change (A→P; change at first position)
  - Command: `codon-recoder --dna GCT --aa P`
  - Output:
    - new DNA: `CCT`
    - AA(before): `A`
    - AA(after): `P`
    - Codons changed: `1 / 1`; Nucleotide changes: `1`

- Case 4 — Accept `*` as stop
  - Command: `codon-recoder --dna ATGTAA --aa M*`
  - Output:
    - new DNA: `ATGTAA`
    - AA(before): `M_`
    - AA(after): `M_`
    - Codons changed: `0 / 2`; Nucleotide changes: `0`

- Case 5 — Internal stop forbidden (error) and allowed with flag
  - Error: `codon-recoder --dna ATGAAAACG --aa M*T`
    - Raises: `ValueError: Internal stop codon in mut_aa is forbidden`
  - Allowed: `codon-recoder --dna ATGAAAACG --aa M*T --allow-internal-stop`
    - new DNA: `ATGTAAACG`
    - AA(before): `MKT`
    - AA(after): `M_T`
    - Codons changed: `1 / 3`; Nucleotide changes: `1`

Support & Contact
- China (WeChat):
  - Contact (scan to add):
    
    ![WeChat - Add Me](img/addme.jpg)
  - Tip/Buy me a coffee (WeChat Pay):
    
    ![WeChat Pay - Tip](img/dashang.jpg)
- International options (pick what suits you):

  - Buy Me a Coffee: https://buymeacoffee.com/bowen007
  - Contact: xiongbojian007@gmail.com

Replace the placeholders above with your actual links/handles.
