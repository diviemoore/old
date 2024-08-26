# noqa: INP001
"""
This solution is largely based on the Playwright's browser dependencies script at
https://github.com/microsoft/playwright/blob/main/utils/linux-browser-dependencies/inside_docker/list_dependencies.js
"""
import logging
import subprocess

logger = logging.getLogger(__name__)


def find_packages(library_name):
    stdout, _code = run_command(["apt-file", "search", library_name])
    if not stdout.strip():
        return []
    libs = [line.split(":")[0] for line in stdout.strip().split("\n")]
    return list(set(libs))


def run_command(cmd, cwd=None, env=None):
    result = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, check=True)
    return result.stdout, result.returncode


def ldd(file_path):
    return run_command(["ldd", file_path])


raw_deps = ldd("/opt/chrome/chrome")
dependencies = raw_deps[0].splitlines()

missing_deps = {
    r[0].strip()
    for d in dependencies
    for r in [d.split("=>")]
    if len(r) == 2 and r[1].strip() == "not found"
}

missing_packages = []
for d in missing_deps:
    all_packages = find_packages(d)
    packages = [
        p
        for p in all_packages
        if not any(
            p.endswith(suffix) for suffix in ["-dbg", "-test", "tests", "-dev", "-mesa"]
        )
    ]
    for p in packages:
        missing_packages.append(p)

logger.info("missing_packages: " + (" ".join(missing_packages)))
