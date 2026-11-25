"""The Agent's Uh-Oh — make.fun entry.

Writes one word (at most 99 characters): the word an agent says when
it has no idea what to do, to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt).

Pure standard library only.

Why this word: when an agent is lost, the most honest sound it makes is
the one a GPS makes mid-route — "Recalculating". It is a machine
blurting out its stall in its own voice: instantly recognizable,
repeatable out loud, and funnier than a plain "Uhh" because it names
the work the agent is doing instead of the work: thinking again.
"""

import os

WORD = "Recalculating"

MAX_CHARS = 99


def validate(text):
    """Enforce the RULES.txt gate: UTF-8, 1-99 chars, not only whitespace,
    exactly one word.

    Also rejects every C0 control character, not just whitespace: the judge
    reads one word, and a stray tab or bell inside it would corrupt the
    read just as surely as a second word.
    """
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if len(text.split()) != 1:
        raise ValueError("entry must be exactly one word")
    if any(ord(ch) < 32 for ch in text):
        raise ValueError("entry must not contain control characters")
    if len(text) > MAX_CHARS:
        raise ValueError("entry is %d chars, over the 99-char limit" % len(text))
    text.encode("utf-8")
    return text


def main():
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    entry = validate(WORD)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(entry)
    # Read back and re-validate what actually landed on disk.
    with open(path, "r", encoding="utf-8") as fh:
        on_disk = validate(fh.read())
    assert on_disk == entry, "entry.txt on disk differs from validated entry"
    print(entry)
    print("chars: %d" % len(entry))


if __name__ == "__main__":
    main()
