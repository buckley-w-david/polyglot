from pathlib import Path
import tempfile
import os
import subprocess
import sys

import re

import typer

app = typer.Typer()

SHEBANG = r"^#!(/.*)"

@app.command()
def run(target: Path, errexit: bool = True):
    """
    Run a polyglot script
    """

    with open(target, 'r') as f:
        content = f.read()

    scripts = [s for chunk in re.split(SHEBANG, content.strip(), 0, re.MULTILINE) if (s := chunk.strip())]

    # Remove "#!/usr/bin/env polyglot" (or related) if present
    if Path(sys.argv[0]).name in scripts[0]:
        scripts = scripts[1:]

    if len(scripts) % 2:
        print("Mismatch in shebang lines to content blocks", file=sys.stderr)
        print("Did you forget to add a shebang line?", file=sys.stderr)
        raise typer.Exit(code=1)

    for i in range(0, len(scripts), 2):
        exe, content = scripts[i:i+2]

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
                raise typer.Exit(res.returncode)
        finally:
            os.remove(tmp_fpath)
