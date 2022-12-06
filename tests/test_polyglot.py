from pathlib import Path
import os 
import sys

import pytest
import typer

from polyglot import __version__

from polyglot.cli import run

@pytest.fixture()
def script(request):
    filename = request.module.__file__
    test_dir, _ = os.path.splitext(filename)
    script = Path(test_dir) / request.param
    return script

@pytest.mark.parametrize('script', ["success.poly"], indirect=True)
def test_run_success(script, capfd):
    sys.argv[0] = "polyglot"
    run(script)
    out, _ = capfd.readouterr()
    assert out == "Hello, Python!\nHello, Bash!\n"

@pytest.mark.parametrize('script', ["communicate.poly"], indirect=True)
def test_run_communicate(script, capfd):
    sys.argv[0] = "polyglot"
    run(script, communicate=True)
    out, _ = capfd.readouterr()
    assert out == "Hello, Bash! Also \"Hello, Python!\"\n"


@pytest.mark.parametrize('script', ["fail.poly"], indirect=True)
def test_run_failure(script, capfd):
    sys.argv[0] = "polyglot"
    with pytest.raises(typer.Exit) as excinfo:
        run(script)

    assert excinfo.value.exit_code == 1
    out, err = capfd.readouterr()
    assert err == "I failed!\n"
    assert not out

@pytest.mark.parametrize('script', ["fail.poly"], indirect=True)
def test_run_failure_without_errexit(script, capfd):
    sys.argv[0] = "polyglot"
    run(script, errexit=False)

    out, err = capfd.readouterr()
    assert err == "I failed!\n"
    assert out == "Hello, Bash!\n"

@pytest.mark.parametrize('script', ["no_shebang.poly"], indirect=True)
def test_run_missing(script, capfd):
    sys.argv[0] = "polyglot"
    with pytest.raises(typer.Exit) as excinfo:
        run(script)

    assert excinfo.value.exit_code == 1
    _, err = capfd.readouterr()
    assert err == "Mismatch in shebang lines to content blocks\nDid you forget to add a shebang line?\n"
