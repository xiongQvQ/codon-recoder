from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Optional

from .recoder import recode_by_aa_min_changes, dna2aa


def _read_text(path: str) -> str:
    text = Path(path).read_text()
    return text


def _read_seq_arg(value: Optional[str], file_arg: Optional[str]) -> Optional[str]:
    if value is not None:
        return value.strip()
    if file_arg is not None:
        return _read_text(file_arg)
    return None


def _normalize_dna(text: str) -> str:
    # Allow FASTA: drop header lines starting with '>'
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    if any(ln.startswith('>') for ln in lines):
        lines = [ln for ln in lines if not ln.startswith('>')]
    seq = ''.join(lines).replace(' ', '').upper()
    return seq


def _normalize_aa(text: str) -> str:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    if any(ln.startswith('>') for ln in lines):
        lines = [ln for ln in lines if not ln.startswith('>')]
    seq = ''.join(lines).replace(' ', '').upper()
    # Accept '*' as stop; core will also normalize
    return seq


def _write_report(path: Path, report):
    if path.suffix.lower() == ".json":
        data = [r.__dict__ for r in report]
        path.write_text(json.dumps(data, indent=2))
    else:
        # TSV
        header = (
            "index\traw_codon\tnew_codon\traw_aa\ttarget_aa\taa_changed\t"
            "distance\tdiff_positions\tdecision\n"
        )
        lines = [header]
        for r in report:
            lines.append(
                f"{r.index}\t{r.raw_codon}\t{r.new_codon}\t{r.raw_aa}\t{r.target_aa}\t"
                f"{int(r.aa_changed)}\t{r.distance}\t{','.join(map(str, r.diff_positions))}\t{r.decision}\n"
            )
        path.write_text("".join(lines))


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="codon-recoder",
        description="Recode DNA to match a target amino-acid sequence with minimal nucleotide changes.",
    )
    g_in = p.add_argument_group("Input")
    g_in.add_argument("--dna", help="DNA sequence (A/T/G/C)")
    g_in.add_argument("--dna-file", help="File containing DNA sequence")
    g_in.add_argument("--aa", help="Target amino-acid sequence (use '_' for stop)")
    g_in.add_argument("--aa-file", help="File containing target AA sequence")

    p.add_argument("--tie-break", choices=["wobble", "freq"], default="wobble",
                   help="Tie-break strategy when multiple codons are equally close (default: wobble)")
    p.add_argument("--allow-internal-stop", action="store_true",
                   help="Allow internal stop in the target AA sequence")
    p.add_argument("--report", help="Optional path to write per-codon report (TSV or JSON by extension)")
    p.add_argument("--quiet", action="store_true", help="Do not print per-codon summary to stdout")

    return p


def main(argv: Optional[list[str]] = None) -> int:
    p = build_parser()
    args = p.parse_args(argv)

    dna_raw = _read_seq_arg(args.dna, args.dna_file)
    aa_raw = _read_seq_arg(args.aa, args.aa_file)
    dna = _normalize_dna(dna_raw) if dna_raw else None
    aa = _normalize_aa(aa_raw) if aa_raw else None
    if not dna or not aa:
        p.error("Provide --dna/--dna-file and --aa/--aa-file")

    new_dna, report = recode_by_aa_min_changes(
        aa, dna, tie_break=args.tie_break, forbid_internal_stop=not args.allow_internal_stop
    )

    print(new_dna)
    if not args.quiet:
        print(f"AA(before): {dna2aa(dna)}")
        print(f"AA(after) : {dna2aa(new_dna)}")
        changed = sum(1 for r in report if r.aa_changed)
        nt_changes = sum(r.distance for r in report)
        print(f"Codons changed: {changed} / {len(report)}; Nucleotide changes: {nt_changes}")

    if args.report:
        _write_report(Path(args.report), report)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
