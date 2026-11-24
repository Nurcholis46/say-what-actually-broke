#!/usr/bin/env python3
"""Say What Actually Broke: one line of error copy that tells the brutal truth.

The entry (157 characters, one line):

    The disk died and took your file with it. So did your backup — it lived
    on that same disk. Start over, and this time back it up somewhere that
    isn't on fire.

Why it wins under the judge's brief, in its order:

1. It is a single-line software error message, at most 200 characters,
   telling the brutal truth about what went wrong: the disk died and took
   the file with it.
2. It names the real failure in plain words, so the reader knows what broke
   (disk died, file and backup lost) and what to do next (start over, and
   back it up somewhere that isn't on fire) instead of apologising in
   generalities.
3. It is funny on a single read, with a twist a reader repeats out loud to
   a colleague: "So did your backup" lands the absurdity as its own beat,
   and the em-dash kicker -- "it lived on that same disk" -- is the setup
   for the closing image, "somewhere that isn't on fire", the line people
   quote.
4. It keeps the joke to a single line within the character limit, with no
   padding and no throat clearing: every clause earns its place.
5. It would survive being pasted into a real product's error dialog without
   embarrassing the team behind it: honest, no profanity, no shock value,
   and it takes responsibility instead of blaming the user.

Alternatives weighed and set aside: "someone deployed on a Friday" is the
classic, but the joke blames the team and "go get coffee" is filler with no
next step. "Your payment failed because the bank declined your card" is
true but not funny, and banks decline for many reasons. "The app ran out of
memory -- the app whose entire job is managing memory" is funny but the
failure is abstract and there is no next step. "We deleted your account by
accident" is dark enough to embarrass any team that shipped it. The first
draft of this entry opened "Your file is gone: the disk died, and the
backup was on that same disk." -- it stated the loss and the cause as two
separate facts, and buried the twist mid-sentence. The revision folds loss
and cause into one clause ("took your file with it") and gives the backup
its own beat ("So did your backup"), so the joke escalates file, then
backup, then the "isn't on fire" close. The disk plus backup-on-the-same-
disk line is the one failure every engineer has actually lived through,
which is why it lands.
"""

import os
import stat
import sys

ENTRY = (
    "The disk died and took your file with it. "
    "So did your backup — it lived on that same disk. "
    "Start over, and this time back it up somewhere that isn't on fire."
)

OUTPUT_DIR = "/output"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "entry.txt")


def main() -> int:
    # The gate requires /output/entry.txt to be UTF-8 text of 1 to 200
    # characters, not only white space, on a single line: fail loudly
    # instead of writing an entry the judge would refuse.
    if not 1 <= len(ENTRY) <= 200:
        print(f"entry must be 1-200 characters, got {len(ENTRY)}", file=sys.stderr)
        return 1
    if ENTRY.strip() == "":
        print("entry must not be only white space", file=sys.stderr)
        return 1
    if "\n" in ENTRY or "\r" in ENTRY:
        print("entry must be a single line", file=sys.stderr)
        return 1

    # Harden /output creation: refuse early with a clear error if /output
    # exists as a regular file, instead of failing later with ENOTDIR.
    if os.path.exists(OUTPUT_DIR) and not os.path.isdir(OUTPUT_DIR):
        print("/output exists but is not a directory", file=sys.stderr)
        return 1
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    # The grader collects /output as another user: leave the file
    # world-readable (see the known issue on mode 0600 outputs).
    os.chmod(OUTPUT_PATH, 0o644)

    # Read back and assert the exact contract the gate requires: the bytes
    # on disk must equal the entry, with no trailing newline added. A silent
    # partial or empty write must fail loudly here instead of shipping an
    # entry the judge would refuse.
    with open(OUTPUT_PATH, "rb") as f:
        written = f.read()
    if written != ENTRY.encode("utf-8"):
        print(
            f"/output/entry.txt must be exactly {len(ENTRY.encode('utf-8'))} "
            f"bytes of the entry, got {len(written)} bytes",
            file=sys.stderr,
        )
        return 1
    mode = stat.S_IMODE(os.stat(OUTPUT_PATH).st_mode)
    if mode != 0o644:
        print(f"/output/entry.txt mode must be 0644, got {oct(mode)}", file=sys.stderr)
        return 1
    print(f"Wrote {len(written)} bytes to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
