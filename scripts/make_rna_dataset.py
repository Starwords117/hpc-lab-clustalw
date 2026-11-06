#!/usr/bin/env python3
"""Build a frozen ClustalW benchmark FASTA from a raw (possibly gzipped) FASTA.

Cleaning: uppercase; strip anything but ACGTN; U->T; drop sequences with too
many ambiguous bases or extreme lengths; drop exact duplicates; sample N
deterministically with a fixed seed (default: fixed date-like seed).
"""
import argparse
import gzip
import random


def read_seqs(path):
    op = gzip.open if path.endswith(".gz") else open
    name, chunks = None, []
    with op(path, "rt", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if name is not None:
                    yield name, "".join(chunks)
                parts = line[1:].split()
                name = parts[0] if parts else "seq"
                chunks = []
            else:
                chunks.append(line)
    if name is not None:
        yield name, "".join(chunks)


def clean(s):
    s = s.upper().replace("U", "T")
    return "".join(c for c in s if c in "ACGTN")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("input")
    p.add_argument("-o", "--out", required=True)
    p.add_argument("-n", type=int, default=800)
    p.add_argument("--min-len", type=int, default=150)
    p.add_argument("--max-len", type=int, default=700)
    p.add_argument("--max-n-frac", type=float, default=0.02)
    p.add_argument("--seed", type=int, default=20261106)
    a = p.parse_args()

    seen, pool = set(), []
    for name, raw in read_seqs(a.input):
        s = clean(raw)
        if not (a.min_len <= len(s) <= a.max_len):
            continue
        if s.count("N") / len(s) > a.max_n_frac:
            continue
        if s in seen:
            continue
        seen.add(s)
        pool.append((name, s))

    rng = random.Random(a.seed)
    take = pool if len(pool) <= a.n else rng.sample(pool, a.n)
    lens = [len(s) for _, s in take]
    with open(a.out, "w") as f:
        for i, (name, s) in enumerate(take):
            f.write(">rna_%05d|%s\n" % (i, name))
            for j in range(0, len(s), 60):
                f.write(s[j : j + 60] + "\n")
    print(
        "pool=%d taken=%d len min/mean/max = %d/%.0f/%d total_nt=%d"
        % (
            len(pool),
            len(take),
            min(lens),
            sum(lens) / len(lens),
            max(lens),
            sum(lens),
        )
    )


if __name__ == "__main__":
    main()
