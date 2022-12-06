from pathlib import Path
import tempfile
import os
import subprocess

import typer

app = typer.Typer()

from typing import Iterator, Tuple


def partition(lines) -> Iterator[Tuple[str, str]]:
    buffer = []
    exe = None
    for line in lines:
        if line.startswith("#!/"):
            if exe and buffer:
                yield (exe, "\n".join(buffer))
            exe = line[2:]
            buffer = []
        else:
            buffer.append(line)
    if exe and buffer:
        yield (exe, "\n".join(buffer))


@app.command()
def run(target: Path, errexit: bool = True):
    """
    Run a polyglot script
    """

    with open(target, 'r') as f:
        content = f.read()

    lines = content.splitlines()
    start = 0
    while not lines[start].startswith("#!/") or 'polyglot' in lines[start]:
        start += 1

    for exe, content in partition(lines[start:]):
        # https://stackoverflow.com/a/17371096
        fd, tmp_fpath = tempfile.mkstemp()
        os.close(fd)
        try:
            with open(tmp_fpath, "w") as tmp:
                tmp.write(content)
            # TODO I'm not sure how quoting works in shebang lines
            #      exe.split() might break things
            res = subprocess.run([*exe.split(), tmp.name])
            if errexit and res.returncode != 0:
                exit(res.returncode)
        finally:
            os.remove(tmp_fpath)
