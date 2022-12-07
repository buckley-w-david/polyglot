from pathlib import Path
import tempfile
import os
import sys

from subprocess import Popen, PIPE
import shlex

import re

import typer

app = typer.Typer()

SHEBANG = r"^#!(/.*)"


@app.command()
def run(target: Path, errexit: bool = True, communicate: bool = False):
    """
    Run a polyglot script
    """

    with open(target, "r") as f:
        content = f.read()

    scripts = [
        s
        for chunk in re.split(SHEBANG, content.strip(), 0, re.MULTILINE)
        if (s := chunk.strip())
    ]

    # Remove "#!/usr/bin/env polyglot" (or related) if present
    if Path(sys.argv[0]).name in scripts[0]:
        scripts = scripts[1:]

    if len(scripts) % 2:
        print("Mismatch in shebang lines to content blocks", file=sys.stderr)
        print("Did you forget to add a shebang line?", file=sys.stderr)
        raise typer.Exit(code=1)

    in_ = b""
    if not sys.stdin.isatty() and communicate:
        in_ = sys.stdin.read().encode()

    stdin, stdout, stderr = None, None, None
    if communicate:
        stdin, stdout, stderr = PIPE, PIPE, PIPE

    for i in range(0, len(scripts), 2):
        exe, content = scripts[i : i + 2]

        # https://stackoverflow.com/a/17371096
        fd, tmp_fpath = tempfile.mkstemp()
        os.close(fd)
        try:
            with open(tmp_fpath, "w") as tmp:
                tmp.write(content)

            proc = Popen(
                [*shlex.split(exe), tmp.name], stdin=stdin, stdout=stdout, stderr=stderr
            )

            if communicate:
                in_, err = proc.communicate(input=in_)
            else:
                proc.wait()
                err = ""

            if errexit and proc.returncode:
                if communicate:
                    print(err, file=sys.stderr, end="")
                raise typer.Exit(proc.returncode)
        finally:
            os.remove(tmp_fpath)

    if communicate:
        print(in_.decode(), end="")
