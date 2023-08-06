import subprocess
import sys


def test_end_to_end_all_modules():
    p = subprocess.run(
        [sys.executable, "-m", "importfiler", "pytest", "--mode", "all_modules"],
        stdout=subprocess.PIPE,
        text=True,
    )
    assert "_pytest" in p.stdout
    assert "pytest" in p.stdout
    assert (
        "email.header, email.message" in p.stdout
    )  # checks order of submodules based on time
