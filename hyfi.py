#!/usr/bin/env python3

import argparse
import re
import sys
from typing import Dict, FrozenSet, Iterator, List, Optional, Tuple


def load_words(file_path: str) -> FrozenSet[str]:
    with open(file_path, "r") as f:
        words = frozenset(word.strip() for word in f)
    return words


def load_user_rules(filepath: str) -> Dict[str, str]:
    """Load user rules from a file. The file format is 'original replacement' per line."""
    d = {}
    with open(filepath, "r") as f:
        for li, line in enumerate(f):
            p = line.split()
            if len(p) != 2:
                exit(f"Error: line {li+1}: invalid user rule: {line}")
            k, v = p
            d[k] = v
        return d


def generate_word_variants(word: str) -> List[str]:
    word_variants = []
    if not any(c.isalpha() for c in word):
        return word_variants

    wi = word
    for i in range(4):
        wj = wi
        for j in range(4):
            word_variants.append(wj)
            if wj and not wj[-1].isalpha():
                wj = wj[:-1]
            else:
                break
        if wi and not wi[0].isalpha():
            wi = wi[1:]
        else:
            break

    if any(c.isupper() for c in word):
        lowercase_variants = list(v.lower() for v in word_variants)
        word_variants.extend(lowercase_variants)

    return word_variants


def process_lines(
    line_it: Iterator[str],
    english_words: FrozenSet[str],
    user_rules: Dict[str, str] = {},
    unrecognized_pairs_sink: Optional[List[Tuple[str, str]]] = None,
) -> Iterator[str]:
    try:
        cur_line = next(line_it).split()
        line_num = 1
    except StopIteration:
        return  # empty file, nothing to process

    unrecognized_pairs = []
    for line in line_it:
        next_line = line.split()
        if cur_line and next_line and re.search(r"[-\u2010-\u2015]$", cur_line[-1]):
            concat_word = cur_line[-1] + next_line[0]
            if concat_word in user_rules:
                cur_line[-1] = user_rules[concat_word]
                next_line = next_line[1:]
            else:
                reformed_word = cur_line[-1][:-1] + next_line[0]
                joint_word_variants = generate_word_variants(reformed_word)
                if not any(word in english_words for word in joint_word_variants):
                    concat_word = cur_line[-1] + next_line[0]
                    unrecognized_pairs.append((concat_word, reformed_word))
                    print(
                        f'Warning: line {line_num + 1}: the word "{concat_word}" does not seem a valid English word.',
                        file=sys.stderr,
                    )
                else:
                    cur_line[-1] = reformed_word
                    next_line = next_line[1:]

        yield " ".join(cur_line)
        cur_line = next_line
        line_num += 1

    yield " ".join(cur_line)  # yield the last line

    if unrecognized_pairs_sink is not None:
        done_pairs = set()
        for p in unrecognized_pairs:
            if p in done_pairs:
                continue
            done_pairs.add(p)
            unrecognized_pairs_sink.append(p)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HyFi: Hyphen Fixer for English text.")
    parser.add_argument("input", help='The input text file to process or "-" for stdin.')
    parser.add_argument("-o", "--output", help="The output text file to write. If not given, write to stdout.")
    parser.add_argument(
        "-u", "--unrecognized-pairs", help="Each of the unrecognized words and its possible replacement."
    )
    parser.add_argument("-r", "--user-rules", help="The file containing user rules for replacing unrecognized words.")
    args = parser.parse_args()

    english_words = load_words("/usr/share/dict/words")

    input_stream = sys.stdin if args.input == "-" else open(args.input, "r")
    output_stream = sys.stdout if args.output is None else open(args.output, "w")
    try:
        user_rules = load_user_rules(args.user_rules) if args.user_rules else {}
        urps = []
        for line in process_lines(input_stream, english_words, user_rules=user_rules, unrecognized_pairs_sink=urps):
            output_stream.write(line + "\n")
    finally:
        if input_stream is not sys.stdin:
            input_stream.close()
        if output_stream is not sys.stdout:
            output_stream.close()
    if args.unrecognized_pairs is not None:
        with open(args.unrecognized_pairs, "w") as outp:
            for concat_word, reformed_word in urps:
                print(f"{concat_word} {reformed_word}", file=outp)
