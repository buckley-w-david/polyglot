import pytest
import typer

from polyglot import __version__

from polyglot.cli import run

def test_version():
    assert __version__ == '0.1.0'

SUCCESS_SCRIPT = """
#!/usr/bin/env python
print("Hello, Python!")
#!/usr/bin/env bash
echo "Hello, Bash!"
"""

def test_run_success(capfd, tmp_path):
    script = tmp_path / "test.poly"
    script.write_text(SUCCESS_SCRIPT)
    run(script)
    out, _ = capfd.readouterr()
    assert out == "Hello, Python!\nHello, Bash!\n"


FAIL_SCRIPT = """
#!/usr/bin/env python
import sys
print("I failed!", file=sys.stderr)
exit(1)
#!/usr/bin/env bash
echo "Hello, Bash!"
"""

def test_run_failure(capfd, tmp_path):
    script = tmp_path / "test.poly"
    script.write_text(FAIL_SCRIPT)
    with pytest.raises(typer.Exit) as excinfo:
        run(script)

    assert excinfo.value.exit_code == 1
    _, err = capfd.readouterr()
    assert err == "I failed!\n"

NO_SHEBANG_SCRIPT = """
print("Hello, Python!")
"""

def test_run_missing(capfd, tmp_path):
    script = tmp_path / "test.poly"
    script.write_text(NO_SHEBANG_SCRIPT)
    with pytest.raises(typer.Exit) as excinfo:
        run(script)

    assert excinfo.value.exit_code == 1
    _, err = capfd.readouterr()
    assert err == "Mismatch in shebang lines to content blocks\nDid you forget to add a shebang line?\n"
