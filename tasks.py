import shlex
import subprocess as sp
import sys


def _run_command(command: str) -> sp.CompletedProcess:
    tokenized_command = shlex.split(command)
    completed_process = sp.run(tokenized_command)
    exit_code = completed_process.returncode
    if exit_code:
        sys.exit(exit_code)
    return completed_process


def run_pylint():
    # Only run across changed files
    _run_command(
        "python -m pylint " "--rcfile=pylint.rc " "-j 8 " "corona_stats tests"
    )


def run_typechecking():
    _run_command("python -m mypy -p corona_stats -p tests")


def run_flake8():
    _run_command("python -m flake8 corona_stats tests")


def run_precommit():
    _run_command("pre-commit run --all-files")
