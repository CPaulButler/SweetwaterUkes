import argparse
import re
import sys
from pathlib import Path


SW_SUFFIX = re.compile(r"\s*-\s*S\s*W\s*$", re.IGNORECASE)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Remove a trailing -SW suffix from filenames under the current directory."
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Show the planned renames without changing files.",
    )
    parser.add_argument(
        "--replace",
        action="store_true",
        help="Replace existing destination files.",
    )
    return parser.parse_args()


def find_renames(root: Path) -> list[tuple[Path, Path]]:
    renames = []
    for source in root.rglob("*"):
        if not source.is_file():
            continue
        new_stem, count = SW_SUFFIX.subn("", source.stem)
        if count:
            renames.append((source, source.with_name(new_stem + source.suffix)))
    return renames


def main() -> int:
    args = parse_args()
    root = Path.cwd()

    try:
        renames = find_renames(root)
    except OSError as exc:
        print(f"Could not scan {root}: {exc}", file=sys.stderr)
        return 1

    if not renames:
        print(f"No matching files found under {root}.")
        return 0

    destinations: set[str] = set()
    duplicate_destinations = set()
    existing_conflicts = []
    for source, destination in renames:
        print(f"{source.name} -> {destination.name}")
        destination_key = str(destination).casefold()
        if destination_key in destinations:
            duplicate_destinations.add(destination)
        if destination.exists():
            existing_conflicts.append(destination)
        destinations.add(destination_key)

    if args.preview:
        print("Preview only; run without --preview to perform these renames.")
        if existing_conflicts:
            print("Destination conflicts detected; pass --replace to overwrite them.")
        if duplicate_destinations:
            print("Multiple files map to the same destination; resolve these conflicts before renaming.")
        return 0

    if duplicate_destinations:
        for destination in duplicate_destinations:
            print(f"Multiple files map to the same destination: {destination}", file=sys.stderr)
        print("No files were renamed. Resolve these conflicts before running again.", file=sys.stderr)
        return 1

    if existing_conflicts and not args.replace:
        for destination in existing_conflicts:
            print(f"Destination already exists or is duplicated: {destination}", file=sys.stderr)
        print("No files were renamed. Pass --replace to overwrite destination files.", file=sys.stderr)
        return 1

    try:
        for source, destination in renames:
            if args.replace:
                source.replace(destination)
            else:
                source.rename(destination)
    except OSError as exc:
        print(f"Could not rename files: {exc}", file=sys.stderr)
        return 1

    print(f"Renamed {len(renames)} file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
