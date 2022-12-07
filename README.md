# polyglot

A script runner that allows usage of multiple languages within the same script.

```shell
$ cat << EOF > script.poly
#!/usr/bin/env polyglot

#!/usr/bin/env python
print("Hello, Python!")

#!/usr/bin/env bash
echo "Hello, Bash!"
EOF
$ chmod +x ./script.poly
$ ./script.poly
Hello, Python!
Hello, Bash!
```

## installation

Python tooling is a bit of a mess, but personally I like [pipx](https://pypa.github.io/pipx/).

```shell
$ pipx install git+https://github.com/buckley-w-david/polyglot.git
```

## Usage

```
$ polyglot --help
                                                                                
 Usage: polyglot [OPTIONS] TARGET                                               
                                                                                
 Run a polyglot script                                                          
                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    target      PATH  The polyglot script to run. [default: None]           │
│                        [required]                                            │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --errexit               --no-errexit          If errexit the script will     │
│                                               exit if any script exits.      │
│                                               [default: errexit]             │
│ --communicate           --no-communicate      If communicate stdout from     │
│                                               each script will be fed into   │
│                                               stdin of the next.             │
│                                               [default: no-communicate]      │
│ --install-completion                          Install completion for the     │
│                                               current shell.                 │
│ --show-completion                             Show completion for the        │
│                                               current shell, to copy it or   │
│                                               customize the installation.    │
│ --help                                        Show this message and exit.    │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## Why?

The idea behind polyglot is that often times you'll run into situations within a single script that are awkward to implement in a single language.

For example something may be simple in Python, but painful in Bash, while a later in the same script the situation is reversed.

Instead of putting up with it (and doing it all in one language) or splitting something into multiple scripts (and having to coordinate calling them in series from some parent script), `polyglot` lets you write the parts in whatever language is easiest.

We're trying to get the benefits of the first option without the negatives.

## Examples

Check out [tests/test_polyglot/](tests/test_polyglot/) for some (very small) example scripts.
