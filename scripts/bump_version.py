#!/usr/bin/env python3
"""Bump Flutterator version across all release-related files.

Source of truth: pyproject.toml [project].version (semver X.Y.Z, no leading v).

Usage:
  python scripts/bump_version.py 3.1.7
  python scripts/bump_version.py --patch
  python scripts/bump_version.py --check
  python scripts/bump_version.py 3.1.7 --dry-run
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
PYPROJECT_VERSION_RE = re.compile(r'^version\s*=\s*"([^"]+)"', re.MULTILINE)
FLUTTERATOR_VERSION_RE = re.compile(r'^VERSION\s*=\s*"([^"]+)"', re.MULTILINE)
BUILD_VERSION_RE = re.compile(r'^VERSION="(v[^"]+)"', re.MULTILINE)

REPO_ROOT = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class VersionTarget:
    path: Path
    label: str


VERSION_TARGETS = (
    VersionTarget(REPO_ROOT / "pyproject.toml", "pyproject.toml"),
    VersionTarget(REPO_ROOT / "flutterator.py", "flutterator.py"),
    VersionTarget(REPO_ROOT / "vscode-extension" / "package.json", "vscode-extension/package.json"),
    VersionTarget(REPO_ROOT / "vscode-extension" / "package-lock.json", "vscode-extension/package-lock.json"),
    VersionTarget(REPO_ROOT / "build.sh", "build.sh"),
    VersionTarget(REPO_ROOT / "build-standalone.sh", "build-standalone.sh"),
)

CHANGELOG_FILES = (
    REPO_ROOT / "CHANGELOG.md",
    REPO_ROOT / "vscode-extension" / "CHANGELOG.md",
)


def normalize_version(value: str) -> str:
    value = value.strip()
    if value.startswith("v"):
        value = value[1:]
    if not SEMVER_RE.match(value):
        raise ValueError(f"Invalid semver (expected X.Y.Z): {value!r}")
    return value


def read_pyproject_version() -> str:
    text = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    match = PYPROJECT_VERSION_RE.search(text)
    if not match:
        raise RuntimeError("Could not read version from pyproject.toml")
    return match.group(1)


def bump_patch(version: str) -> str:
    major, minor, patch = (int(part) for part in version.split("."))
    return f"{major}.{minor}.{patch + 1}"


def extract_version(path: Path) -> str | None:
    text = path.read_text(encoding="utf-8")

    if path.name == "pyproject.toml":
        match = PYPROJECT_VERSION_RE.search(text)
        return match.group(1) if match else None

    if path.name == "flutterator.py":
        match = FLUTTERATOR_VERSION_RE.search(text)
        return match.group(1) if match else None

    if path.name in {"build.sh", "build-standalone.sh"}:
        match = BUILD_VERSION_RE.search(text)
        if match:
            return normalize_version(match.group(1))
        return None

    if path.suffix == ".json":
        data = json.loads(text)
        if path.name == "package-lock.json":
            return data.get("version")
        return data.get("version")

    return None


def apply_version(path: Path, version: str) -> str:
    text = path.read_text(encoding="utf-8")

    if path.name == "pyproject.toml":
        new_text, count = PYPROJECT_VERSION_RE.subn(f'version = "{version}"', text, count=1)
        if count != 1:
            raise RuntimeError(f"Failed to update version in {path}")

    elif path.name == "flutterator.py":
        new_text, count = FLUTTERATOR_VERSION_RE.subn(f'VERSION = "{version}"', text, count=1)
        if count != 1:
            raise RuntimeError(f"Failed to update VERSION in {path}")

    elif path.name in {"build.sh", "build-standalone.sh"}:
        new_text, count = BUILD_VERSION_RE.subn(f'VERSION="v{version}"', text, count=1)
        if count != 1:
            raise RuntimeError(f'Failed to update VERSION in {path}')

    elif path.name == "package.json":
        data = json.loads(text)
        data["version"] = version
        new_text = json.dumps(data, indent=2) + "\n"

    elif path.name == "package-lock.json":
        data = json.loads(text)
        data["version"] = version
        if "" in data.get("packages", {}):
            data["packages"][""]["version"] = version
        new_text = json.dumps(data, indent=2) + "\n"

    else:
        raise RuntimeError(f"No update rule for {path}")

    path.write_text(new_text, encoding="utf-8")
    return new_text


def check_versions(expected: str | None = None) -> list[str]:
    expected = expected or read_pyproject_version()
    mismatches: list[str] = []

    for target in VERSION_TARGETS:
        found = extract_version(target.path)
        if found is None:
            mismatches.append(f"{target.label}: could not read version")
        elif found != expected:
            mismatches.append(f"{target.label}: {found} (expected {expected})")

    return mismatches


def bump(version: str, *, dry_run: bool = False) -> None:
    version = normalize_version(version)
    changes: list[tuple[str, str | None, str | None]] = []

    for target in VERSION_TARGETS:
        old = extract_version(target.path)
        if old == version:
            changes.append((target.label, old, old))
            continue

        if dry_run:
            changes.append((target.label, old, version))
            continue

        apply_version(target.path, version)
        changes.append((target.label, old, version))

    print(f"Target version: {version}")
    for label, old, new in changes:
        if old == new:
            print(f"  ok   {label} ({old})")
        else:
            print(f"  bump {label}: {old} -> {new}")

    if dry_run:
        print("\n(dry-run: no files written)")
    else:
        print("\nVersion files updated.")
        print("Remember to update release notes:")
        for changelog in CHANGELOG_FILES:
            print(f"  - {changelog.relative_to(REPO_ROOT)}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "version",
        nargs="?",
        help="New semver version (X.Y.Z). Omit with --patch to increment patch.",
    )
    parser.add_argument(
        "--patch",
        action="store_true",
        help="Increment patch from pyproject.toml",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verify all version files match pyproject.toml",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned changes without writing files",
    )
    args = parser.parse_args()

    if args.check:
        mismatches = check_versions()
        if mismatches:
            print("Version mismatch:")
            for line in mismatches:
                print(f"  - {line}")
            return 1
        current = read_pyproject_version()
        print(f"All version files match pyproject.toml ({current}).")
        return 0

    if args.patch:
        new_version = bump_patch(read_pyproject_version())
    elif args.version:
        new_version = normalize_version(args.version)
    else:
        parser.error("Provide VERSION or use --patch")

    try:
        bump(new_version, dry_run=args.dry_run)
    except (ValueError, RuntimeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
